from typing import Union
import base64, re, io, datetime
from PIL import Image

from image_processing import image_to_byte_array
from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
from firestore import upload_image_bytearray_to_filename, get_unique_id,\
    get_all_locations, get_location_w3w, update_document, get_document, \
        upload_document, get_all_photos_in_location
from locationVerifier import locationToW3W


# To run app
# uvicorn main:app --reload

# To exit app
# Control C

# See docs at:
# https://fastapi.tiangolo.com/#installation


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/allLocation")
def get_pins():
    locations = get_all_locations()
    return locations

@app.get("/location")
def get_pin_w3w(w3w: str):
    location = get_location_w3w(w3w)
    return location

@app.get("/photo")
def get_photo(ref: str):
    photo = get_document("photos", ref)
    photo["public_url"] = f"https://firebasestorage.googleapis.com/v0/b/hackathon2023-brown.appspot.com/o/{photo['photoRef']}?alt=media"
    return photo

@app.get("/collage")
def get_collage(ref: str):
    collage = get_document("collage", ref)
    collage["public_url"] = f"https://firebasestorage.googleapis.com/v0/b/hackathon2023-brown.appspot.com/o/{collage['collageRef']}?alt=media"
    return collage

@app.get("/photos")
def get_photos(locationId: str):
    photos = get_all_photos_in_location(locationId)
    for photo in photos:
        photo["public_url"] = f"https://firebasestorage.googleapis.com/v0/b/hackathon2023-brown.appspot.com/o/{photo['photoRef']}?alt=media"
    return photos

@app.post("/location")
def add_pin(
    lon: str = Form(...),
    lat: str = Form(...),
    file_: str = Form(...),
    comment: str = Form(...)):

    w3w = locationToW3W(float(lon), float(lat))

    place_data = {
        "lon": lon,
        "lat": lat,
        "w3w": w3w['words'],
        "num_images": 0,
    }
    placeRef = upload_document("places", place_data)

    photoRef = post_photo(placeRef, comment, file_)

    collageRef = post_collage(placeRef, file_, [])

    update_document("places", placeRef, {"latest_image": photoRef, "collageRef": collageRef})

    return placeRef

@app.post("/collage")
def post_collage(
    locationId: str = Form(...),
    file_: str = Form(...),
    comments: list = Form(...)
    ):

    im = Image.open(io.BytesIO(base64.b64decode(re.sub('^data:image/.+;base64,', '', file_))))
    im_resized_byte_array = image_to_byte_array(im)
    filename = get_unique_id() + ".jpg"

    fileRef = upload_image_bytearray_to_filename(im_resized_byte_array, filename)
    collageMetadata = {
        "location": locationId,
        "collageRef": fileRef,
        "comments": comments,
        "timestamp": datetime.datetime.utcnow().timestamp()
    }

    dataRef = upload_document("collage", collageMetadata)

    update_document("places", locationId, {"collageRef": dataRef})
    return dataRef

@app.post("/photo")
def post_photo(
    locationId: str = Form(...),
    comment: str = Form(...),
    file_: str = Form(...)):

    locationDoc = get_document("places", locationId)

    im = Image.open(io.BytesIO(base64.b64decode(re.sub('^data:image/.+;base64,', '', file_))))
    im_resized_byte_array = image_to_byte_array(im.convert("RGB"))
    filename = get_unique_id() + ".jpg"

    fileRef = upload_image_bytearray_to_filename(im_resized_byte_array, filename)
    photoMetadata = {
        "location": locationId,
        "photoRef": fileRef,
        "comment": comment,
        "timestamp": datetime.datetime.utcnow().timestamp()

    }
    dataRef = upload_document("photos", photoMetadata)
    update_document("places", locationId, {"latest_image": dataRef, "num_images": locationDoc["num_images"] + 1})
    return dataRef


    
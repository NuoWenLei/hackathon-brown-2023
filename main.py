from typing import Union
import base64, re, io, datetime
from PIL import Image

from image_processing import image_to_byte_array
from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
from firestore import upload_image_bytearray_to_filename, get_unique_id,\
    get_all_locations, get_location_w3w, update_document, get_document, \
        upload_document
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
def get_pin_w3w(w3w: str = Form(...)):
    location = get_location_w3w(w3w)
    return location

@app.post("/location")
def add_pin(
    lon: str = Form(...),
    lat: str = Form(...),
    imageRef: str = Form(...)):

    w3w = locationToW3W(lon, lat)

    place_data = {
        "lon": lon,
        "lat": lat,
        "w3w": w3w,
        "latest_image": imageRef,
        "num_images": 1
    }
    placeRef = upload_document("places", place_data)
    return placeRef

@app.post("/collage")
def post_collage(
    locationId: str = Form(...),
    file_: str = Form(...),
    comments: list = Form(...),
    timestamps: list = Form(...)
    ):

    locationDoc = get_document("places", locationId)

    im = Image.open(io.BytesIO(base64.b64decode(re.sub('^data:image/.+;base64,', '', file_))))
    im_resized_byte_array = image_to_byte_array(im)
    filename = get_unique_id() + ".jpg"

    fileRef = upload_image_bytearray_to_filename(im_resized_byte_array, filename)
    collageMetadata = {
        "location": locationId,
        "collageRef": fileRef,
        "comments": comments,
        "timestamps": timestamps,
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
    im_resized_byte_array = image_to_byte_array(im)
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


    
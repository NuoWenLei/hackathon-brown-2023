from typing import Union
import base64, re, io, datetime
from PIL import Image

from image_processing import image_to_byte_array
from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
from firestore import upload_image_bytearray_to_filename, get_unique_id,\
    upload_photo_data, upload_place_tag, get_all_locations, get_location_w3w,\
        update_document, get_document


# To run app
# uvicorn main:app --reload

# To exit app
# Control C

# See docs at:
# https://fastapi.tiangolo.com/#installation

# See interactive api at:
# http://127.0.0.1:8000/docs

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
    w3w: str = Form(...),
    imageRef: str = Form(...)):

    place_data = {
        "lon": lon,
        "lat": lat,
        "w3w": w3w,
        "latest_image": imageRef,
        "num_images": 1
    }
    placeRef = upload_place_tag(place_data)
    return placeRef

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
    dataRef = upload_photo_data(photoMetadata)
    update_document("places", locationId, {"latest_image": dataRef, "num_images": locationDoc["num_images"] + 1})
    return dataRef


    
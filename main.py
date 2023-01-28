from typing import Union
import base64, re, io
from PIL import Image

from image_processing import image_to_byte_array
from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
from firestore import upload_image_bytearray_to_filename, get_unique_id, upload_photo_data, upload_place_tag


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

@app.post("/location")
def add_pin(
    lon: str = Form(...),
    lat: str = Form(...)):

    # TODO: maybe save as What3Words?
    place_data = {
        "lon": lon,
        "lat": lat
    }
    placeRef = upload_place_tag(place_data)
    return placeRef

@app.post("/photo")
def post_photo(
    locationId: str = Form(...),
    file_: str = Form(...)):

    im = Image.open(io.BytesIO(base64.b64decode(re.sub('^data:image/.+;base64,', '', file_))))
    im_resized_byte_array = image_to_byte_array(im)
    filename = get_unique_id() + ".jpg"
    fileRef = upload_image_bytearray_to_filename(im_resized_byte_array, filename)
    photoMetadata = {
        "location": locationId,
        "photoRef": fileRef
    }

    dataRef = upload_photo_data(photoMetadata)
    return dataRef


    
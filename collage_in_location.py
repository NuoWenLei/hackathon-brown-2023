import requests
import base64
import tempfile
from io import BytesIO
from collager import Collager
from firestore import get_all_photos_in_location, download_image_to_filename

def create_collage_in_location(location):
    # get all photos of one locaion from firestore to the imagesPath
    imageInfos = get_all_photos_in_location(location)
    # [{'location': 'edTNI7cej0YFVYHfA5xe',
    #   'photoref': 'something.jpg',
    #   'username': 'nlei'}]
    # imageInfos = sorted(imageInfos, key=lambda d: d['timestep']) # in ascending order
    photorefs = [ imageInfo['photoRef'] for imageInfo in imageInfos ]
    # photorefs = [ imageInfo['timestep'] for imageInfo in imageInfos ]
    # comments_from_old_to_new = [ imageInfo['comments'] for imageInfo in imageInfos ]

    with tempfile.TemporaryDirectory() as imagesPath:
        print(imagesPath)
        download_image_to_filename(photorefs, imagesPath)

        # make a collage img
        width, height = (1920, 1080)
        lines = 3
        collager = Collager(imagesPath)
        collage = collager.collage(width, height, lines)
    collage = collage.convert("RGB")
    # collage.save("/Users/nuowenlei/Desktop/collage_env.png", format="JPEG")

    # upload collage
    buffered = BytesIO()
    collage.save(buffered, format="JPEG")
    collage_str = base64.b64encode(buffered.getvalue())

    requests.post("http://139.144.57.146:8000/collage", data={'locationId': location, 'file_': collage_str})
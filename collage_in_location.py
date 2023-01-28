import requests
import base64
from io import BytesIO
from collager import Collager
from firestore import get_all_photos_in_location, download_image_to_filename

def create_collage_in_location(location):
    # get all photos of one locaion from firestore to the imagesPath
    imageInfos = get_all_photos_in_location(location)
    # [{'location': 'edTNI7cej0YFVYHfA5xe',
    #   'photoref': 'something.jpg',
    #   'username': 'nlei'}]
    photorefs = [ imageInfo['photoref'] for imageInfo in imageInfos ]

    imagesPath = "/Users/air17/Documents/showCollageAPI/dogs"
    download_image_to_filename(photorefs, imagesPath)

    # make a collage img
    width, height = (1920, 1080)
    lines = 5
    collager = Collager(imagesPath)
    collage = collager.collage(width, height, lines)
    # collage.save("collage_env.png")

    # upload collage
    buffered = BytesIO()
    collage.save(buffered, format="JPEG")
    collage_str = base64.b64encode(buffered.getvalue())

    requests.post("127...", data={'location': location, 'file_': collage_str, 'collage': True})

create_collage_in_location("edTNI7cej0YFVYHfA5xe")
# from firestore import download_image_to_filename
from collager import Collager

fp = ""
# download_image_to_filename(fp)
# path = "D:/Projects/cats_dataset/best"
path = "/Users/air17/Documents/showCollageAPI/dogs"
width, height = (1920, 1080)
lines = 5

collager = Collager(path)
collage = collager.collage(width, height, lines)
collage.save("collage1.png")
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore, storage

cred = credentials.Certificate('hackathon2023-brown-firebase-adminsdk-j9tvt-4d881dd810.json')

# Application Default credentials are automatically created.
app = firebase_admin.initialize_app(cred, {"storageBucket": "hackathon2023-brown.appspot.com"})

bucket = storage.bucket()

def download_image_to_filename(fp):
	blob = bucket.blob("something.jpg")
	blob.download_to_filename(fp)

db = firestore.client()

ref = db.collection("photos").document("93WjlFDDGjBOtyKMenwU")

print(ref.get())




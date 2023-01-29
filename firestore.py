import firebase_admin, uuid, datetime
from firebase_admin import credentials
from firebase_admin import firestore, storage

cred = credentials.Certificate('hackathon2023-brown-firebase-adminsdk-j9tvt-4d881dd810.json')

# Application Default credentials are automatically created.
app = firebase_admin.initialize_app(cred, {"storageBucket": "hackathon2023-brown.appspot.com"})
db = firestore.client()
bucket = storage.bucket()

def get_unique_id():
	doc_id = str(uuid.uuid4())
	return doc_id + "-" + str(int(datetime.datetime.utcnow().timestamp()))

def download_image_to_filename(paths, fp):
	for p in paths:
		blob = bucket.blob(p)
		blob.download_to_filename(fp + "/" + p)
	
def upload_image_bytearray_to_filename(bytearr, fp):
	blob = bucket.blob(fp)
	blob.upload_from_file(bytearr, content_type = "image/jpeg")
	return fp

def get_all_locations():
	docs = db.collection("places").stream()
	locations = []
	for doc in docs:
		locations.append(doc.to_dict())
	return locations

def get_location_w3w(w3w):
	doc = db.collection("places").where("w3w", "==", w3w).get()
	return doc

def get_all_photos_in_location(locationRef):
	docs = db.collection("photos").where("location", "==", locationRef).stream()
	photoDocs = []
	for doc in docs:
		photoDocs.append(doc.to_dict())
	return photoDocs

def upload_document(collection, data):
	col = db.collection(collection)
	dataDoc = get_unique_id()
	col.document(dataDoc).create(data)
	return dataDoc

def update_document(collection, id, data):
	ref = db.collection(collection).document(id)
	ref.update(data)

def get_document(collection, id):
	return db.collection(collection).document(id).get()







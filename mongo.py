import pymongo


def createClient():
	mongo_uri = "mongodb+srv://brown-hack-dev:THTmh2KowR1mOfBR@cluster0.jds65oj.mongodb.net/?retryWrites=true&w=majority"
	client = pymongo.MongoClient(mongo_uri, tlsInsecure = True)
	db = client.all_db

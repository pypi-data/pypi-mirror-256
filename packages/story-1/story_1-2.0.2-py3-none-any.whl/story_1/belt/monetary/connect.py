
'''
	import story_1.belt.monetary.connect as monetary_connect
	monetary_connection = monetary_connect.start ()
'''

def start ():
	mongo_client = pymongo.MongoClient ("mongodb://localhost:50001")
	return mongo_client
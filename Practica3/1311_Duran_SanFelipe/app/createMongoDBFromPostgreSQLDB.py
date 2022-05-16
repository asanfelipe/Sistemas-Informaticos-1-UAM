import pymongo
import sys
import inspect
import os
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import database
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["si1"]
if 'si1' in client.list_database_names():
	db.collection.drop()
	client.drop_database("si1")
else:
    print("La base de datos no estaba creada.")
collection = db["topUSA"]
movies = database.db_topUSA()

for item in movies:
	dict = {"title": item[0], 
		   "year": item[1],
		   "genres": item[2],
		   "directors": "",
		   "actors": item[3]}
	directors=database.db_getDirectors(item[0])
	if directors:
		for x in directors:
			dict["directors"]=dict["directors"]+str(x)
	else:
		dict["directors"]="Sin un director especifico"
	x = collection.insert_one(dict)


def mongo_Life():
	try:
		query=db.topUSA.find({"title":{"$regex":"Life"}});
		return list(query)
	except:
		print("Error Life")
		return []

	
def mongo_Allen():
	try:
		query=db.topUSA.find({"directors":{"$regex":"Allen, Woody"},"year":{"$regex":"199"}});
		return list(query)
	except:
		print("Error Allen")
		return []
	
def mongo_ParsonsGalecki():
	try:
		query=db.topUSA.find({"$and":[{"actors":{"$regex":"Parsons"}},{"actors":{"$regex":"Galecki"}}]});
		return list(query)
	except:
		print("Error Parsons")
		return []

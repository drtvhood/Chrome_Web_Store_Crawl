#Made by Dm
# This script Fetches manifest file from downloaded crx packages
#updates permissions to Database
# Fetches only permission if packages folder has crx packages in it

import json  
import zipfile  
import os
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client['pymongo_test'];
posts = db.posts

ls=os.listdir("Packages/")

for ExtId in ls:
	d = None  
	data = None  
	filename= "manifest.json"
	with zipfile.ZipFile(ExtId, "r") as z:
		with z.open(filename) as f:
			data = f.read()
			d = json.loads(data)
			C= { 'permissions' : d.get("permissions") }
			posts.update({ 'UID' : ExtId.replace(".crx" , "")  } , C)
	

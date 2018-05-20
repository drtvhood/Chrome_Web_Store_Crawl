# Made By DM
# This script downloads chrome extension crx packages from the store
# Serial Download
from tqdm import tqdm
import requests
from pymongo import MongoClient
from bson import json_util
import time
import json  
import zipfile  
import os

client = MongoClient('localhost', 27017)
db = client['Chrome-Webstore-Extensions'];
posts = db.posts
tqdm.monitor_interval = 0
for post in tqdm(posts.find({ 'Manifest': { "$exists" : False } }).batch_size(10)):
	try :
		ExtId=post.get('UID')
		url = "https://clients2.google.com/service/update2/crx?response=redirect&prodversion=62.0.3202.94&x=id%3D"+ExtId+"%26uc"
		response = response = requests.get(url, stream=True)
		with open("Packages/"+ExtId+".crx", "wb") as handle:
			for data in tqdm(response.iter_content()):
				handle.write(data)
		handle.close();
		response.close();
		d = None  
		data = None  
		filename= "manifest.json"
		with zipfile.ZipFile("Packages/"+ExtId+".crx", "r") as z:
			with z.open(filename) as f:
				data = f.read()
				d = json.loads(data)
				C= {'Manifest' : d }
				posts.update({ 'UID' : ExtId.replace(".crx" , "")  } , { "$set": C })

		os.remove("Packages/"+ExtId+".crx"); # Comment this line if packages need to be stored.

	except Exception, e:
		f = open('log_Download.txt', 'a')
		f.write("\n" + post.get('UID'))
		f.write('-An exceptional thing happed - %s' % e)
		f.close()
		pass

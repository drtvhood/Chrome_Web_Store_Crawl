# Made By DM
# This script downloads chrome extension crx packages from the store
#multithreading downloading 


from tqdm import tqdm
import requests
from pymongo import MongoClient
from bson import json_util
import time
import json  
import zipfile  
import os
import threading
P=4; #Num of threads < 2

client = MongoClient('localhost', 27017)
db = client['Chrome-Webstore-Extensions'];
posts = db.posts
tqdm.monitor_interval = 0
ls=posts.find({'Manifest': { "$exists" : False } }).distinct('UID');
N=1001

def fetch(i):
	for x in tqdm(range(i,i+N/P)):
		ExtId = ls[x]
		client = MongoClient('localhost', 27017)
		dbx = client['Chrome-Webstore-Extensions'];
		px = dbx.posts
		try:
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
					
					px.update({ 'UID' : ExtId.replace(".crx" , "")  } , { "$set": C })

			os.remove("Packages/"+ExtId+".crx");

		except Exception, e:
			f = open('log_Download.txt', 'a')
			f.write("\n" + str(ExtId) + str(i) )
			f.write('-An exceptional thing happed - %s' % e)
			f.close()

			pass


def createNewDownloadThread(i):
    download_thread = threading.Thread(target=fetch, args=(i,))
    download_thread.start()

for i in range(0,N-N/P, N/P):
	createNewDownloadThread(i)



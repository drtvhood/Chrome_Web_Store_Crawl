# Made By DM
# This script downloads chrome extension crx packages from the store
from tqdm import tqdm
import requests
from pymongo import MongoClient
from bson import json_util
import time

client = MongoClient('localhost', 27017)
db = client['pymongo_test'];
posts = db.posts
tqdm.monitor_interval = 0
for post in tqdm(posts.find({},{'_id': False}), ascii=True):
	ExtId=post.get('UID')
	url = "https://clients2.google.com/service/update2/crx?response=redirect&prodversion=62.0.3202.94&x=id%3D"+ExtId+"%26uc"
	response = response = requests.get(url, stream=True)
	with open("Packages/"+ExtId+".crx", "wb") as handle:
		for data in tqdm(response.iter_content()):
			handle.write(data)
	handle.close();
	response.close();

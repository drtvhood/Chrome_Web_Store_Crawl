# Made By DM
# This script scrapes UIDs and Names of the extenions from Google Chrome Webstore and saves it to MongoDb
#Change the pv parameter accordingly.
# Theres no specific sorting order .  
# This Script has to be run First.
import requests
import re
import json
from pymongo import MongoClient
from bson import json_util
import io
import time
from tqdm import tqdm


#client = MongoClient('localhost', 27017)
#db = client['Chrome-Webstore-Extensions']; # Name of the database
#posts = db.posts

def Process(strs):
	z=strs.replace('"',"").split(",");
	y=dict({'UID':z[0],'Name': z[1]})
	return y;

TotalCount=70400; # Total No of Extensions IDs to be Scraped.
FetchCount=200; # No of Extension to be fetched at each iteration . This parameter should not be higher than 200.
tqdm.monitor_interval = 0
for i in tqdm(range(70000,TotalCount,FetchCount)):
	time.sleep(3);
	url = 'https://chrome.google.com/webstore/ajax/item?hl=en-US&gl=US&pv=20180301&mce=atf%2Cpii%2Crtr%2Crlb%2Cgtc%2Chcn%2Csvp%2Cwtd%2Cnrp%2Chap%2Cnma%2Cc3d%2Cncr%2Cctm%2Cac%2Chot%2Cmac%2Cfcf%2Crma%2Cpot%2Cevt%2Crer%2Crae%2Cshr%2Cesl&requestedCounts=infiniteWall%3A'+str(FetchCount)+'%3A0%3Atrue&token=infiniteWall%3A0%40351725%3A'+str(i)+'%3Atrue&category=extensions&_reqid=56766778&rt=j';
	r=requests.post(url);
	link_re = re.compile('"[a-z]{32}",".*?"')
	links = link_re.findall(r.text)
	a= list(set(links));
	c = [i.encode('UTF-8') for i in a]
	b=(map(Process, c))
	new_result = posts.insert_many(b)
	




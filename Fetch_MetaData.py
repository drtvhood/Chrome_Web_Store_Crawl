import requests
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from tqdm import tqdm

client = MongoClient('localhost', 27017)
db = client['Chrome-Webstore-Extensions'];
posts = db.posts
tqdm.monitor_interval = 0
ls =posts.find({ 'Updated' : { "$exists" : False } });
for post in tqdm(ls):
	try :
		Name = post.get('Name').replace(' ', '-');
		Url = 'https://chrome.google.com/webstore/detail/'+Name+'/'+post.get('UID')+'?hl=en'
		response = requests.get(Url)
		soup = BeautifulSoup(response.text, "lxml")
		Description = soup.find("meta",attrs ={ 'name':'Description'})
		url = soup.find("meta",  property="og:url")
		Version= soup.find("meta", itemprop="version") 
		Etype=soup.find("meta", property="og:type")
		Os= soup.find("meta", itemprop="operatingSystem")
		C={ "Description" : Description["content"] , "Og:url" : url["content"] , "Version" : Version["content"], "type" : Etype["content"] , "Operating System " : Os["content"] , 'Updated' : True }
			
		posts.update({'UID' : post.get('UID')} , C)
	except Exception, e:
		f = open('log.txt', 'a+')
		f.write("\n" + post.get('UID'))
		f.write('An exceptional thing happed - %s' % e)
		f.close()
		pass

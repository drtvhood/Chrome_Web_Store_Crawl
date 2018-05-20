##This fetches only the category of the extensions as its not stored in meta tags , its stored <Attribute> tags , for some reason
## beautifulSoup is not workigng For <attribute> tag so simple string match pattern is implemented in this 


import requests
from pymongo import MongoClient
from tqdm import tqdm
import re

client = MongoClient('localhost', 27017)
db = client['Chrome-Webstore-Extensions'];
posts = db.posts
tqdm.monitor_interval = 0
ls =posts.find({ 'Category': { "$exists" : False } });
for post in tqdm(ls):
	try :
		Name = post.get('Name').replace(' ', '-').replace('/[&\/\\:"*<>|?]/g','');
		Url = 'https://chrome.google.com/webstore/detail/'+Name+'/'+post.get('UID')+'?hl=en'
		response = requests.get(Url)
		link_re = re.compile(r'<Attribute name="category">.*</Attribute>')
		links = link_re.findall(response.text)
		Category=links[0].split("<")[1].split(">")[1];
		C= {'Category' : Category }
		posts.update({'UID' : post.get('UID')}, { "$set": C })
	
	except Exception, e:
			f = open('log_category.txt', 'a+')
			f.write("\n" + str(post.get('_id')))
			f.write('An exceptional thing happed - %s' % e)
			f.close()
			pass

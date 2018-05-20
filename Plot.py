from pymongo import MongoClient
import json 

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt


#critical permission listed by google Chrome.
permW= ["bookmarks" , "clipboardRead" , "clipboardWrite" , "contentSettings" , "debugger" , "desktopCapture" , "downloads" ,
	"geolocation" , "history" , "management" , "nativeMessaging" , "notifications" , "pageCapture" , "privacy" ,"proxy" , "system.storage" , "tabCapture" , "tabs" , "topSites" , "ttsEngine" , "webNavigation" , "http://*/*" , "https://*/*" , "*://*/*" , "<all_urls>"]

N= len(permW);
Count = [0] * N;
 
client = MongoClient('localhost', 27017)
db = client['Chrome-Webstore-Extensions'];
posts = db.posts

for post in posts.find({ 'Category' : '6_news' ,'Manifest': { "$exists" : True } }):
	z=(post.get("Manifest").get("permissions" , "empty"));
	for i in range(N):
		if permW[i] in z :
			Count[i]=Count[i]+1;


print(Count);




plt.barh( permW,Count, align='center', alpha=0.5)
plt.yticks(permW, permW)
plt.xlabel('No of Each Permission used ')
plt.title('Critical Permissions Used in News Category ')
 
plt.show()

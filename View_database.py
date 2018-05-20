# Just to query the database.

from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client['Chrome-Webstore-Extensions'];
posts = db.posts

ls=posts.find({ 'Category' : '6_news' ,'Manifest': { "$exists" : True } }).distinct('UID');
print(len(ls));


from google.appengine.ext import ndb
from mylist import MyList

class MyUser(ndb.Model):
    wordList = ndb.StructuredProperty(MyList, repeated=True)

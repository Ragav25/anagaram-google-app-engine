from google.appengine.ext import ndb

class WordList(ndb.Model):
    words = ndb.StringProperty(repeated= True)

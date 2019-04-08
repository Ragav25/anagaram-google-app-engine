from google.appengine.ext import ndb

class WordList(ndb.Model):
    words = ndb.StringProperty(repeated = True)
    # Counter
    uniqueAnagramCounter = ndb.IntegerProperty()
    wordCounter = ndb.IntegerProperty()
    # BlobStore
    # filenames = ndb.StringProperty(repeated=True)
    # blobs = ndb.BlobKeyProperty(repeated=True)

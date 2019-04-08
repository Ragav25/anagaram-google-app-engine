import webapp2
import jinja2
import os
import logging

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.api import taskqueue
from WordList import WordList


JINJA_ENVIRONMENT = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape = True
)

class BlobPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        userId = users.get_current_user().user_id()

        key = ndb.Key('WordList',userId)
        wordList = key.get()

        if wordList == None:
            wordList = WordList(id=userId, wordCounter = 0, uniqueAnagramCounter = 0)
            wordList.put()

        template_values = {
        'collection' : wordList,
        # 'upload_url': blobstore.create_upload_url('/upload'),
        # 'wordCounter': wordList.wordCounter,
        # 'uniqueAnagramCounter': wordList.uniqueAnagramCounter,
        # 'UploadedFile': UploadedFile
        }



        template = JINJA_ENVIRONMENT.get_template('blobpage.html')
        self.response.write(template.render(template_values))

    def post(self):
        userId = users.get_current_user().user_id()
        fileContent = self.request.POST.multi['my_file'].file

        while True:
            wordToSave = fileContent.readline()
            if wordToSave == None or wordToSave == "":
                break
            wordToSave = str(wordToSave.lower())
            wordToSave = wordToSave.strip()
            logging.info(wordToSave)

            key = ndb.Key('WordList', userId)
            wordList = key.get()
            wordList.words.append(wordToSave)

            task = taskqueue.add(url='/update_counter', target='worker',
            params={'newWordToSave': wordToSave, 'key': userId})

            wordList.put()
            self.redirect('/')

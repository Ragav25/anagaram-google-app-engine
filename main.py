import os
import jinja2
import webapp2
import logging
from google.appengine.api import users

# from google.appengine.api import users
from google.appengine.ext import ndb

# from myuser import MyUser
from WordList import WordList

JINJA_ENVIRONMENT = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape = True
)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type']='text/html'

        userId = users.get_current_user().user_id()

        key = ndb.Key('WordList',userId)
        wordList = key.get()
        if wordList == None:
            wordList = WordList(id=userId)
            wordList.put()

        emptyList =[]

        lexicoList = []

        # for j in emptyList:
        #     y = sorted(j)
        #     lexicoList.append(y)
        #
        # tupleValue = tuple(lexicoList)
        #
        # tupleValue = [tuple(x) for x in lexicoList]
        #
        # # keyValue = dict(zip(d, b))
        # dictionary = dict(zip(tupleValue, emptyList))

        # logging.info(emptyList)

        template_values = {
        'wordList': wordList,
        # 'emptyList': emptyList,
        # 'lexicoList': lexicoList,
        # 'length': len(emptyList),
        # 'keyValue': dictionary
        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

    def post(self):
        action = self.request.get('button')

        userId = users.get_current_user().user_id()

        emptyLexi = []
        logging.info(emptyLexi)

        if action == 'add':
            newWordToSave = self.request.get('list1')

            key = ndb.Key('WordList', userId)
            wordList = key.get()
            wordList.words.append(newWordToSave.lower())

            wordList.put()

            self.redirect('/')

app = webapp2.WSGIApplication([('/', MainPage)], debug = True)

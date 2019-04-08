import os
import jinja2
import webapp2
import logging
import re
from google.appengine.api import users
from google.appengine.ext import ndb

from page2 import Page2
from WordList import WordList
from anagramUtils import createLexicoGraphicalSort, createWordDict
from blobPage import BlobPage


JINJA_ENVIRONMENT = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape = True
)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        welcome = 'welcome'
        searchAnagram = self.request.get('sentence')

        user = users.get_current_user()

        if user == None:
            template_values = {
            'login_url': users.create_login_url(self.request.uri)
            }

            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            return

        key = ndb.Key('WordList',user.user_id())
        wordList = key.get()

        if wordList == None:
            wordList = WordList(id=user.user_id(), wordCounter = 0, uniqueAnagramCounter = 0)
            wordList.put()

        wordDict = createWordDict(wordList.words)
        # anagramWord = []
        anagramOutput = dict()
        splitWord = None

        if searchAnagram != None and searchAnagram != '':
            words = searchAnagram
            words = words.lower()
            words = str(words.strip())
            splitWord = words.split()
            for word in splitWord:
                anagramOutput[word] = []
                wordLex = createLexicoGraphicalSort(word)
                if wordLex in wordDict:
                    anagramOutput[word] = ", ".join(wordDict[wordLex])
                else:
                    anagramOutput[word] = "Sorry!! No Anagram Found"

        template_values = {
        'logout_url': users.create_logout_url(self.request.uri),
        'user': user,
        'welcome': welcome,
        'wordList': wordList,
        'anagramOutput':anagramOutput,
        'wordCounter': wordList.wordCounter,
        'uniqueAnagramCounter': wordList.uniqueAnagramCounter

        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

    def post(self):

        action = self.request.get('button')

        userId = users.get_current_user().user_id()

        if action == 'Scramble':
            key = ndb.Key('WordList', userId)
            wordList = key.get()

            searchAnagram = self.request.get('anagram')

            if re.match("^[a-zA-Z'\s']*$", searchAnagram):
                url = "/?sentence=" + searchAnagram
                self.redirect(url)
            else:
                self.redirect('/errorOnlyText')

        elif action == 'Try Another':
            self.redirect('/')

class ErrorOnlyText(webapp2.RequestHandler):
    def get(self):
        userId = users.get_current_user().user_id()
        key = ndb.Key('WordList', userId)
        wordList = key.get()

        template_values ={
        'wordList': wordList
        }

        template = JINJA_ENVIRONMENT.get_template('errorOnlyText.html')
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([('/', MainPage), ('/page2', Page2),
('/blobpage', BlobPage), ('/errorOnlyText', ErrorOnlyText)], debug = True)

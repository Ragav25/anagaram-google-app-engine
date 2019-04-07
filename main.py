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
        anagramWord = []
        anagramOutput = dict()
        splitWord = None

        if searchAnagram != None and searchAnagram != '':
            words = searchAnagram
            words = words.lower()
            words = str(words.strip())
            splitWord = words.split()
            for word in splitWord:
                logging.info("$$$"+word)
                anagramOutput[word] = []
                wordLex = createLexicoGraphicalSort(word)
                if wordLex in wordDict:
                    anagramOutput[word] = ", ".join(wordDict[wordLex])
                else:
                    anagramOutput[word] = "Sorry!! No Anagram Found"

        # if list2 != []:
        #     anagram = [j for i in list2 for j in i]
        #     anagramValues = ', '.join(anagram)
        #
        # elif list2 == []:
        #     anagramValues = "Sorry!! No Anagram Found"

            # logging.info(anagramValues)

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


app = webapp2.WSGIApplication([('/', MainPage), ('/page2', Page2)], debug = True)

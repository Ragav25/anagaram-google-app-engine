from google.appengine.ext import ndb
from google.appengine.api import users
import webapp2
from WordList import WordList
import logging
from anagramUtils import createLexicoGraphicalSort, createWordDict

class HandlerCounterUpdate(webapp2.RequestHandler):
    @ndb.transactional
    def update(self, newWordToSave, key):
        wordListKey = ndb.Key('WordList', key)
        wordList = wordListKey.get()

        wordList.wordCounter += 1
        wordDict = createWordDict(wordList.words)
        lexicoWord = createLexicoGraphicalSort(newWordToSave)
        logging.info('$$$ ' + lexicoWord)
        logging.info(wordDict)
        if len(wordDict[lexicoWord]) == 1:
            wordList.uniqueAnagramCounter += 1
        wordList.put()
        # self.redirect('/page2')

    def post(self):
        logging.info("$$$$$$")
        newWordToSave = self.request.get('newWordToSave')
        key = self.request.get('key')
        logging.info(key + " %% " + newWordToSave)
        self.update(newWordToSave, key)

app = webapp2.WSGIApplication([('/update_counter', HandlerCounterUpdate)])

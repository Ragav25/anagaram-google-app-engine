def createLexicoGraphicalSort(word):
    # wordTrim = word.strip()
    sortedWord = sorted(word)
    lexicoKey = ""
    for letter in sortedWord:
        lexicoKey += letter
    return lexicoKey.lower()

def createWordDict(words):
    wordDict = dict()

    for word in words:
        word = str(word.strip())
        sortedKey = str(createLexicoGraphicalSort(word))
        if sortedKey in wordDict:
            wordDict[sortedKey].append(word)
            continue
        wordDict[sortedKey] = []
        wordDict[sortedKey].append(word)
    return wordDict

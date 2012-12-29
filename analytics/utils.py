from collections import Counter
import nltk

VALKYRIE = 6851810
EVAN = 122601542

def getHaiku(doc):
  italics = doc.xpath('//i')
  if not italics:
    return None
  possible_haiku = italics[0]
  breaks = possible_haiku.xpath('//br')
  if len(breaks) < 2 or len(breaks) > 3:
    return None
  return ''.join(list(possible_haiku.itertext()))

def hasHaiku(doc):
  return bool(getHaiku(doc))

def identifyAuthor(data):
  if data['country'] == 'ca':
    return EVAN
  if hasHaiku(data['content']):
    return VALKYRIE
  return EVAN

def normalizeToken(token):
  token = unicode(token)
  if not token.isalpha():
    return None
  return token.lower()

def extractWords(doc):
  acc = Counter()
  for text in doc.find('body').itertext():
    acc.update(filter(None, map(normalizeToken, nltk.word_tokenize(text))))
  return acc

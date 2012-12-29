import codecs
import json
import sys
import nltk
from collections import Counter
from lxml import etree
from utils import *

sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)
words = {EVAN: Counter(), VALKYRIE: Counter()}
normalizer = createNormalizer(
  allow_nonalpha=False,
  allow_stopwords=False
)
for line in sys.stdin:
  data = json.loads(line)
  data['content'] = etree.HTML(data['content'])
  author = identifyAuthor(data)
  words[author].update(extractWords(data['content'], normalizer))
totals = words[EVAN] + words[VALKYRIE]
E = []
for W, N in totals.iteritems():
  if N < 5 or len(W) < 2:
    continue
  e = words[EVAN][W] / float(N)
  E.append((W, N, e))
E.sort(key=lambda x: (x[2], x[1], x[0]))
for W, N, e in E:
  print '%30s %10d %10.4f %10.4f' % (W, N, e, 1.0 - e)

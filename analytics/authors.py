import codecs
import json
import sys
from collections import Counter
from lxml import etree
from utils import *

sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)
D = []
words = {EVAN: Counter(), VALKYRIE: Counter()}
normalizer = createNormalizer(
  allow_nonalpha=False,
  allow_stopwords=False
)
for line in sys.stdin:
  data = json.loads(line)
  data['content'] = etree.HTML(data['content'])
  author = identifyAuthor(data)
  doc = extractWords(data['content'], normalizer)
  words[author].update(doc)
  D.append(doc)
totals = words[EVAN] + words[VALKYRIE]
idf = IDF(D)
out = []
for W, N in totals.iteritems():
  E = words[EVAN][W]
  out.append({
    'word' : W,
    'count' : {
      'evan' : E,
      'valkyrie' : N - E,
      'total' : N
    },
    'idf': idf[W]
  })

print json.dumps(out)

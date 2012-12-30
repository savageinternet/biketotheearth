import codecs
import json
import math
import sys
from collections import Counter
from lxml import etree
from utils import *

sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)
D = {}
normalizer = createNormalizer(
  allow_nonalpha=False,
  allow_stopwords=True
)
df = Counter()
for line in sys.stdin:
  data = json.loads(line)
  data['content'] = etree.HTML(data['content'])
  words = extractWords(data['content'], normalizer)
  df.update(words.keys())
  D[data['path']] = words
idf = {}
ND = float(len(D))
for W, N in df.iteritems():
  idf[W] = math.log(ND / N, 2)
# see http://nlp.stanford.edu/IR-book/html/htmledition/maximum-tf-normalization-1.html
a = 0.4
for k, d in sorted(D.iteritems()):
  r = []
  M = float(d.most_common(1)[0][1])
  for W, N in d.iteritems():
    tf = a + (1.0 - a) * N / M
    r.append((W, tf * idf[W]))
  r.sort(key=lambda x: (x[1], x[0]), reverse=True)
  print json.dumps({k: r[:25]})

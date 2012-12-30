import codecs
import itertools
import json
import sys
from lxml import etree
from utils import *

sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)
D = {}
normalizer = createNormalizer(
  allow_nonalpha=False,
  allow_stopwords=True
)
for line in sys.stdin:
  data = json.loads(line)
  data['content'] = etree.HTML(data['content'])
  D[data['path']] = extractWords(data['content'], normalizer)
idf = IDF(D.values())
for k, d in sorted(D.iteritems()):
  tf = TF(d, a=0.4)
  r = [(W, tf[W] * idf[W]) for W in tf]
  r.sort(key=lambda x: (x[1], x[0]), reverse=True)
  gs = itertools.groupby(r, key=lambda x: x[1])
  gs = itertools.imap(lambda g: (g[0], [x[0] for x in g[1]]), gs)
  print json.dumps({k: list(itertools.islice(gs, 3))})

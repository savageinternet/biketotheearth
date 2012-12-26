from xhpy.init import register_xhpy_module
register_xhpy_module('post')
from post import render_post, render_index

import codecs
import datetime
import json
import sys
import os
import os.path

def _write_file(html, path):
  filename = os.path.join(root, path)
  dirname = os.path.dirname(filename)
  if not os.path.exists(dirname):
    os.makedirs(dirname)
  with codecs.open(filename, mode='w', encoding='utf-8') as f:
    f.write(html)

sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)
root = sys.argv[1]
posts = [json.loads(line) for line in sys.stdin]
posts.sort(key=lambda post: post['order'])
for i, data in enumerate(posts):
  print u'Generating post: {0}'.format(data['title'])
  data['prev'] = {}
  data['next'] = {}
  if i > 0:
    data['prev'] = posts[i - 1]
  if i < len(posts) - 1:
    data['next'] = posts[i + 1]
  data['date'] = datetime.datetime.strptime(data['date'], '%Y-%m-%dT%H:%M:%S')
  _write_file(render_post(data), data['path'])
_write_file(render_index(posts), 'index.html')

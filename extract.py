from xhpy.init import register_xhpy_module
register_xhpy_module('post')
from post import render_post, render_index

import codecs
import datetime
import json
import sys
import os
import os.path

def _parse_post(line):
  now = datetime.datetime.now()
  post = json.loads(line)
  if post.get('type') != 'post':
    raise ValueError('incorrect JSON blob type')
  date_format = '%Y-%m-%dT%H:%M:%SZ'
  post_date = now.strptime(post['at'], date_format)
  path = os.path.join(
    'posts',
    post_date.strftime('%Y'),
    post_date.strftime('%m'),
    post_date.strftime('%d'),
    '{0}.html'.format(post['permalink'])
  )
  href = '/{0}'.format(path)
  country = post['icon'][-6:-4]
  return {
    'order': post_date.strftime('%Y%m%d'),
    'prev': {},
    'next': {},
    'path': path,
    'href': href,
    'title': post['title'],
    'content': post['content'],
    'author': post['author'],
    'country': country,
  }

def _write_file(html, path):
  filename = os.path.join(root, path)
  dirname = os.path.dirname(filename)
  if not os.path.exists(dirname):
    os.makedirs(dirname)
  with codecs.open(filename, mode='w', encoding='utf-8') as f:
      f.write(html)

sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)

root = sys.argv[1]
posts = []
for line in sys.stdin:
  try:
    posts.append(_parse_post(line))
  except ValueError:
    continue

posts.sort(key=lambda post: post['order'])
for i, data in enumerate(posts):
  if i > 0:
    data['prev'] = posts[i - 1]
  if i < len(posts) - 1:
    data['next'] = posts[i + 1]
  _write_file(render_post(data), data['path'])
_write_file(render_index(posts), 'index.html')

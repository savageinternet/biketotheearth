import codecs
import datetime
import json
import sys
import os.path

def _parse_post(line):
  now = datetime.datetime.now()
  post = json.loads(line)
  if post.get('type') != 'post':
    raise ValueError('incorrect JSON blob type')
  date_format = '%Y-%m-%dT%H:%M:%SZ'
  post_date = now.strptime(post['at'], date_format)
  path = os.path.join(
    'biketotheearth',
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
    'date': post_date.isoformat(),
    'path': path,
    'href': href,
    'title': post['title'],
    'content': post['content'],
    'author': post['author'],
    'country': country,
  }

sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)
for line in sys.stdin:
  try:
    print json.dumps(_parse_post(line))
  except ValueError:
    continue

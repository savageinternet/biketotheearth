from xhpy.pylib import *

country_names = {
  'al': 'Albania',
  'ba': 'Bosnia and Herzegovina',
  'be': 'Belgium',
  'ca': 'Canada',
  'ch': 'Switzerland',
  'de': 'Germany',
  'dk': 'Denmark',
  'es': 'Spain',
  'fr': 'France',
  'gb': 'United Kingdom',
  'gr': 'Greece',
  'hr': 'Croatia',
  'it': 'Italy',
  'ma': 'Morocco',
  'mc': 'Monaco',
  'me': 'Montenegro',
  'nl': 'Holland',
  'pt': 'Portugal',
  'si': 'Slovenia',
  'tr': 'Turkey'
}

class :ui:page(:x:element):
  attribute unicode title
  def render(self):
    return \
    <x:doctype>
      <html>
        <head>
          <meta charset="UTF-8" />
          <title>{self.getAttribute('title')}</title>
          <link href='http://fonts.googleapis.com/css?family=Lusitana:400,700' rel='stylesheet' type='text/css' />
          <link href='/style.css' rel='stylesheet' type='text/css' />
        </head>
        <body>
          {self.getChildren()}
        </body>
      </html>
    </x:doctype>

class :ui:raw(:x:primitive):
  category %flow
  children pcdata
  def stringify(self):
    return u''.join(self.getChildren())

class :ui:index-section(:x:element):
  attribute string country
  def __init__(self, attributes={}, children=[], source=None):
    super(:ui:index-section, self).__init__(attributes, children, source)
    self._posts = <div class="country-posts" />
  def render(self):
    country = self.getAttribute('country')
    return \
    <div class="country" id={country}>
      <div class="country-icon">
        <img src={'/icons/{0}.png'.format(country)} />
      </div>
      <div class="country-name">
        {country_names[country]}
      </div>
      {self._posts}
    </div>
  def addPost(self, data):
    self._posts.appendChild(<ui:index-entry data={data} />)

class :ui:index-entry(:x:element):
  attribute dict data
  def render(self):
    data = self.getAttribute('data')
    return \
    <div class="post">
      <div class="post-date">
        {data['date'].strftime('%Y-%m-%d')}
      </div>
      <div class="post-link">
        <a href={data['href']}>{data['title']}</a>
      </div>
    </div>

def _link(href, text):
  if href is None:
    return <a class="disabled" href="#">{text}</a>
  return <a class="nav" href={href}>{text}</a>

def render_index(posts):
  countries = []
  for data in posts:
    if not countries or data['country'] != countries[-1].getAttribute('country'):
      countries.append(<ui:index-section country={data['country']} />)
    countries[-1].addPost(data)
  page = \
  <ui:page title={u"Bike To The Earth"}>
    <div id="root">
      <div id="title">
        <h1>Bike to the Earth</h1>
      </div>
      <div id="content">
        {countries}
      </div>
    </div>
  </ui:page>
  return unicode(page)

def render_post(data):
  country_href = '/index.html#{0}'.format(data['country'])
  nav = \
  <div class="nav">
    <div class="post-link">
      {_link(data['prev'].get('href'), 'prev')}
    </div>
    <div class="post-link">
      {_link(data['next'].get('href'), 'next')}
    </div>
    <div class="post-link">
      {_link('/index.html', 'index')}
    </div>
  </div>
  post = \
  <div id="root">
    {nav}
    <div id="title">
      <h1>{data['title']}</h1>
    </div>
    <div id="info">
      <div id="country">
        <div class="country-icon">
          <a href={country_href}>
            <img src={'/icons/{0}.png'.format(data['country'])} />
          </a>
        </div>
        <div class="country-name">
          {country_names[data['country']]}
        </div>
      </div>
      <div class="post-date">
        {data['date'].strftime('%Y-%m-%d')}
      </div>
    </div>
    <div id="content">
      <ui:raw>
        {data['content']}
      </ui:raw>
    </div>
    {nav}
  </div>
  page = \
  <ui:page title={data['title']}>
    {post}
  </ui:page>
  return unicode(page)

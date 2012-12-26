from xhpy.pylib import *

class :ui:page(:x:element):
  attribute string title
  def render(self):
    return \
    <x:doctype>
      <html>
        <head>
          <meta charset="UTF-8" />
          <title>{self.getAttribute('title')}</title>
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

def _link(href, text):
  if href is None:
    return <a class="disabled" href="#">{text}</a>
  return <a class="nav" href={href}>{text}</a>

def render_index(datae):
  index = 'Hello World'
  page = \
  <ui:page title="Bike To The Earth">
    {index}
  </ui:page>
  return unicode(page)

def render_post(data):
  post = \
  <div id="root">
    <div id="nav">
      {_link(data['prev'].get('href'), '[prev]')}
      {_link(data['next'].get('href'), '[next]')}
    </div>
    <div id="title">
      <h1>{data['title']}</h1>
    </div>
    <div id="content">
      <ui:raw>
        {data['content']}
      </ui:raw>
    </div>
  </div>
  page = \
  <ui:page title="Bike To The Earth">
    {post}
  </ui:page>
  return unicode(page)

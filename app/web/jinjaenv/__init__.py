"""
  app.web.jinjaenv
  ~~~~~~~~~~~~~~~~

  jinja2 custom filters for pages and email templates.


  :copyright: (c) 2014 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals
# from jinja2 import contextfilter
from jinja2.utils import Markup
from json import dumps
from urllib import quote_plus
# from app.models.shorturl import ShortUrl


__all__ = ['register_filters', 'register_globals']


def register_filters(flaskapp):
  """
  defines and appends jinja context filters to the flask environment.

    :param flaskapp: instance of a `flask.Flask` application.
  """

  def escapejson(value):
    if not isinstance(value, basestring):
      value = unicode(value)
    return Markup(value.replace("<", "&lt;").replace(">", "&gt;"))

  def nl2br(value):
    return value.replace("\n", "<br>\n")

  def urlencode(value):
    return quote_plus(value.encode("utf-8"))

  flaskapp.add_template_filter(dumps, name="dumps")
  flaskapp.add_template_filter(nl2br, name="nl2br")
  flaskapp.add_template_filter(urlencode, name="urlencode")

  # enable jinja2 loop controls extension
  flaskapp.jinja_env.add_extension("jinja2.ext.loopcontrols")


#: config variables to export as jinja globals
EXPORTS = [
  "flask_debug",
  "facebook_app_id",
  "linkedin_app_id",
  "twitter_secret",
  "SERVER_NAME",
]


def register_globals(flaskapp):
  """
    :param flaskapp: instance of a `flask.Flask` application.
  """
  for export in EXPORTS:
    if not hasattr(flaskapp.config, export):
      continue
    flaskapp.jinja_env.globals[export] = getattr(flaskapp.config, export)

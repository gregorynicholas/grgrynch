"""
  app.models
  ~~~~~~~~~~

  data models package.


  :copyright: (c) 2014 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals
from logging import getLogger
from google.appengine.ext import ndb as db


log = getLogger(__name__)
debug = False


def init(flaskapp):
  """
  init the db module.
  """

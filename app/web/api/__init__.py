"""
  app.web.api
  ~~~~~~~~~~~

  rest api that services internal apps.


  :copyright: (c) 2014 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals
from logging import getLogger
from flask.ext import api as flask_api

__all__ = ["API"]


log = getLogger(__name__)
debug = False
_endpoints = flask_api.discover_endpoints(__file__, __package__)

if debug:
  log.info("starting web api: %s", _endpoints)


class API(object):
  """
  initializes the web api interface.
  """

  def __init__(self, flaskapp):
    """
    attaches api endpoints (`flask.Blueprint`s) to the flask application.

      :param flaskapp: instance of a `flask.Flask` app
    """
    [flaskapp.register_blueprint(**_) for _ in _endpoints]
    if debug:
      log.info("registered api blueprints: %s", flaskapp)

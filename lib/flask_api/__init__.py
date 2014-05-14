"""
  flask.ext.api
  ~~~~~~~~~~~~~

  making rest api's in flask applications easier.

  there's no need to be so verbose in building rest api services for internal
  apps. this ain't a fucking book club.


  :copyright: (c) 2014 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals
__import__("pkg_resources").declare_namespace(__name__)

# proxy the key extension modules + objects for convenience.
from flask_wtf import Form
from wtforms import ValidationError, validators, fields
from wtforms.fields import *
from wtforms.validators import *
from wtforms.widgets import *

# proxy object from `flask.ext.api.*`.
from flask.ext.api.endpoints import Endpoints, discover, normalize
from flask.ext.api.exceptions import FieldValidationError

__all__ = [
  "API", "expandjson",
  "Endpoints", "discover", "normalize",
  "Form", "ValidationError", "FieldValidationError", "fields", "validators",
]

DEBUG = False


class API(object):
  """
  initializes the web api interface.
  """

  def __init__(self, flaskapp, endpoint_blueprints):
    """
    attaches api endpoints (`flask.Blueprint`s) to the flask application.

      :param flaskapp: instance of a `flask.Flask` app
      :param endpoint_blueprints: list of `flask.Blueprint` objects
    """
    if DEBUG:
      log.info("registering endpoint blueprints: %s", endpoint_blueprints)

    [flaskapp.register_blueprint(**_) for _ in endpoint_blueprints]


# decorator utils
# --------------------------------------------------------------------------

from json import loads
from functools import wraps
from flask import request


def expandjson(fn):
  """
  method decorator which expands `request.json` as kwargs.
  """
  @wraps(fn)
  def decorated_view(*args, **kwargs):
    if request.json:
      kwargs.update(**request.json)
    elif request.data:
      kwargs.update(**loads(request.data))
    return fn(*args, **kwargs)
  return decorated_view

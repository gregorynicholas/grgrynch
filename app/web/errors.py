"""
  app.web.errors
  ~~~~~~~~~~~~~~

  defines global flask exception handling, and binds error routes + views to
  the flask application.


  :copyright: (c) 2013 by gregorynicholas.

"""
from __future__ import unicode_literals

#@ import error helpers
import traceback
from pprint import pformat

from logging import getLogger
from flask import Response, request
from flask.ext import templated
from app.main import flaskapp

#@ import error handlers
from jinja2 import TemplateNotFound
from google.appengine.api import datastore_errors


log = getLogger(__name__)
log.debug('starting error handler.')
debug = False


@flaskapp.errorhandler(404)
def page_not_found(error=None):
  """
  404 error handler.
  """
  if debug:
    log.warning(
      "page not found: %s %s %s %s %s",
      request.url,
      request.method,
      request.endpoint,
      request.url_rule,
      pformat(request.data))
  return templated.render("404.html")


@flaskapp.errorhandler(500)
def server_error_500(server_error):
  """
  500 error handler. if request is from ajax than return empty page.
  otherwise render template.
  """
  log.exception(traceback.format_exc())
  if request.is_xhr:
    return Response(status=500)
  else:
    return templated.render("500.html")


@flaskapp.errorhandler(TemplateNotFound)
def template_not_found(server_error):
  log.exception(traceback.format_exc())
  return Response("couldn't find the template file.", status=500)


@flaskapp.errorhandler(datastore_errors.BadValueError)
def datastore_bad_value_error(error=None):
  """
  """
  return Response(status=500)


@flaskapp.errorhandler(datastore_errors.BadPropertyError)
def datastore_bad_property_error(error=None):
  """
  """
  return Response(status=500)


@flaskapp.errorhandler(datastore_errors.BadKeyError)
def datastore_bad_key_error(error=None):
  """
  """
  return Response(status=500)


@flaskapp.errorhandler(datastore_errors.Timeout)
def datastore_timeout_error(error=None):
  """
  """
  return Response(status=500)


@flaskapp.errorhandler(datastore_errors.BadFilterError)
def datastore_bad_filter_error(error=None):
  """
  """
  return Response(status=500)


@flaskapp.errorhandler(datastore_errors.BadArgumentError)
def datastore_bad_argument_error(error=None):
  """
  """
  return Response(status=500)


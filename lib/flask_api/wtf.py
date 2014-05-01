"""
  flask.ext.api.wtf
  ~~~~~~~~~~~~~~~~~

  there's no need to be so verbose in building rest api services for internal
  apps. this ain't a fucking book club.


  :license: MIT, see LICENSE for more details.
  :copyright: (c) 2013 by gregorynicholas.
"""
from __future__ import unicode_literals
from flask import request
from flask.exceptions import JSONBadRequest
from functools import wraps
from json import loads
from logging import getLogger
from pprint import pformat
from flask.ext.api.exceptions import FieldValidationError

__all__ = ["form_endpoint"]
logger = getLogger(__name__)


def form_endpoint(form_class, blacklist_methods=["DELETE"]):
  """
    :param form_class:
    :param blacklist_methods:
  """
  def decorated(fn):
    @wraps(fn)
    def wrapped(*args, **kw):
      if request.json or "json" in request.form:
        form = _from_json(form_class)
      else:
        form = form_class(request.form)

      # run the validators..
      if request.method in blacklist_methods:
        raise FieldValidationError(
          {}, message="method not allowed on endpoint.")

      if not form.validate_on_submit():
        # logger.warning("form validation errors: %s", form.errors)
        errors, etype = _format_errors(form.errors)

        # logger.warning("error validating json data: %s, %s", errors, etype)
        raise FieldValidationError(
          errors, message="validation error occurred.")

      return fn(form=form, *args, **kw)
    return wrapped
  return decorated


def _from_json(form_class):
  """
    :returns: instance of a `wtforms.Form` object
  """
  if request.json:
    data = request.json
  else:
    data = loads(request.form["json"])
  if data is None:
    raise JSONBadRequest()
  return form_class.from_json(data)


def _format_errors(errors):
  """
  todo: this code is a bit inelegant. probably just want to override
  the __str__ or __repr__ class of the form.errors object.
  if we easily can't, create a pull request for wtforms to be able to.
  inject an errors class type we can somehow override or subclass
  """
  for k, v in errors.iteritems():
    errors[k] = _serialize_errors(v)
  return pformat(errors), type(errors)


def _serialize_errors(errors):
  if isinstance(errors, str) or isinstance(errors, unicode):
    return errors
  elif isinstance(errors, list):
    return "".join([_serialize_errors(_) for _ in errors])
  else:
    return ""

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

# proxy the key extension modules + objects for convenience..

from flask_wtf import Form
from wtforms import ValidationError, validators, fields
from wtforms.fields import *
from wtforms.validators import *
from wtforms.widgets import *
# loads the `register` method
from flask.ext.api.endpoints import *
from flask.ext.api.exceptions import FieldValidationError

__all__ = [
  "Form", "ValidationError", "FieldValidationError", "fields",
  "validators"
]

"""
  flask.ext.api.exceptions
  ~~~~~~~~~~~~~~~~~~~~~~~~

  exception classes for the api extension.


  :license: MIT, see LICENSE for more details.
  :copyright: (c) 2013 by gregorynicholas.
"""
from __future__ import unicode_literals
from wtforms import ValidationError

__all__ = ["ValidationError", "FieldValidationError"]


class FieldValidationError(ValidationError):
  """
  exception raised when fields don't pass validation.
  """

  def __init__(self, errors, message=None):
    """
    initializes this validation error.

    :param errors: dict representing a mapping of `field.name` to `message`
    :param message: optional string indicating the nature of the error
    """
    if message:
      self.message = message
    self.errors = errors

  def __str__(self):
    return self.__repr__()

  def __repr__(self):
    return "FieldValidationError(errors=%r, message=%r)" % (
      self.errors, self.message)

"""
  paver.ext.virtualenv
  ~~~~~~~~~~~~~~~~~~~~

  paver extension for virtualenv + virtualenvwrapper.


  :copyright: (c) 2014 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from os import environ

__all__ = ["current"]


def current():
  """
  returns the current `$VIRTUAL_ENV` environ variable.
  """
  return environ.get("VIRTUAL_ENV")

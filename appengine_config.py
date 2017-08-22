"""
  grgrynch.appengine_config
  ~~~~~~~~~~~~~~~~~~~~~~~~~


  :copyright: (c) by gregorynicholas.

"""
from __future__ import unicode_literals

import logging
logging.getLogger().setLevel(logging.DEBUG)

from google.appengine.api.logservice import logservice
from textwrap import dedent


from app import include_paths

#@ set the python runtime to 2.7 for the deferred lib wants to default to
#@ webapp25 with webob..
from os import environ
environ.setdefault("APPENGINE_RUNTIME", "python27")


__all__ = [
  'gae_mini_profiler_should_profile_production',
]


def gae_mini_profiler_should_profile_production():
  """
  uncomment the first two lines to enable gae mini profiler on production
  for admin accounts
  """
  # from google.appengine.api import users
  # return users.is_current_user_admin()
  return False

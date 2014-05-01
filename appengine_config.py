"""
  appengine_config
  ~~~~~~~~~~~~~~~~

  :copyright: (c) 2014 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals
from app import include_paths

# set the python runtime to 2.7 for the deferred lib wants to default to
# webapp25 with webob..
import os
os.environ.setdefault("APPENGINE_RUNTIME", "python27")


def gae_mini_profiler_should_profile_production():
  """
  uncomment the first two lines to enable gae mini profiler on production
  for admin accounts
  """
  # from google.appengine.api import users
  # return users.is_current_user_admin()
  return False

"""
  paver.ext.gae
  ~~~~~~~~~~~~~

  paver extension for google app engine sdk's appcfg.py oauth2 token
  management.


  :copyright: (c) 2014 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from paver.easy import task
from paver.ext.utils import sh


__all__ = ['create_oauth2_token', 'refresh_oauth2_token']


@task
def create_oauth2_token():
  """
  create an oauth2 token to use with appcfg.py commands.
  """
  run = "appcfg.py update --skip_sdk_update_check "
  " --noauth_local_webserver "
  " --oauth2 "
  " . "
  sh(run)


@task
def refresh_oauth2_token():
  """
  refreshes an oauth2 token to use with appcfg.py commands.
  """
  run = "appcfg.py update --skip_sdk_update_check "
  " --noauth_local_webserver "
  " --oauth2_refresh_token "
  " --oauth2 "
  " . "
  sh(run)

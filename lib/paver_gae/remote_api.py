"""
  paver.ext.gae.remote_api
  ~~~~~~~~~~~~~~~~~~~~~~~~

  paver extension to connect to the app engine remote_api.


  :copyright: (c) 2014 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals

__all__ = ["connect"]


DEFAULT_APP_PARTITION = "s"
DEFAULT_APP_NAME = "app-name"
DEFAULT_HOST_NAME = "localhost:8888"
DEFAULT_ENDPOINT_PATH = "/_ah/remote_api"
DEFAULT_ENV_ID = "local"


def connect(app_id, path, host, email=None, password=None):
  """
  attaches the datastore service stubs to the `app_id` instance at `host`.
  prompts for user's `email` and `password` on connection if they are `None`.

    :param app_id: required. the app_id of the application to connect to
    :param path: path to remote_api handler. defaults to: "/_ah/remote_api"
    :param host: hostname + port. to connect to google production
      servers, use: <app_id>.appspot.com
    :param email: email address of the google account
    :param password: password for the google account

  if you are connecting to the sdk server running locally, just hit return
  when prompted for email / password.

  NOTE: not tested with two-factor authentication and application specific
  passwords.

  NOTE: https://code.google.com/p/googleappengine/issues/detail?id=3258
  remote_api does not work with Federated Login/OpenID. in order to use with
  a custom domain, you must set the login method to Google Accounts API.
  """
  def _auth():

    def _prompt_input():
      """
      prompts for credentials input.
      """
      from getpass import getpass
      return raw_input("email: "), getpass("password: ")

    def _auto_input(value, *a):
      """
      monkeypatches stdin.
      """
      import sys
      from StringIO import StringIO
      sys.stdin = StringIO(value)
      return value

    if email and password:
      return (_auto_input(email), _auto_input(password))
    elif host == DEFAULT_HOST_NAME:
      return (_auto_input(""), _auto_input(""))
    else:
      return _prompt_input()

  from os import environ
  from google.appengine.tools.appengine_rpc import HttpRpcServer
  from google.appengine.ext.remote_api import remote_api_stub

  remote_api_stub.ConfigureRemoteApi(
      app_id, path, _auth, host, rpc_server_factory=HttpRpcServer)

  # remote_api_stub.MaybeInvokeAuthentication()
  environ["SERVER_SOFTWARE"] = "Development (remote_api)/1"

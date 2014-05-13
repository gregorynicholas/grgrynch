"""
  paver.ext.gae.remote_api
  ~~~~~~~~~~~~~~~~~~~~~~~~

  paver extension to connect to the app engine remote_api.


  :copyright: (c) 2014 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals
from paver.ext import http
from paver.ext.project import opts


__all__ = ["remote"]


DEFAULT_APP_PARTITION = "s"
DEFAULT_APP_NAME = "app-name"
DEFAULT_HOST_NAME = "localhost:8888"
DEFAULT_ENDPOINT_PATH = "/_ah/remote_api"
DEFAULT_ENV_ID = "local"


def _connect(app_id, path, host, email=None, password=None):
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


def _dev_appserver(env_id):
  """
  """
  res = opts.proj.dev_appserver[env_id]
  res.hostname = "{}:{}".format(res.host, res.port)
  return res


def fix_gae_sdk_path():
  """
  hack to load the app engine sdk into the python path.
  """
  import dev_appserver
  dev_appserver.fix_sys_path()


def remote(options):
  """
  attaches the shell to an app engine remote_api endpoint.
  """
  env_id = options.get("env_id", opts.proj.envs.local)
  dev_appserver = _dev_appserver(env_id)

  partition = options.get("partition", dev_appserver.partition)
  app_name = options.get("app_name", DEFAULT_APP_NAME)
  host = options.get("host", DEFAULT_HOST_NAME)
  path = options.get("path", DEFAULT_ENDPOINT_PATH)
  email = options.get("email")
  password = options.get("password")

  if env_id == opts.proj.envs.local:
    http.health_check(host)

    partition = "dev"

  if email is None and host != DEFAULT_HOST_NAME:
    email = opts.proj.email
    password = opts.proj.password

  fix_gae_sdk_path()

  print "connecting to remote_api: ", env_id, host, email, password

  _connect(
    "{}~{}-{}".format(partition, app_name, env_id),
    path=path, host=host, email=email, password=password)

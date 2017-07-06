"""
  app.web.auth
  ~~~~~~~~~~~~

  this module contains the flask specific context of the app objects required
  for security purposes.


  how auth and sessions are implemented:

    KVSession:
      modifies the builtin Flask session, and gives us an interface
      to persist the session data with our own implementation.

    flask_login:
      does the work of authenticating users and setting the session data.


  :copyright: (c) 2013 by gregorynicholas.

"""
from __future__ import unicode_literals
from logging import getLogger
from flask import redirect
from flask.ext import login, login_auth
from flask.ext import login_ndb as login_model
from flask.ext.kvsession import KVSessionExtension

__all__ = ["Auth", "login_manager", "FlaskUser"]

log = getLogger(__name__)
login_manager = login.LoginManager()
# since we're doing this from a module global, we get a flask app context
# error trying to use url_for(), so leave as string for now..
login_manager.login_view = "/login"

# proxy the FlaskUser object
FlaskUser = login_model.FlaskUser


class Auth(object):
  """
  initializes the flask-login extension for an application.
  """
  def __init__(self, flaskapp):
    self.store = login_model.SessionStore()
    self.kvsession = KVSessionExtension(self.store, flaskapp)
    login_manager.session_protection = "strong"
    login_manager.init_app(flaskapp)

    @flaskapp.before_request
    def set_jinja_default_session():
      """
      sets the session data in jinja globals.
      """
      flaskapp.jinja_env.globals["_session"] = FlaskUser.default_session_ctx()


@login_manager.user_loader
def load_user(id):
  """
  """
  return login_model.FlaskUser.find_by_id(id)


@login_manager.unauthorized_handler
def unauthorized():
  log.warn(
    'User is unauthorized.. redirecting to login view: "%s"',
    login_manager.login_view)
  return redirect(login_manager.login_view)


@login.user_logged_in.connect
def on_user_logged_in(app, user):
  """
  signal listener for a user login.

    :param app: Instance of a `Flask` application context.
    :param user: Instance of a `FlaskUser` object.
  """
  # from flask import session
  # ex: set custom session values:
  #   session['company_key'] = user.user.company_key
  log.debug('user logged in: %s, %s', app, user)


@login.user_logged_out.connect
def on_user_logged_out(app, user):
  """
  signal listener for a user logout.

  :param app: Instance of a `Flask` application context.
  :param user: Instance of a `FlaskUser` object.
  """
  log.debug("user logged out: %s, %s", app, user)
  login_auth.clear_flask_session()

"""
  flask.ext.login_auth
  ~~~~~~~~~~~~~~~~~~~~

  glue between a flask app and the flask_login extension.


  :copyright: (c) 2013 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals
from functools import wraps
from flask import abort
from flask import render_template
from flask import session
from flask.ext import login
from itsdangerous import BadSignature


__all__ = [
  "required", "requires_roles", "api_requires_roles",
]


class MissingSessionError(BadSignature):
  """
  error to differentiate from BadSignature of missing key.

  would be cool to move definition to kvsession or have other Exception types
  that are captured by the kvsession plugin.
  """


# proxy the login_required decorator for convenience
required = login.login_required


def _check_roles(roles):
  if len(login.current_user.user.roles) < 1:
    return False
  rv = all(
    login.current_user.user.is_in_role(role) for role in roles)
  return rv


def requires_roles(*roles):
  """
  decorator to ensure a specified role is present in the user's roles for a
  view endpoint.
  """
  def wrapper(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
      if not _check_roles(roles):
        return render_template("login.html")
      return f(*args, **kwargs)
    return wrapped
  return wrapper


def api_requires_roles(*roles):
  """
  decorator to ensure a specified role is present in the user's roles for
  an api endpoint.
  """
  def wrapper(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
      if not _check_roles(roles):
        abort(401)
      return f(*args, **kwargs)
    return wrapped
  return wrapper


def clear_flask_session():
  """
  helper method to ensure the session is cleared in flask.
  """
  sess = session._get_current_object()
  sess["remember"] = "clear"
  sess.destroy()

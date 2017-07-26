"""
  app.web.views
  ~~~~~~~~~~~~~

  this is the base module that will serve the app's views.


  :copyright: (c) 2013 by gregorynicholas.

"""
from __future__ import unicode_literals
from logging import getLogger
from flask import Response
from flask import redirect, session
from flask.ext import login
from flask.ext import login_auth
from flask.ext import templated
from app.main import flaskapp
from app.web import auth
from app.web import jinjaenv
# from app import models
from app.models import user


__all__ = [
  'index_get',
  'favicon',
  'login_get',
  'logout_get',
  'admin_get',
  'test_signin_get',
]


debug = False
log = getLogger(__name__)
if debug:
  log.info("starting views.")


# jinja2 template configuration
jinjaenv.register_filters(flaskapp)
jinjaenv.register_globals(flaskapp)


@flaskapp.route("/", subdomain="<subdomain>", methods=["GET"])
@templated.render("index.html")
def index_get(subdomain=None):
  return {}


@flaskapp.route("/favicon.ico", subdomain="<subdomain>", methods=["GET"])
def favicon(subdomain=None):
  """
  because chrome won't not try to prefetch this, even if it doesn't exist.
  """
  return Response("", 200)


@flaskapp.route("/login", methods=["GET"])
@templated.render("login.html")
def login_get():
  if login.current_user.is_authenticated():
    return redirect("/")
  return {}


@flaskapp.route("/logout", methods=["GET"])
def logout_get():
  login.logout_user()
  sess = session._get_current_object()
  sess["remember"] = "clear"
  sess.regenerate()
  return redirect("/")


@flaskapp.route("/admin", methods=["GET"])
@login_auth.required
@login_auth.requires_roles("admin")
@templated.render("login.html")
def admin_get():
  if login.current_user.is_authenticated():
    return redirect("/")
  return {}


@flaskapp.route("/test_signin", methods=["GET"])
def test_signin_get():
  u = user.User.get_by_id("testing")  # todo
  u.roles = ["admin"]
  flask_user = auth.FlaskUser(u)
  rv = login.login_user(flask_user, remember=True)
  return Response(rv)

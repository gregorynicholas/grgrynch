"""
  flask.ext.templated
  ~~~~~~~~~~~~~~~~~~~

  hoping to make templating easier.


  :copyright: (c) 2014 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals
from functools import wraps
from json import dumps
from flask import request
from flask import render_template

__all__ = ['render', 'render_session_template', 'render_template']


def render(template=None):
  def decorator(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
      tname = template
      if tname is None:
        tname = request.endpoint.replace(".", "/") + ".html"
      ctx = f(*args, **kwargs)
      if ctx is None:
        ctx = {}
      elif not isinstance(ctx, dict):
        return ctx
      return render_template(tname, **ctx)
    return wrapped
  return decorator


try:
  # if the login extension exists..
  from flask.ext import login

  def render_session_template(flaskapp, template, **kw):
    """
      :param flaskapp: todo: replace with get current app call
      :param template: string template name
    """
    if login.current_user.is_authenticated():
      _session = login.current_user.session_dict()
    else:
      _session = flaskapp.jinja_env.globals["_session"]
    flaskapp.jinja_env.globals["_session"] = dumps(_session)
    return render_template(template, **kw)

except ImportError:
  # otherwise, continue gracefully..
  def render_session_template(flaskapp, template, **kw):
    return render_template(template, **kw)

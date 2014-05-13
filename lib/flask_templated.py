"""
  flask.ext.templated
  ~~~~~~~~~~~~~~~~~~~

  hoping to make templating easier.


  :copyright: (c) 2014 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals
from functools import wraps
from flask import request
from flask import render_template


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

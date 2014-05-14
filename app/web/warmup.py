"""
  app.web.warmup
  ~~~~~~~~~~~~~~

  handles app engine built-in warmup requests.


  :copyright: (c) 2014 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals
from logging import getLogger
from flask import Response
from app.main import flaskapp

log = getLogger(__name__)


@flaskapp.route("/_ah/start", subdomain="<subdomain>", methods=["GET"])
@flaskapp.route("/_ah/warmup", subdomain="<subdomain>", methods=["GET"])
def warmup_get(subdomain=None):
  """
  handles an appengine instance startup warmup request.

  this is needed to when using the app engine mapreduce lib.
  """
  log.debug('warmup request..')
  return Response("", 200)

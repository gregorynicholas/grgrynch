"""
  flask.ext.taskqueue
  ~~~~~~~~~~~~~~~~~~~

  wrapper around the app engine taskqueue api, which gives the ability to run
  tasks immediately.

  this is to work around the fact that when testing, the taskqueue service api
  is stubbed and task queues don"t run (and since testing asynchronous stuff is
  a giant pain anyway).


  :copyright: (c) by gregorynicholas.
  
"""
from __future__ import unicode_literals
import datetime
from json import dumps, loads
from functools import wraps
from flask import request
from google.appengine.api import taskqueue
from urlparse import urlparse

__all__ = [
  "add", "run", "json_task", "test_client",
]


# global test client which should be set in setUp and set to None in tearDown.
# for test cases which need to test the result of running tasks.
test_client = None


def add(url, data=None, *args, **kwargs):
  """
    :param url: parsed, and forced to a relative path for gae
    :param data: optional dict that will be passed along as json
  """
  url = urlparse(url)[2]
  if test_client:
    return run(url, data=data, *args, **kwargs)
  else:
    if data:
      kwargs["data"] = {"json": dumps(_json_safe(data))}
    return taskqueue.add(url=url, *args, **kwargs)


def run(url, data=None, *args, **kwargs):
  """
  runs a task syncronously, not through the app engine task queue api.
  """
  from tests.test_utils import TestUtils
  # deliberately ignores return value to match taskqueue behavior
  if data is not None:
    TestUtils.post_url(test_client, url, _json_safe(data))
  else:
    test_client.post(url, data=kwargs["payload"])


def _json_safe(value):
  for k, v in value.iteritems():
    if isinstance(v, datetime.datetime):
      value[k] = v.strftime("%Y-%m-%d %H:%M:%S")
  return value


def json_task(taskhandler):
  """
  flask route decorator, reads json encoded tasks arguments from
  request.form["json"], decodes them, and put them in kwargs. this allows for
  not using forms to transmit post data between tasks.
  """
  @wraps(taskhandler)
  def wrapped(*args, **kwargs):
    if "json" in request.form:
      data = loads(request.form["json"])
    elif request.json:
      data = request.json["data"]
    for (k, v) in data.viewitems():
      kwargs[k] = v

    return taskhandler(*args, **kwargs)
  return wrapped

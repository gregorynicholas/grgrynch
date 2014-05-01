"""
  paver.ext.http
  ~~~~~~~~~~~~~~

  paver extension for working with http.


  :copyright: (c) 2014 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
import urllib2
import time
from paver.ext.utils import sh

__all__ = ["wget", "ping", "PingError"]


class PingError(ValueError):
  """
  """


def ping(url, retries=15, sleep=2):
  """
  makes http requests to a url until it responds with a 200-299 status.

    :param url: string url to ping
    :param retries: maximum number of retries to attempt
    :param sleep: number of seconds to sleep between retries
  """
  for _ in range(retries):
    try:
      urllib2.urlopen(url)
      break
    except urllib2.URLError:
      print "can't connect to local appengine server.. will retry.."
    time.sleep(sleep)
  else:
    raise PingError("""
  maximum number of retries reached
  """)


def wget(src, dest, callback=None):
  """
    :param src: instance of a `paver.easy.path` object.
    :param dest: instance of a `paver.easy.path` object.
    :param callback (todo): move the DL to non-blocking, and invoke
      callback function on done.
  """
  return sh("wget {}", src, err=True, cwd=dest)


def curl(src, dest, callback=None):
  """
    :param src: instance of a `paver.easy.path` object.
    :param dest: instance of a `paver.easy.path` object.
    :param callback (todo): move the DL to non-blocking, and invoke
      callback function on done.
  """
  # todo

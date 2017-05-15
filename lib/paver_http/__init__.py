"""
  paver.ext.http
  ~~~~~~~~~~~~~~

  paver extension for working with http.


  :copyright: (c) 2014 by gregorynicholas.

"""
import urllib2
import time
from paver.ext.utils import sh

__all__ = [
  "wget",
  "ping",
  "health_check",
  "PingError",
]


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


def health_check(url, retries=15, sleep=2):
  """
  pings a url. used as a health check.

    :param url: full hostname address of the url.
    :param retries: number of pings to attempt.
    :param sleep: number of seconds to wait between pings.
  """
  ping(url, retries=retries, sleep=sleep)

  print "connected to {}".format(url)


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
  # <TODO>

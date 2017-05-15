"""
  paver.ext.supervisor
  ~~~~~~~~~~~~~~~~~~~~

  paver extension for supervisord.


  :copyright: (c) 2014 by gregorynicholas.

"""
from __future__ import unicode_literals
from time import sleep
from paver.ext.utils import sh


__all__ = ["start", "stop"]


class RunProcessFailure(ValueError):
  """
  """


class ProcessNotFound(ValueError):
  """
  """


class ProcessNotRunning(ValueError):
  """
  """


def start():
  """
  starts supervisord.
  """
  s = "program is already listening on a port that one of our HTTP servers"
  res = sh("supervisord -c supervisord.conf", capture=True)
  if s in res:
    print 'supervisord already started..'
  sleep(1)  # wait for supervisor to startup..
  return res


def shutdown():
  """
  stops supervisord.
  """
  res = sh("supervisorctl -c supervisord.conf shutdown", capture=True)
  if 'ERROR' in res:
    print 'error stopping supervisord:', res
  sleep(1)  # wait for supervisor to shutdown..
  return res


def run(program, *a, **kw):
  """
  capture the process id, so we can manage by saving the process.

    :param program: supervisor program to run.
  """
  error = kw.pop('error', True)
  capture = kw.pop('capture', True)
  return sh(
    "supervisorctl start {}".format(program),
    error=error,
    capture=capture,
    *a, **kw)


def stop(program, *args, **kw):
  """
  stop a program.
  """
  error = kw.pop('error', True)
  capture = kw.pop('capture', True)
  return sh(
    "supervisorctl stop {}".format(program),
    error=error,
    capture=capture,
    *args, **kw)

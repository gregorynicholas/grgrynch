"""
  paver.ext.supervisor
  ~~~~~~~~~~~~~~~~~~~~

  paver extension for supervisord.


  :copyright: (c) 2014 by gregorynicholas.

"""
from __future__ import unicode_literals
from time import sleep
from jinja2 import Environment
from jinja2.loaders import DictLoader
from paver.easy import Bunch, options as opts
from paver.ext.utils import sh
from paver.ext.gae import descriptor


__all__ = [
  "render_config",
  "reload_config",
  "start",
  "shutdown",
  "run",
  "stop",
]


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
  res = sh("supervisord -c supervisord.conf", capture=True)

  _s = "program is already listening on a port that one of our HTTP servers"
  if _s in res:
    print('[ supervisord:warning ] already started..')

  sleep(1)  # wait for supervisor to startup..
  return res


def shutdown():
  """
  stops supervisord.
  """
  res = sh("supervisorctl -c supervisord.conf shutdown", capture=True)

  if 'ERROR' in res.upper():
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


def render_config(context):
  """
  """
  template = (opts.proj.dirs.buildconfig / 'supervisord.template.conf').text()

  #@ render the supervisor config template..
  print('[ supervisorctl ] rendering config template..')

  jinjaenv = Environment(loader=DictLoader(
    {'supervisord.template.conf': str(template)}
  ))
  descriptor.render_jinja_templates(jinjaenv, context, dest=opts.proj.dirs.base)


def reload_config():
  """
  """
  _sh = "supervisorctl reload -c supervisord.conf"
  out = sh(_sh, error=False, capture=True)

  if 'Restarted supervisord' in out:
    print('[ supervisorctl ] config reloaded..')

  return out

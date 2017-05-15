"""
  paver.ext.mongodb
  ~~~~~~~~~~~~~~~~~

  paver extension to automate mongodb.


  :copyright: (c) 2013 by gregorynicholas.

"""
from __future__ import unicode_literals
from paver.easy import options as opts
from paver.easy import task, BuildFailure
from paver.ext import daemon
from paver.ext.utils import sh


__all__ = [
  'run',
  'stop',
]


@task
def run():
  """
  starts a local mongod server.
  """
  if daemon.is_pid_running(opts.proj.dirs.mongodb.pid):
    BuildFailure("mongodb is already running..")
  daemon.nohup(
    "mongod ",
    pid=opts.proj.dirs.mongodb.pid,
    append=True,
    cwd=opts.proj.dirs.base)


@task
def stop():
  """
  stops a local mongod server.
  """
  daemon.kill(opts.proj.dirs.mongodb.pid)

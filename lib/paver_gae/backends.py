"""
  paver.ext.gae.backends
  ~~~~~~~~~~~~~~~~~~~~~~

  paver extension to work with app-engine backend services.


  :copyright: (c) 2014 by gregorynicholas.

"""
from __future__ import unicode_literals
from paver.easy import options as opts
from paver.easy import task, call_task
from paver.ext.gae import descriptor
from paver.ext.gae.appcfg import appcfg
# from paver.ext import utils


__all__ = [
  "backends",
  "get_backends"
  "backends_deploy",
  "backends_rollback",
]


def get_backends():
  """
    :returns: list of Bunch objects for each descriptor config.
  """
  return descriptor.backends(opts.proj.dirs.dist)


@task
def backends():
  '''
  prints backends defined in the gae descriptors.
  '''
  #: <TODO> yaml dump..?
  print get_backends()


@task
def backends_rollback(backends=None):
  """
  performs a rollback operation for all backend definitions.
  """
  if backends is None:
    backends = get_backends()
  # todo: can we run these in parallel?
  for backend in backends:
    appcfg(
      "backends {dir} rollback ".format(
        dir=opts.proj.dirs.dist), backend_name=backend.name)


@task
def backends_deploy():
  """
  runs the comamnd:
    appcfg.py [options] backends <directory> update [<backend>]
  """
  backends = get_backends()
  # call rolleback for all backends..  it was often experienced to have caused
  # break the build when trying to deploy the backends, with the error message
  # returning to perform a rollback operation first.  (me thinks google doesn't
  # put the same deployment reliability emphasis on the backends)
  call_task("backends_rollback", backends)
  for backend in backends:
    appcfg(
      "backends {dir} update ".format(
        dir=opts.proj.dirs.dist), backend_name=backend.name)
  print("---> backends_deploy success\n")

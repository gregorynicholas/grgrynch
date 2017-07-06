"""
  paver.ext.virtualenv
  ~~~~~~~~~~~~~~~~~~~~

  paver extension for python virtualenv.


  :copyright: (c) by gregorynicholas.

"""
from os import environ
from paver.easy import task
from paver.easy import options as opts
from paver.ext import utils


__all__ = [
  "current",
  "reset_virtualenv",
]


def current():
  """
  returns the current `$VIRTUAL_ENV` environ variable.
  """
  return environ.get("VIRTUAL_ENV")


@task
def reset_virtualenv():
  """
  rebuilds the python virtualenv for the project.
  """
  utils.rm(opts.proj.dirs.venv)
  utils.sh("mkvirtualenv {}", opts.proj.virtualenv_id)

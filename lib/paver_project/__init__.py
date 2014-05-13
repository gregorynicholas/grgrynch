"""
  paver.ext.project
  ~~~~~~~~~~~~~~~~~

  load project settings.


  :copyright: (c) 2014 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals
from paver.ext import virtualenv
from paver.ext.utils import yaml_load, rbunch, rpath
from paver.easy import Bunch
from paver.easy import path
from paver.easy import options


__all__ = ["proj", "opts"]


def load(config_path):
  """
  initialize the project config from yaml definition.

    :param config_path:
  """
  p = yaml_load(config_path)["project"]
  rv = Bunch(**rbunch(p))

  # set the project dirs as `path` objects
  rv.dirs = Bunch(**rpath(p["dirs"]))

  # manually add the the `virtualenv` path object
  rv.dirs.venv = path(virtualenv.current())
  rv.pip_config = path(rv.dirs.buildconfig / rv.pip_config)

  return rv


proj = load("build/project.yaml")

# set the `proj` var in the paver environment options
options(proj=proj)

# export the options variable
opts = options

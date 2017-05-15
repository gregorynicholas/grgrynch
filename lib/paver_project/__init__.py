"""
  paver.ext.project
  ~~~~~~~~~~~~~~~~~

  load project settings.


  :copyright: (c) by gregorynicholas.

"""
from __future__ import unicode_literals
from paver.ext import virtualenv
from paver.ext.utils import yaml_load
from paver.ext.utils import rbunch
from paver.ext.utils import rpath
from paver.easy import Bunch
from paver.easy import path as pth
from paver.easy import options as opts


__all__ = ["proj", "opts"]


def load(config_path):
  """
  initialize the project config from yaml definition.

    :param config_path: string path.
  """
  config_path = pth(config_path)

  if not config_path.exists():
    raise ValueError('project configuration file not found: {}'.format(config_path))

  p = yaml_load(config_path)["project"]
  rv = Bunch(**rbunch(p))

  #: set the project dirs as `path` objects
  rv.dirs = Bunch(**rpath(p["dirs"]))

  #: manually add the the `virtualenv` path object
  rv.dirs.venv = pth(virtualenv.current())

  #: pre-pend the pip_dependencies.yaml file..
  rv.pip_dependencies = pth(rv.dirs.buildconfig / rv.pip_dependencies)

  return rv


#: shorthanded to `proj`
proj = load("build/project.yaml")

#: set the `proj` var in the paver environment options
opts(proj=proj)

"""
  paver.ext.pip
  ~~~~~~~~~~~~~

  paver extension for python pip.


  :copyright: (c) 2014 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals
from paver.easy import options as opts
from paver.ext.utils import sh
from pkg_resources import Distribution


__all__ = ["get_installed_top_level_files"]


def install(packages, group='runtime'):
  """
  installs the specified python package(s).

    :param packages: dict, list, or string name of package to install.
  """

  if isinstance(packages, dict):
    packages = packages[group]
  elif isinstance(packages, str):
    packages = [packages]

  return sh(
    "pip install --download-cache={cache} -q {packages}",
    packages=" ".join(packages),
    cache=opts.proj.dirs.base / ".pip",
    cwd=opts.proj.dirs.base)


def _normalize(name):
  """
  normalizes the file name of a package.
  """
  return name.split("==")[0].split("#egg=")[-1].replace("-", "_").lower()


def get_installed_top_level_files(packages):
  """
    :param packages:
    :returns:
  """
  venvlib = opts.proj.dirs.venv / "lib/python2.7/site-packages"
  runtimes = [_normalize(_) for _ in packages]
  rv = []
  for egg in venvlib.walkdirs("*.egg-info"):
    dist = Distribution.from_location(egg, basename=str(egg.name))
    if _normalize(dist.project_name) not in runtimes:
      continue
    toplevels = (egg / "top_level.txt").text().split("\n")
    toplevels.remove("")
    for tlevel in [_ for _ in toplevels if _ != "tests"]:
      if not (venvlib / tlevel).isdir():
        tlevel += ".py"
      else:
        pass  # todo: try to append an __init__ file
      rv.append(venvlib / tlevel)
  return rv

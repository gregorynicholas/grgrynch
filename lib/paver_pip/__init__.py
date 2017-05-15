"""
  paver.ext.pip
  ~~~~~~~~~~~~~

  paver extension for working with python setuptools + pip.


  :copyright: (c) 2014 by gregorynicholas.

"""
from __future__ import unicode_literals
from pprint import pformat
from paver.easy import options as opts
from paver.ext.utils import sh
from pkg_resources import Distribution  # <TODO> add as alias to utils


__all__ = [
  "install",
  "get_installed_top_level_files",
]


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
    "pip install --disable-pip-version-check {packages}",
    packages=" ".join(packages),
    cache=opts.proj.dirs.base / ".pip",
    cwd=opts.proj.dirs.base)


def _normalize(name):
  """
  normalizes the file name of a package.
  """
  #: <TODO> check for "egg" vs "dist"
  return name.split("==")[0].split("#egg=")[-1].replace("-", "_").lower()


def get_normalized_package_names(packages):
  """
    :param packages:
    :returns:
  """
  return [_normalize(_) for _ in packages]


def filter_top_level_runtime_deps(toplevels):
  rv = []

  for top in toplevels:
    if (top == "tests") or (top.startswith("tests") or top.endswith("tests")):
      continue

    rv.append(top)
  return rv


def get_installed_top_level_files(packages):
  """
    :param packages:
    :returns:
  """
  venvlib = opts.proj.dirs.venv / "lib/python2.7/site-packages"
  runtimes = get_normalized_package_names(packages)
  rv = []
  for egg in venvlib.walkdirs("*.egg-info"):
    dist = Distribution.from_location(egg, basename=str(egg.name))

    if _normalize(dist.project_name) not in runtimes:
      continue

    toplevels = (egg / "top_level.txt").text().split("\n")
    toplevels.remove("")

    for tlevel in [_ for _ in toplevels if _ != "tests"]:
      _path = venvlib / tlevel

      if not _path.isdir():
        tlevel += ".py"

      else:
        pass

      rv.append(venvlib / tlevel)

  return rv

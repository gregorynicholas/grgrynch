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

  log = 'pip-install.log'

  return sh(
    "pip install --disable-pip-version-check --log {log} {packages}",
    packages=" ".join(packages),
    log=log,
    cwd=opts.proj.dirs.base)


def _normalize(name):
  """
  normalizes the file name of a package.
  """
  #: <TODO> check for "egg" vs "dist"
  _sep = '=='

  if '>=' in name:
    _sep = '>='

  elif '<=' in name:
    _sep = '<='

  return name.split(_sep)[0].split("#egg=")[-1].replace("-", "_").lower()


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
  venvpkgs = opts.proj.dirs.venv / "lib/python2.7/site-packages"
  runtimes = get_normalized_package_names(packages)

  print('''
  site-packages: {}
  runtimes: {}
  '''.format(venvpkgs, pformat(runtimes)))

  rv = []
  _dirs = [venvpkgs.walkdirs("*.egg-info"), venvpkgs.walkdirs("*.dist-info")]
  _eggs = []

  for _gen in _dirs:
    for _dir in _gen:
      _eggs.append(_dir)

  print('_eggs: {}'.format(pformat(_eggs)))

  for _egg in _eggs:
    print('_egg: {}'.format(_egg))

    dist = Distribution.from_location(_egg, basename=str(_egg.name))
    _name = _normalize(dist.project_name)

    print('_name: {}'.format(_name))

    if _name not in runtimes:
      continue

    toplevels = (_egg / "top_level.txt").text().split("\n")
    toplevels.remove("")

    for tlevel in [_ for _ in toplevels if _ != "tests"]:
      _path = venvpkgs / tlevel

      if not _path.isdir():
        tlevel += ".py"

      else:
        pass

      rv.append(venvpkgs / tlevel)

  return rv

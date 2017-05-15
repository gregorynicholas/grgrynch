"""
  paver.ext.utils
  ~~~~~~~~~~~~~~~

  hoping to make life easier for every engineer.


  :copyright: (c) by gregorynicholas.

"""
from __future__ import unicode_literals
import os
import codecs
import tempfile
import yaml
from paver.easy import Bunch
from paver.easy import path
from paver.easy import sh2 as sh


__all__ = [
  "parse_cmd_flags",
  "pop_sh_kwargs",
  "to_flags",
  "sh",
  "sym",
  "rm",
  "file_to_utf8",
  "yaml_load",
  "rbunch",
  "rpath",
]


def parse_cmd_flags(args=None, flags=None):
  """
  returns a string that can be used for command line flags.
  """
  res = ""

  if flags:
    res = "".join(
      [" --%s " % _ for _ in flags])

  if args:
    res += "".join(
      [" --%s=%s " % (_, args[_]) for _ in args])

  return res


def pop_sh_kwargs(kwargs):
  """
  returns global command options popped to a list with defaults.
  """
  std_kwargs = dict(
    capture=True,
    error=False,
    quiet=False,
  )
  return [kwargs.pop(kwarg, val) for kwarg, val in std_kwargs.iteritems()]


def to_flags(d):
  """
  same as `parse_cmd_flags`
  """
  rv = []
  for k, v in d.iteritems():
    if v is (None or True):
      rv.append(" --{} ".format(k))
    else:
      rv.append(" --{}={} ".format(k, v))
  return "".join(rv)


def rm(*paths):
  """
  fucking sick of how tedious it is to make a simple `rm` call.
  """
  for p in paths:
    sh("rm -rf {}", p)
  return paths


def file_to_utf8(file_path, replacements):
  """
  replaces contents of a file with utf-8 encoded text.

    :param file_path: instance of a `paver.easy.path` object.
    :param replacements:
  """
  return _replace_in_file(file_path, replacements)


def _replace_in_file(file_path, replacements):
  """
  replaces contents of a file with utf-8 encoded text.

    :param file_path: instance of a `paver.easy.path` object.
    :param replacements:
  """

  def _replace(_line, _orig, _replace):
    return _line.replace(_orig, _replace).encode("utf-8")

  tmp, tmp_path = tempfile.mkstemp()
  with open(tmp_path, "wb") as f1:
    with codecs.open(file_path, "r", "utf-8") as f2:
      for line in f2:
        for (orig, new) in replacements.iteritems():
          f1.write(_replace(line, orig, new))
  os.close(tmp)
  rm(file_path)
  return path(tmp_path).move(file_path)


def sym(src, dest):
  """
  symlinks a path, overwriting if the destination already exists.

    :param src: instance of a `paver.easy.path` object.
    :param dest: instance of a `paver.easy.path` object.
  """

  # if dest.is_link():
  #   sh('unlink {}'.format(dest))

  rm(dest)  #: <TODO> use `unlink`..
  return src.symlink(dest)


def yaml_load(path):
  """
    :param path: instance of a `paver.easy.path` object.
  """
  if not path.exists():
    raise ValueError('yaml file not found: {}'.format(path))

  with open(path, "r") as f:
    rv = yaml.safe_load(f)
  return rv


# paver `bunch`ng helpers..
# -------------------------------------------------------------------------

def rpath(d):
  """
  recursively Bunch a dict, converting string values to `paver.easy.path`.

    :param d: instance of a dict.
  """
  rv = {}
  if isinstance(d, dict):
    for k, v in d.iteritems():
      if isinstance(v, dict):
        rv[k] = Bunch(**rpath(v))
      elif isinstance(v, basestring):
        if v.startswith("~"):
          v = os.path.expanduser(v)
        rv[k] = path(v)
  return rv


def rbunch(d):
  """
  recursively Bunch dict values.

    :param d: instance of a dict.
  """
  rv = {}
  if isinstance(d, dict):
    for k, v in d.iteritems():
      rv[k] = Bunch(**rbunch(v)) if isinstance(v, dict) else v
  return rv

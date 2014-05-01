"""
  paver.ext.archives
  ~~~~~~~~~~~~~~~~~~

  paver extension for working with archive files.


  :copyright: (c) 2014 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from shutil import make_archive
from paver.easy import BuildFailure
from paver.ext.utils import sh


__all__ = ["archive", "extract"]


class InvalidArchiveFile(BuildFailure):
  """
  """


def archive(src, dest, format="zip"):
  """
  create an archive file (eg. zip or tar).

    :param format: "zip", "tar", "bztar" or "gztar"
  """
  make_archive(
    base_name=dest.name,
    format=format,
    root_dir=dest.abspath(),
    base_dir=src)
  return src


def extract(archive, dest):
  """
  extracts an archive, any archive.

    :param archive: instance of a `paver.easy.path` object.
    :param dest: instance of a `paver.easy.path` object.
  """
  if archive.endswith(".zip"):
    run = "unzip {archive}"
  elif archive.endswith(".tar"):
    run = "tar xvzf {archive}"
  elif archive.endswith(".tar.gz"):
    run = "tar -zxvf {archive}"
  else:
    raise InvalidArchiveFile("""
  unable to extract archive, unsupported format:
    {}
  """.format(archive))
  return sh(run, archive=archive, cwd=dest)

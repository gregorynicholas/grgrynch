"""
  paver.ext.archives
  ~~~~~~~~~~~~~~~~~~

  paver extension for working with archive files.


  :copyright: (c) 2014 by gregorynicholas.

"""
from shutil import make_archive
from paver.easy import BuildFailure
from paver.ext.utils import sh


__all__ = [
  "InvalidArchiveFile",
  "archive",
  "extract",
]


class InvalidArchiveFile(BuildFailure):
  """
  """


def archive(src, dest, format="zip"):
  """
  creates an archive file (eg. zip or tar).

    :param src: source path to compress
    :param dest: path to write compressed archive to
    :param format: "zip", "tar", "bztar" or "gztar"
  """
  make_archive(
    base_name=dest.name,
    format=format,
    root_dir=dest.abspath(),
    base_dir=src)

  # return src
  return dest


def extract(archive, dest):
  """
  extracts an archive, [most] any archive.

    :param archive: instance of `paver.easy.path`, path to archive to extract.
    :param dest: instance of `paver.easy.path`, root dir to extract to.
  """
  if archive.endswith(".zip"):
    run = "unzip {archive}"

  elif archive.endswith(".tar"):
    run = "tar -xvzf {archive}"

  elif archive.endswith(".tar.gz"):
    run = "tar -xvf {archive}"

  else:
    raise InvalidArchiveFile("""
  unable to extract archive, unsupported format:
    {}
  """.format(archive))

  return sh(run, archive=archive, cwd=dest)

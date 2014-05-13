"""
  paver.ext.client
  ~~~~~~~~~~~~~~~~

  paver extension for building the app client.


  :copyright: (c) 2014 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from hashlib import sha256
from itertools import chain
from paver.ext.project import opts
from paver.ext.utils import file_to_utf8


__all__ = [
  'copy_page_templates', 'copy_client_build_to_static', 'tag_static_build',
]


def copy_page_templates(root):
  """
  copies html page templates from the client build dir to the app
  web templates dir.

  from ./client/build/dist/*.html to ./app/web/templates

    :param root: instance of a `paver.easy.path` object
  """
  dest = root / opts.proj.dirs.app_web_templates
  dest.makedirs()

  templates = opts.proj.dirs.client_build_dist.walkfiles("*.html")

  for template in templates:
    template.copy2(dest)


def copy_client_build_to_static(root):
  """
  copies client build output to the app web static dir.

  from ./client/build/dist/*.[!html] to ./app/web/static

    :param root: instance of a `paver.easy.path` object
  """
  dest = root / opts.proj.dirs.app_web_static
  dest.rmtree()
  opts.proj.dirs.client_build_dist.cp(
    dest, ignore=("*.html", "test*"))


def tag_static_build(root):
  """
  used to cache bust static files. hashes the contents of each static file,
  and appends the hash string to the end of the filenames.

    :param root: instance of a `paver.easy.path` object
  """
  templates_dir = root / opts.proj.dirs.app_web_templates
  static_dir = root / opts.proj.dirs.app_web_static

  replace_map = {}
  static_files = chain(
    static_dir.walkfiles("*.js"), static_dir.walkfiles("*.css"))

  for f in static_files:
    hash_str = sha256(open(f, "rb").read()).hexdigest()
    new_name = "{}_{}{}".format(f.namebase, hash_str, f.ext)
    replace_map["/" + f.name] = "/" + new_name
    f.rename(f.parent / new_name)

  for f in templates_dir.walkfiles("*.html"):
    file_to_utf8(f, replace_map)

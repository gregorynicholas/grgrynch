"""
  paver.ext.gae.sdk
  ~~~~~~~~~~~~~~~~~

  paver extension for working with google-cloud app-engine sdk.


  :copyright: (c) 2014 by gregorynicholas.

"""
from __future__ import unicode_literals
from paver.easy import task
from paver.easy import BuildFailure
from paver.easy import path
from paver.easy import options as opts
from paver.ext import archives
from paver.ext import http
from paver.ext import pip
from paver.ext import virtualenv
from paver.ext.utils import rm
from paver.ext.utils import sh


__all__ = [
  'install_sdk',
  'install_runtime_libs',
  'install_mapreduce_lib',
]


@task
def install_sdk():
  """
  installs the app-engine sdk, to the virtualenv root dir.
  """
  #: <TODO> add a "force" option to override cache
  archive = path(opts.gae.dev_appserver.ver + ".zip")
  if not (opts.proj.dirs.venv / archive).exists():
    http.wget(
      '--no-config ' + opts.gae.dev_appserver.src + archive.name, opts.proj.dirs.venv)

  if opts.gae.sdk.root.exists():
    #: <TODO> add interactive confirm ..?
    rm(opts.gae.sdk.root)

  #: <TODO> replaces with archives call.
  sh(
    """
    unzip -d ./ -oq {archive} && mv ./google_appengine {sdk_root}
    """,
    archive=archive.name,
    sdk_root=opts.gae.sdk.root,
    cwd=opts.proj.dirs.venv,
    err=True)

  if not opts.gae.sdk.root.exists():
    raise BuildFailure("shit didn't download + extract the lib properly.")

  print('opts.gae.sdk.root: {}'.format(opts.gae.sdk.root))

  _write_venv_pth()
  _write_post_activate_v2()


def _write_venv_pth():
  '''
  integrates the app-engine sdk with virtualenv ..
  '''
  venv_pth_file = opts.gae.dev_appserver.ver + ".pth"
  site_packages = opts.proj.dirs.venv / "lib/python2.7/site-packages"
  venv_pth_file = site_packages / venv_pth_file

  venv_pth_file.write_lines([
    opts.gae.sdk.root.abspath(),
    "import dev_appserver",
    "dev_appserver.fix_sys_path()"])


def _write_post_activate_v2():
  '''
  use virtualenv hooks to add gae's sdk to the exec path
  '''
  activate = opts.proj.dirs.base / ".env"
  activate.write_lines([
    '',
    'echo "exec path adjusted for {}.." '.format(opts.gae.dev_appserver.ver),
    'export PATH="{}":"$PATH" '.format(opts.gae.sdk.root),
    '',
  ], append=True)


def _write_post_activate_v1():
  '''
  use virtualenv hooks to add gae's sdk to the exec path
  '''
  postactivate = opts.proj.dirs.venv / "bin/postactivate"
  postactivate.write_lines([
    '#!/usr/bin/env bash',
    'echo "exec path adjusted for {}.." '.format(opts.gae.dev_appserver.ver),
    'export PATH="{}":"$PATH" '.format(opts.gae.sdk.root),
    '',
  ], append=True)


@task
def install_mapreduce_lib():
  """
  installs app-engine mapreduce library.
  (http://github.com/gregorynicholas/appengine-mapreduce)
  """
  if (opts.proj.dirs.lib / "mapreduce.zip").exists():
    return
  print "installing app engine mapreduce libraries.."

  rm(opts.proj.dirs.lib / "appengine-mapreduce-master")
  rm(opts.proj.dirs.lib / "mapreduce")
  rm(opts.proj.dirs.lib / "appengine_pipeline")

  if not (opts.proj.dirs.lib / "master.tar.gz").exists():
    http.wget("https://github.com/gregorynicholas/appengine-mapreduce/"
              "archive/master.tar.gz", opts.proj.dirs.lib)

  archives.extract("master.tar.gz", opts.proj.dirs.lib)

  (opts.proj.dirs.lib / "appengine-mapreduce-master/mapreduce"
   ).move(opts.proj.dirs.lib)

  (opts.proj.dirs.lib / "appengine-mapreduce-master/appengine_pipeline"
   ).move(opts.proj.dirs.lib)

  rm(opts.proj.dirs.lib / "appengine-mapreduce-master")


def install_runtime_libs(packages, dest):
  """
  since app engine doesn't allow for fucking pip installs, we have to symlink
  the libs to a local project directory. we could do 2 separate pip installs,
  but that shit gets slow as fuck.

  <TODO> we could zip each third-party lib dir within ./lib + use zipimport

  """
  print("  INSTALLING RUNTIME LIBS TO: {}".format(dest))

  for f in pip.get_installed_top_level_files(packages):
    print("  - sym linking:  {}".format(f))

    _path = dest / f.name

    #: symlink the path
    f.sym(_path)

    #: ensure there's an `__init__.py` file in package roots
    if _path.isdir() and not (_path / "__init__.py").exists():
      (_path / "__init__.py").touch()

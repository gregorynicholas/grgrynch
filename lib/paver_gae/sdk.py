"""
  paver.ext.gae.sdk
  ~~~~~~~~~~~~~~~~~

  gae sdk version manager.


  :copyright: (c) 2014 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals
from paver.easy import task
from paver.easy import BuildFailure, path
from paver.easy import options as opts
from paver.ext import http, archives
from paver.ext.utils import rm, sh


__all__ = ['install_sdk', 'install_mapreduce_lib']


@task
def install_sdk():
  """
  installs the app engine sdk to the virtualenv.
  """
  # todo: add a "force" option to override cache
  archive = path(opts.gae.dev_appserver.ver + ".zip")
  if not (opts.proj.dirs.venv / archive).exists():
    http.wget(
      opts.gae.dev_appserver.src + archive.name, opts.proj.dirs.venv)

  rm(opts.gae.sdk.root)
  # todo: replaces with archives call.
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

  # integrate the app engine sdk with virtualenv
  pth_path = opts.proj.dirs.venv / "lib/python2.7/site-packages/gaesdk.pth"
  pth_path.write_lines([
    opts.gae.sdk.root.abspath(),
    "import dev_appserver",
    "dev_appserver.fix_sys_path()"])

  # use virtualenv hooks to add gae's sdk to the exec path
  postactivate = opts.proj.dirs.venv / "bin/postactivate"
  postactivate.write_lines([
    "#!/usr/bin/env bash",
    "echo \"exec path adjusted for google_appengine_1.8.9\"",
    "export PATH=\"{}\":$PATH".format(opts.gae.sdk.root)])


@task
def install_mapreduce_lib():
  """
  installs google app engine's mapreduce library.
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

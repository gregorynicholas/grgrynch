"""
  paver.ext.casperjs
  ~~~~~~~~~~~~~~~~~~

  paver extension for casperjs headless webkit testing.


  :copyright: (c) 2014 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals
import os
from paver.easy import Bunch, options as opts, cmdopts
from paver.easy import task, BuildFailure
from paver.ext.utils import sh, rm
from paver.ext.archives import extract


__all__ = ["install", "run", "CasperjsTestsFailure"]

opts(
  casperjs=Bunch(
    cookiesfile=".cookiejar",
  ))


class CasperjsTestsFailure(BuildFailure):
  """
  """


def _install_phantomjs_ubuntu():
  """
  installs phantomjs for end-to-end testing.
  """
  run = """
  apt-get install build-essential chrpath git-core
  apt-get install libssl-dev libfontconfig1-dev
  git clone git://github.com/ariya/phantomjs.git
  cd ./phantomjs
  git checkout 1.8
  ./build.sh
  """
  sh(run, cwd=opts.proj.dirs.venv)


def _install_phantomjs():
  """
  installs phantomjs for end-to-end testing.
  """
  rm(opts.proj.dirs.venv / "phantomjs")
  archive = "phantomjs-1.8.1-macosx.zip"
  if not os.path.exists(opts.proj.dirs.venv / archive):
    sh("curl -L -O http://phantomjs.googlecode.com/files/{archive}",
       archive=archive, cwd=opts.proj.dirs.venv)

  extract(archive, opts.proj.dirs.venv)
  run = """
  mv ./phantomjs-1.8.1-macosx ./phantomjs
  chmod +x ./phantomjs/bin/phantomjs
  ln -sf $PWD/phantomjs/bin/phantomjs $PWD/bin/phantomjs
  """
  sh(run, archive=archive, cwd=opts.proj.dirs.venv)


def _install_casperjs():
  """
  installs casperjs for end-to-end testing.
  """
  rm(opts.proj.dirs.venv / "casperjs")
  archive = "1.0.2.tar.gz"
  if not (opts.proj.dirs.venv / archive).exists():
    sh("curl -L -O https://github.com/n1k0/casperjs/archive/{archive}",
       archive=archive, cwd=opts.proj.dirs.venv)

  extract(archive, opts.proj.dirs.venv)
  run = """
  mv ./casperjs-1.0.2 ./casperjs
  chmod +x ./casperjs/bin/casperjs
  ln -sf $PWD/casperjs/bin/casperjs $PWD/bin/casperjs
  """
  sh(run, archive=archive, cwd=opts.proj.dirs.venv)


@task
def install():
  _install_phantomjs()
  _install_casperjs()
  print("---> casperjs_install: success\n")


@task
def build():
    """
    builds the casperjs test suite.
    """
    run = "coffee --compile --output {dest} {src}"
    sh(run, src="./src", dest="./build", cwd=opts.proj.dirs.casperjs.root)
    print("---> build_casperjs success\n")


@task
@cmdopts([
  ("path", "p", "path to the tests.")
])
def run(options):
  path = options.get("path", "./")
  rm(opts.casperjs.cookiesfile)
  command = "casperjs test {path} --cookies-file={cookiesfile}"
  rv = sh(
    command,
    path=path,
    cookiesfile=opts.casperjs.cookiesfile,
    cwd=opts.proj.dirs.casperjs.dest,
    capture=True)
  rm(opts.casperjs.cookiesfile)

  if "FAIL" in rv:
    raise CasperjsTestsFailure("""
      casperjs tests failure:
    {}
  """.format(rv))

  print rv

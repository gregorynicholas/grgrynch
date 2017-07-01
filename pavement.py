# encoding: utf-8
"""
  pavement
  ~~~~~~~~

  paver tasks. automate everything.


  :copyright: (c) by gregorynicholas.

"""
import os
import sys
sys.path.insert(0, "lib")
sys.path.append(os.path.abspath("."))
from hashlib import sha256
from itertools import chain
# from collections import defaultdict
#: imported first to load project config options.
from paver.ext.project import proj
from paver.ext.project import opts

from paver.ext.utils import yaml_load
from paver.ext.utils import file_to_utf8
from paver.ext.utils import rm
from paver.ext.utils import sh

from paver.easy import BuildFailure
from paver.easy import task, call_task, cmdopts
from paver.options import Namespace

from paver.ext import (
  casperjs,
  client,
  gae,
  nose,
  nvm,
  pip,
  release,
  virtualenv)


env_id_opt = (
  "env_id=", "e",
  "the environment to seed data to. is one of {}.".format(opts.proj.envs))


class InvalidEnvironmentIdOption(BuildFailure):
  """
  """


def _validate_env_id(options, optional=False):
  """
    :param options: instance of a `paver.options.Namespace` object
    :param optional: boolean
  """
  err = False
  env_id = options.get("env_id", None)
  if env_id is None and not optional:
    err = True
  if not err and (env_id not in opts.proj.envs):
    err = True
  if err:
    raise InvalidEnvironmentIdOption("""
  an environment must be specified with the -e flag as one of:
    {}
  """.format(opts.proj.envs))


def _bootstrap_init_dirs():
  opts.proj.dirs.data.root.makedirs_p()
  opts.proj.dirs.dist.makedirs_p()
  opts.proj.dirs.build.makedirs_p()
  opts.proj.dirs.lint.root.makedirs_p()
  opts.proj.dirs.lint.reports.makedirs_p()


def _load_dependencies_config():
  print('loading pip dependencies config..')
  return yaml_load(opts.proj.pip_dependencies)


def _install_pip_packages():
  packages = _load_dependencies_config()

  print('installing build pip dependency packages..')
  pip.install(packages, 'build')

  print('installing runtime pip dependency packages..')
  pip.install(packages, 'runtime')


def _install_appengine_sdk():
  packages = _load_dependencies_config()['runtime']

  print('installing app-engine sdk..')
  gae.sdk.install_sdk()

  print('installing third-party libs to work with app-engine runtime sdk..')
  gae.sdk.install_runtime_libs(packages, opts.proj.dirs.lib)


def _install_gcloud_sdk():
  base_url = 'https://dl.google.com/dl/cloudsdk/channels/rapid/downloads'
  file_url_path = 'google-cloud-sdk-155.0.0-darwin-x86_64.tar.gz'
  url = base_url + '/' + file_url_path
  # <TODO> .. migrate to using `gcloud` ..


@task
def bootstrap_server():
  """
  backend server setup + install.
  also configures 3rd party external python dependencies.
  """
  opts.proj.dirs.lib.makedirs_p()
  _install_pip_packages()
  print("---> bootstrap_server success\n")


@task
def bootstrap_server_gae_sdk():
  """
  """
  _install_appengine_sdk()
  # _install_gcloud_sdk()
  print("---> bootstrap_server_gae_sdk success\n")


@task
def bootstrap_client():
  """
  sets up the client development environment.
  """
  nvm_install = nvm.install()
  if nvm_install != True:
    print('nvm.install error:', nvm_install)
  else:
    print("---> nvm install success\n")

  sh("nvm use {}".format('0.10.26'), shell=False)
  return

  rm(opts.proj.dirs.client / "node_modules")
  sh("npm install -g {}".format('grunt@0.4.1 grunt-cli@0.1.8 bower stylus@0.31.0 coffee-script'))
  sh("npm install", cwd=opts.proj.dirs.client)
  sh("bower install", cwd=opts.proj.dirs.client)
  print("---> bootstrap_client success\n")


@task
def bootstrap():
  """
  sets up the project environment.
  """

  print("initializing directories..")
  _bootstrap_init_dirs()

  print("bootstrapping server + build tools..")
  call_task("bootstrap_server")

  print("boostrapping client..")
  call_task("bootstrap_client")

  print("---> bootstrap success\n")


@task
def clean_lib():
  """
  clean all lib dependency artifacts.
  """
  rm(opts.proj.dirs.pip)
  rm(opts.proj.dirs.lib)


@task
def clean():
  """
  clean artifacts produced by dist and empty artifacts produced by build.
  """
  rm(opts.proj.dirs.build,
     opts.proj.dirs.dist,
     opts.proj.dirs.deploy)

  # [os.remove(f) for f in opts.proj.dirs.base.walkfiles("*.yaml")]

  [os.remove(f) for f in opts.proj.dirs.app.walkfiles("*.py[co]")]


@task
def build_casperjs_tests():
  """
  builds casperjs tests.
  """
  sh("grunt build_casperjs", cwd=opts.proj.dirs.client)


@task
def build_server(options):
  """
  builds the server.
  """
  dest = opts.proj.dirs.base
  # env_id = options.get("env_id", opts.proj.envs.local)
  env_id = opts.proj.envs.local
  ver_id = release.dist_version_id()

  gae.supervisor_render_config(
    config_id=config_id,
    env_id=env_id,
    ver_id=ver_id,
  )

  gae.descriptor.build_descriptors(
    dest=dest,
    env_id=env_id,
    ver_id=ver_id)


@task
def build_client():
  """
  builds the client.
  """
  sh("grunt dist", cwd=opts.proj.dirs.client)
  dest = opts.proj.dirs.base

  print("\n---> build_client success: copying artifacts to app..")

  client.copy_page_templates(root=dest)
  client.copy_client_build_to_static(root=dest)

  # for cache-busting
  # client.tag_static_build(root=dest)


@task
@cmdopts([env_id_opt])
def build(options):
  """
  builds a debug version of the app for local development.
  """
  env_id = options.get("env_id", opts.proj.envs.local)
  ver_id = release.dist_version_id()
  config_id = options.get("config_id", "default")

  print('env-id: {}'.format(env_id))
  print('ver-id: {}'.format(ver_id))
  print('config-id: {}'.format(config_id))

  # STEP 1
  # ------
  # clean up previous build artifacts..
  call_task("clean")

  # STEP 2
  # ------
  # build the app client ui, then copy client build output
  # directly to the source app tree..
  call_task("build_client")

  # STEP 3
  # ------
  # build the app-engine descriptors..
  call_task("build_server")

  print("---> build success\n")


@task
@cmdopts([
  ("suite=", "s", "name of the html file to run the test suite.")
])
def test_client(options):
  """
  executes client unit & functional tests with mochajs.
  """
  suite = options.get("suite", "index.html")
  print("---> test_client success\n", suite)


@task
@cmdopts([
  ("path=", "p", "path to the tests file you want to run."),
  ("mode=", "m", "mode to the tests file you want to run. is one of "
                 "['local', 'integration'].", 'local'),
])
def test_server(options):
  """
  execute server unit & functional tests with nosetests.  if no path is
  specified, scans all modules in the project + executes tests.
  """
  path = options.get("path", opts.proj.dirs.app)
  mode = options.get("mode", "local")

  nose.run(
    path=path,
    config=opts.proj.dirs.buildconfig,
    mode=mode,
    env_id="test")

  print("---> test_server success\n")


@task
# @needs(["build_tests", "save"])
def test_headless_browser():
  """
  executes end-to-end tests with casperjs & phantomjs.
  """
  # wait for the server to run..
  # http.health_check(
  #   "http://{}".format(opts.proj.default_hostname))

  casperjs.build()
  try:
    _options = opts.Namespace()
    _options.path = "app/"
    casperjs.run(_options)
    # call_task("caspjerjs:run", _options)

  except casperjs.CasperjsTestsFailure, e:
    print("---> test_casperjs failure\n")
    raise e

  finally:
    # teardown test server..
    call_task("server_stop")

  print("---> test_headless_browser success\n")


@task
@cmdopts([env_id_opt])
def dist_build(options):
  """
  builds a release version of the app for deployment.
  """
  _validate_env_id(options)
  ver_id = release.dist_version_id()
  print("version id:", ver_id)

  #@ STEP 1
  #@ ------
  #@ clean up previous build artifacts..
  call_task("clean")
  call_task("build")

  #@ STEP 2
  #@ ------
  do_not_deploy = (
    "*.py[co]",
    ".data",
    ".lint",
    "build",
    "client",
    "tests",
    "docs",
    ".git*",
    "*.pid",
    "*.pip",
    "*.out",
    "*.err",
    "*.md",
    "*.sh",
    "*.txt",
    ".coverage",
    "*.*env",
    ".DS_Store",
    "pavement.py",
    "paver_*",
    "testsuite",
    "*_tests.py",
    "*supervisor*",
    "logs",

    #@ wtforms
    "sqlalchemy",

    #@ mongoengine
    "bson", "mongoengine", "pymongo", "flask_mongoengine", "gridfs",
  )
  opts.proj.dirs.base.cp(opts.proj.dirs.dist, ignore=do_not_deploy)

  #@ STEP 3
  #@ ------
  release.write_ver_id(ver_id)

  print("---> dist success\n")


@task
@cmdopts([env_id_opt])
def dist_release(options):
  """
  make a release, deploy it to the target environment.
  """
  _validate_env_id(options)

  # build
  call_task("dist_build", options)

  # deploy
  _deploy_opts = opts.Namespace()
  _deploy_opts.default = True

  call_task("gae:deploy", _deploy_opts)

  print("---> release success\n")


@task
@cmdopts([env_id_opt])
def dbseed(options):
  """
  load any reference data into the datastore if it"s not already present.
  """
  env_id = options.get("env_id", opts.proj.envs.local)
  _validate_env_id(options, optional=True)

  # <TODO>

  print("---> dbseed success\n")


@task
def lint():
  call_task("linter:check")

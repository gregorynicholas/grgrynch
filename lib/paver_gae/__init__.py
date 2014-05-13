"""
  paver.ext.gae
  ~~~~~~~~~~~~~

  paver extension for google app engine.


  :copyright: (c) 2014 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals
from jinja2 import Environment
from jinja2.loaders import DictLoader

from paver.easy import Bunch, cmdopts
from paver.easy import task, call_task
from paver.easy import BuildFailure
from paver.ext.project import opts
from paver.ext import supervisor, pip
from paver.ext import release, utils
from paver.ext.utils import rm, sh

from paver.ext.gae import descriptor
from paver.ext.gae.appcfg import appcfg
from paver.ext.gae.backends import *
from paver.ext.gae.cron import *
from paver.ext.gae.dos import *
from paver.ext.gae.index import *
from paver.ext.gae.queue import *
from paver.ext.gae.sdk import *
from paver.ext.gae.oauth2 import *


__all__ = [
  "appcfg", "install_runtime_libs", "descriptor", "killall", "datastore_init",
  "server_run", "server_stop", "server_restart", "server_tail",
  "deploy", "deploy_branch", "update_indexes", "open_admin",
  "backends", "backends_rollback", "backends_deploy", "get_backends",
  "ServerStartFailure",
]


opts(
  gae=Bunch(
    sdk=Bunch(
      root=opts.proj.dirs.venv / opts.proj.dev_appserver.ver,
    ),
    dev_appserver=opts.proj.dev_appserver
  ))


class ServerStartFailure(BuildFailure):
  """
  """


class SdkServerNotRunningFailure(BuildFailure):
  """
  """


# shell command utils.
# -----------------------------------------------------------------------------

def _dev_appserver_config(config_id="default"):
  """
  returns config dict for the dev_appserver of a specified environ.
  """
  config = opts.gae.dev_appserver[config_id]
  if "blobstore_path" not in config["args"]:
    config["args"]["blobstore_path"] = opts.proj.dirs.data.blobstore

  if "datastore_path" not in config["args"]:
    config["args"]["datastore_path"] = opts.proj.dirs.data.datastore_file

  return config


def _parse_flags(cfg):
  """
  returns a string to run as the `dev_appserver.py` command.
  """
  flags = utils.parse_cmd_flags(cfg["args"], cfg["flags"])
  return "{}/dev_appserver.py {} .".format(opts.gae.sdk.root, flags)


def install_runtime_libs(packages, dest):
  """
  since app engine doesn't allow for fucking pip installs, we have to symlink
  the libs to a local project directory. we could do 2 separate pip installs,
  but that shit gets slow as fuck.

    :todo: zip each lib inside of the lib dir to serve third party libs
  """
  for f in pip.get_installed_top_level_files(packages):
    # print "sym linking: ", f
    _path = dest / f.name

    # symlink the path
    f.sym(_path)

    # ensure there's an `__init__.py` file in package roots
    if _path.isdir() and not (_path / "__init__.py").exists():
      (_path / "__init__.py").touch()


@task
@cmdopts([
  ("set-default", "d", "set the current dist version as the default serving "
                       "version on app engine.", False),
  ("clear-cookies=", "c", "clear local cookies before deploying.", True),
  ("deploy-backends", "b", "flag to deploy the backend servers.", False),
])
def deploy(options):
  """
  deploys the app to google app engine remote servers.
  """
  ver_id = release.dist_version_id()
  appcfg(
    "update -v ",
    error=False, capture=True, cwd=opts.proj.dirs.dist)

  if options.set_default:
    set_default_serving_version(ver_id)

  if options.deploy_backends:
    call_task("backends_deploy")

  print("---> deploy success\n")


def set_default_serving_version(ver_id):
  """
  sets the default serving version on app engine remote servers.

    :param ver_id:
  """
  appcfg(
    "set_default_version",
    version=ver_id,
    cwd=opts.proj.dirs.dist)


@task
def deploy_branch(options):
  """
  deploy current branch to named instance onto the integration environment.
  """
  call_task("build")

  _opts = opts.Namespace()
  _opts.env_id = opts.proj.envs.integration
  call_task("dist", options=_opts)

  _opts = opts.Namespace()
  _opts.default = False
  call_task("deploy", options=_opts)


@task
def update_indexes():
  """
  updates model index definitions on google app engine remote servers.
  """
  appcfg("vacuum_indexes", quiet=True, cwd=opts.proj.dirs.dist)
  appcfg("update_indexes", quiet=True, cwd=opts.proj.dirs.dist)
  print("---> update_indexes success\n")


@task
def datastore_init():
  """
  cleans + creates the local app engine sdk server blobstore & datastore.
  """
  rm(opts.proj.dirs.data.datastore,
     opts.proj.dirs.data.blobstore)
  opts.proj.dirs.data.blobstore.makedirs()
  opts.proj.dirs.data.datastore.makedirs()
  opts.proj.dirs.data.datastore_file.touch()
  print("---> datastore_init success\n")


dev_appserver_config_option = (
  "config_id=", "c", "name of the configuration profile, defined in "
                     "dev_appserver.yaml, to run the server with.")


@task
@cmdopts([dev_appserver_config_option])
def server_run(options):
  """
  starts a google app engine server for local development.
  """
  env_id = options.get("env_id", opts.proj.envs.local)
  ver_id = release.dist_version_id()
  config_id = options.get("config_id", "default")

  # if supervisor.is_pid_running(pid):
  #   raise ServerStartFailure("app engine sdk server is already running..")

  dev_appserver_command = _parse_flags(_dev_appserver_config(config_id))

  # generate the supervisord.conf file
  context = dict(
    dev_appserver_command=dev_appserver_command,
    app_id=opts.proj.app_id,
    env_id=env_id,
    ver_id=ver_id,
    stdout=_stdout_path(),
  )
  template = (opts.proj.dirs.buildconfig / 'supervisord.template.conf').text()

  jinjaenv = Environment(loader=DictLoader(
    {'supervisord.template.conf': str(template)}
  ))

  descriptor.render_jinjaenv(jinjaenv, context, opts.proj.dirs.base)
  supervisor.start()

  stdout = supervisor.run('devappserver-{}'.format(env_id))
  if "ERROR (already started)" in stdout:
    raise ServerStartFailure("server already running..")


@task
@cmdopts([dev_appserver_config_option])
def server_stop(options):
  """
  stops the google app engine sdk server.
  """
  env_id = options.get("env_id", opts.proj.envs.local)
  supervisor.stop('devappserver-{}'.format(env_id))
  supervisor.shutdown()
  killall()  # remove any leaks..


@task
@cmdopts([
  ("config_id=", "c", "name of the configuration profile, defined in "
                      "project.yaml, to run the server with.")
])
def server_restart(options):
  """
  restarts the local Google App Engine SDK server.
  """
  server_stop(options)
  server_run(options)


def _stdout_path():
  """
  returns a path instance to the stdout log path.
  """
  return opts.proj.dirs.logs / "app.log"


@task
def server_tail():
  """
  view the dev_appserver logs by running the unix native "tail" command.
  """
  print sh("tail -f {}", _stdout_path(), capture=True)


@task
@cmdopts([
  ("config_id=", "c", "name of the configuration profile, defined in "
                      "project.yaml, to run the server with.")
])
def open_admin(options):
  """
  opens the google app engine sdk admin console.
  """
  config_id = options.get("config_id", "default")
  sh("open http://{url}:{port}/",
     cwd=opts.proj.dirs.base,
     **_dev_appserver_config(config_id).get("args"))


@task
def killall():
  """
  quietly kills all known processes known to god and man.
  """
  try:
    sh("killall node", capture=True)
    sh("killall dev_appserver.py", capture=True)
    sh("killall _python_runtime.py", capture=True)
  except:
    pass

"""
  paver.ext.nose
  ~~~~~~~~~~~~~~

  paver extension for nose test runner.


  :copyright: (c) 2013 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals
from paver.ext.utils import sh


def run(path, config, mode, env_id):
  """
  executes the nosetests runner.

    :param path:
    :param config:
    :param mode:
    :param env_id:
  """
  # set environment variables inline with the command
  env_vars = "ENV_ID={env_id} NOSE_MODE={mode} ".format(
    mode=mode,
    env_id="test")

  cmd = "{env_vars} "
  "nosetests -c {config}/nose-{mode}.cfg "
  "{path}"

  # print 'COMMAND:', cmd

  return sh(
    cmd,
    env_vars=env_vars,
    config=config,
    mode=mode,
    env_id="test",
    path=path,
    error=True,
    capture=False)

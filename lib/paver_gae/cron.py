"""
  paver.ext.gae.cron
  ~~~~~~~~~~~~~~~~~~

  paver extension to automate app engine.


  :copyright: (c) 2014 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals
from paver.easy import options as opts
from paver.easy import task
from paver.ext.gae import descriptor


__all__ = ["crons"]


def _cron_descriptor(build_target=opts.proj.dirs.base):
  """
  returns cron job descriptor.
  """
  return descriptor.cron(build_target)


@task
def crons():
  """
  displays cron jobs configured.
  """
  # TODO: generate yaml rendering.
  cron_descriptor = _cron_descriptor()
  print 'cron_descriptor:', cron_descriptor

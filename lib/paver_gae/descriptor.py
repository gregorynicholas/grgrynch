"""
  paver.ext.gae.descriptor
  ~~~~~~~~~~~~~~~~~~~~~~~~

  paver extension to automate app engine.


  :copyright: (c) 2014 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals
from paver.easy import Bunch
from paver.ext import utils


class DESCRIPTORS(object):
  app = "app"
  backends = "backends"
  cron = "cron"
  dos = "dos"
  index = "index"
  queue = "queue"


def load(path, descriptor):
  """
    :returns: the parsed yaml for the backends descriptor.
  """
  rv = utils.yaml_load(
    path / "{}.yaml".format(descriptor)).get(descriptor)
  for v in range(len(rv)):
    rv[v] = Bunch(**rv[v])
  return rv


# creates a shorthand method for each descriptor name
import sys
m = sys.modules[__name__]
for name in [_ for _ in dir(DESCRIPTORS) if not _.startswith("_")]:
  fn = lambda path, name=name: load(path, DESCRIPTORS.__dict__.get(name))
  setattr(m, name, fn)

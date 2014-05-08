"""
  paver.ext.gae.descriptor
  ~~~~~~~~~~~~~~~~~~~~~~~~

  paver extension to automate app engine.


  :copyright: (c) 2013 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals
from paver.easy import Bunch
from paver.easy import BuildFailure
from paver.ext import utils


class DESCRIPTORS(object):
  """
  enum of app engine descriptor file names.
  """
  app = "app"
  backends = "backends"
  cron = "cron"
  dos = "dos"
  index = "index"
  queue = "queue"


class DescriptorNotFound(BuildFailure):
  """
  """


def load(path, descriptor):
  """
    :returns: the parsed yaml for the backends descriptor.
  """
  f = path / '{}.yaml'.format(descriptor)
  if not f.exists():
    raise DescriptorNotFound(
      "descriptor file not found: {}".format(descriptor))

  rv = utils.yaml_load(f).get(descriptor)
  for v in range(len(rv)):
    rv[v] = Bunch(**rv[v])
  return rv


# creates shorthand methods for each descriptor name
# ex: `descriptor.cron()`  returns the yaml config for cron.yaml
import sys
m = sys.modules[__name__]
for name in [_ for _ in dir(DESCRIPTORS) if not _.startswith("_")]:
  fn = lambda path, name=name: load(path, DESCRIPTORS.__dict__.get(name))
  setattr(m, name, fn)

"""
  paver.ext.gae.descriptor
  ~~~~~~~~~~~~~~~~~~~~~~~~

  paver extension to work with app-engine yaml service config descriptors.


  :copyright: (c) 2014 by gregorynicholas.

"""
from __future__ import unicode_literals
from jinja2 import Environment
from jinja2.loaders import DictLoader
from paver.easy import Bunch
from paver.easy import BuildFailure
from paver.ext import release
from paver.ext import utils
from paver.ext.project import opts


__all__ = [
  'DESCRIPTORS',
  'build_descriptors',
  'render_jinja_templates',
  'DescriptorNotFound'
]


class DESCRIPTORS(object):
  """
  enum of app-engine service descriptor file-names.
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
  returns a `Bunch`d yaml for the specified descriptor.
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


# descriptor utils.
# -----------------------------------------------------------------------------

def render_jinja_templates(jinjaenv, context, dest):
  """
  renders all templates in the specified `jinjaenv`.
  """
  for name, _ in jinjaenv.loader.mapping.iteritems():
    template = jinjaenv.get_template(name)
    _write_descriptor(name, template, context, dest)


def _load_descriptors():
  """
  loads yaml descriptor templates and returns an instance of a
  `jinja2.Environment`
  """
  descriptors = opts.proj.dirs.gae.descriptors.walkfiles("*.yaml")
  rv = Environment(loader=DictLoader(
    {str(d.name): str(d.text()) for d in descriptors}
  ))
  return rv


def _write_descriptor(name, template, context, dest):
  """
  parses the config template files and generates yaml descriptor files in
  the root directory.

    :param template: instance of a jinja2 template object
    :param context: instance of a dict
    :param dest: instance of a paver.easy.path, string file path to write to
  """
  print('writing descriptor file: {} ({})'.format(name, dest))
  descriptor = dest / name.replace(".template", "")
  descriptor.write_text(template.render(**context))


def build_descriptors(dest, env_id, ver_id=None):
  """
    :param dest:
    :param env_id:
    :param ver_id:
  """
  if ver_id is None:
    ver_id = release.dist_version_id()

  module_id = None
  runtime = 'python27'
  api_version = 1

  builtins = [
    'deferred',
  ]

  inbound_services = []
  if env_id in ('prod', 'integration'):
    #: on local machine, warmup seems to be called in a continuous poll..
    inbound_services.append('warmup')

  context = dict(
    app_id=opts.proj.app_id,
    env_id=env_id,
    ver_id=ver_id,
    module_id=module_id,
    templates_dir=str(opts.proj.dirs.app_web_templates.relpath()),
    static_dir=str(opts.proj.dirs.app_web_static.relpath()),
    builtins=builtins,
    inbound_services=inbound_services,
    runtime=runtime,
    api_version=api_version,
  )

  render_jinjaenv(_load_descriptors(), context, dest)

"""
  paver.ext.linter
  ~~~~~~~~~~~~~~~~

  paver extension for linting + static analysis.

  @see github.com/shazow/workerpool/blob/master/check.py


  :copyright: (c) 2014 by gregorynicholas.

"""
from __future__ import unicode_literals
from paver.easy import task, options as opts
from collections import OrderedDict
import pep8
from pyflakes.scripts import pyflakes
from pprint import pprint, pformat


__all__ = [
  'check',
]


def _flk8(path, files):
  """
  """
  print("---> running pyflakes...")
  _errored = False
  _error_count = 0

  for f, _ in files.iteritems():
    files[f]['flk8']['response'] = pyflakes.checkPath(f)
    status = files[f]['flk8']['response'] == 0
    files[f]['flk8']['status'] = status

    if not status:
      _errored = True
      _error_count += 1

  return (files, _errored, _error_count)


def _pep8(path, files):
  """
  """
  print("---> running pep8...")
  _errored = False
  _error_count = 0

  # pep8.process_options([''])
  for f, _ in files.iteritems():
    files[f]['pep8']['response'] = pep8.Checker(f).check_all()
    status = files[f]['pep8']['response'] == 0
    files[f]['pep8']['status'] = status

    if not status:
      _errored = True
      _error_count += 1

  return (files, _errored, _error_count)


@task
def check():
  path = opts.proj.dirs.app

  #@ create a hash-map of the files..
  files = {f: OrderedDict(
    pep8={'response': None, 'status': None},
    flk8={'response': None, 'status': None},
  ) for f in path.walkfiles("*.py")}

  files, pep8_error, pep8_error_count = _pep8(path, files)
  files, flk8_error, flk8_error_count = _flk8(path, files)

  if pep8_error or flk8_error:
    _report_errors(
      files,
      pep8_error, pep8_error_count,
      flk8_error, flk8_error_count)

  else:
    print("---> shit's clean!")


def _report_errors(results, pep8_error, pep8_error_count, flk8_error, flk8_error_count):
  """
  """
  msg = '\n'

  if pep8_error:
    msg += "\n"
    msg += "[ pep8:errors ]: {} source files with errors\n".format(pep8_error_count)
    # msg += "\n"
    # msg += "[ pep8:errors ]: count: {}\n".format(pep8_error_count)
    # msg += "\n"

  if flk8_error:
    # msg += "\n"
    msg += "[ flk8:errors ]: {} source files with errors\n".format(flk8_error_count)
    # msg += "\n"
    # msg += "[ flk8:errors ]: count: {}\n".format(flk8_error_count)
    msg += "\n"

  msg += "file\t\t\t\t| pep8\t| flk8\n"
  msg += "--------------------------------|-------|-------\n"

  for file, result in results.iteritems():
    if result['pep8']['status'] and result['flk8']['status']:
      continue

    msg += "{}\t\t|".format(file)
    msg += "{}\t|".format(result['pep8']['response'])
    msg += "{}\t".format(result['flk8']['response'])
    msg += "\n"

  msg += "\n"
  msg += "===================================================\n"

  print(msg)

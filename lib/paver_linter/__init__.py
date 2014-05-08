"""
  paver.ext.linter
  ~~~~~~~~~~~~~~~~

  paver extension for linting + static analysis.

  happily sourced from:
  github.com/shazow/workerpool/blob/master/check.py


  :copyright: (c) 2014 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals
from paver.easy import task, options as opts
import pep8
from pyflakes.scripts import pyflakes


def pyflakes(src):
  print("---> running pyflakes...")
  clean = True
  for f in src.walkfiles("*.py"):
    if pyflakes.checkPath(f) != 0:
      clean = False
      break
  return clean


def pep8(src):
  print("---> running pep8...")
  clean = True
  # pep8.process_options([''])
  for f in src.walkfiles("*.py"):
    if pep8.Checker(f).check_all() != 0:
      clean = False
      break
  return clean


@task
def check():
  path = opts.proj.dirs.app
  if not pep8(path):
    print
    err = "ERROR: pep8 failed on some source files\n"
    err += "ERROR: please fix the errors and re-run this script"
    print(err)

  if not pyflakes(path):
    print
    err = "ERROR: pyflakes failed on some source files\n"
    err += "ERROR: please fix the errors and re-run this script"
    print(err)

  print("---> shit's clean!")

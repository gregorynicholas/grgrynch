"""
  paver.ext.osx
  ~~~~~~~~~~~~~

  paver extension for osx.


  :copyright: (c) 2014 by gregorynicholas.

"""
from paver.easy import task
from paver.ext.utils import sh


__all__ = [
  'clear',
  "osascript",
]


@task
def clear():
  """
  invokes applescript to clear terminal screen. (same as pressing `cmd+k`)
  """
  osascript(
    'tell application "System Events" to tell process '
    '"Terminal" to keystroke "k" using command down')


def osascript(script):
  """
  executes an applescript string.
  """
  return sh(
    "/usr/bin/open -a Terminal /usr/bin/osascript -e '{script}'",
    script=script.replace('"', '\"'))

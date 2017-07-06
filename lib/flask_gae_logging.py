"""
  flask_gae_logging
  ~~~~~~~~~~~~~~~~~

  making logging with flask + app-engine apps easier.


  if app_config.IS_LOCAL:
    set_logging_local()
  else:
    set_logging_production()
    register_ereporter()


  :copyright: (c) by gregorynicholas.

"""
import logging
from logging import Formatter, basicConfig, getLogger
from google.appengine.ext import ereporter
from app.config import config as app_config


format = '\033[0;34m%(levelname)-7s'
'\033[0;0m %(filename)s\033[0;0m:\033'
'[0;0mline:%(lineno)-2s\033[0;0m:\033'
'[0;0mfn:%(funcName)-3s\033[0;0m %(message)s'
formatter = Formatter(format)
log = getLogger()


def set_logging_local():
  basicConfig(level=logging.DEBUG, format=format)
  for handler in log.handlers:
    handler.setFormatter(formatter)
  log.setLevel(logging.DEBUG)
  logging.logMultiprocessing = 1
  log.debug('setting logging level for LOCAL env.')


def set_logging_production():
  basicConfig(level=logging.INFO)
  log.setLevel(logging.INFO)
  logging.logMultiprocessing = 0
  log.info('setting logging level for PRODUCTION env.')


def register_ereporter():
  for handler in log.handlers:
    if not isinstance(handler, ereporter.ExceptionRecordingHandler):
      ereporter.register_logger()
      log.debug('initializing ereporter: %s, handler: %s..', log, handler)


_level_colors = {
  "DEBUG": "\033[22;34m",
  "INFO": "\033[01;32m",
  "WARNING": "\033[22;35m",
  "ERROR": "\033[22;31m",
  "CRITICAL": "\033[01;31m"
}


def _error(msg, *args, **kwargs):
  old_error("\033[22;31m%s\033[0;0m" % msg, *args, **kwargs)


def _warning(msg, *args, **kwargs):
  old_warning("\033[22;35m%s\033[0;0m" % msg, *args, **kwargs)


def _info(msg, *args, **kwargs):
  old_info("\033[00;34m%s\033[0;0m" % msg, *args, **kwargs)


old_warning = logging.warning
old_error = logging.error
old_info = logging.info

logging.warning = _warning
logging.error = _error
logging.info = _info

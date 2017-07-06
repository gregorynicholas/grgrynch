"""
  app.config
  ~~~~~~~~~~

  flask app & project configuration settings.


  :copyright: (c) 2014 by gregorynicholas.

"""
from __future__ import unicode_literals
from os import environ
import keys


__all__ = [
  "DEFAULT_ENV_ID",
  "env_id",
  "config",
  "Config",
  "LocalConfig",
  "QaConfig",
  "TestConfig",
  "IntegrationConfig",
  "ProdConfig",
]


DEFAULT_ENV_ID = "local"
env_id = environ.get("ENV_ID", DEFAULT_ENV_ID)


class AppConfig(object):
  """
  """
  def __str__(self):
    return self.__class__.__name__


class Config(AppConfig):
  env_id = env_id
  #: prevents a weird bubbling of bad request errors for missing form params.
  TRAP_BAD_REQUEST_ERRORS = True
  DEBUG = True
  TESTING = False
  CSRF_ENABLED = False
  # CSRF_SESSION_KEY = keys.SESSION_KEY
  jinja_strict_undefined = False

  #: flask-debugtoolbar settings
  DEBUG_TB_PROFILER_ENABLED = True
  DEBUG_TB_INTERCEPT_REDIRECTS = False

  #: flask-cache settings
  CACHE_TYPE = "gaememcached"

  # SECRET_KEY = keys.SESSION_KEY
  # SESSION_PROTECTION = "strong"
  # SESSION_COOKIE_NAME = "session"

  # set secret keys for csrf protection
  flask_debug = True
  flask_secret_key = keys.FLASK_SECRET_KEY
  flask_session_cookie_secure = True
  flask_remember_cookie_name = "session"
  flask_remember_cookie_duration_in_days = 365

  facebook_app_id = ""
  facebook_secret = ""

  twitter_app_id = ""
  twitter_secret = ""

  linkedin_app_id = ""
  linkedin_secret = ""

  sendgrid_username = ""
  sendgrid_password = ""
  sendgrid_callback_username = "sendgrid"
  sendgrid_callback_password = ""

  fullcontact_api_key = ""

  sentry_dsn = None


class LocalConfig(Config):
  """
  Local development env.
  """
  TESTING = False
  SERVER_NAME = "lvh.me:8888"
  SESSION_COOKIE_DOMAIN = ".lvh.me:8888"

  facebook_app_id = ""
  facebook_secret = ""

  twitter_app_id = ""
  twitter_secret = ""

  linkedin_app_id = ""
  linkedin_secret = ""


class TestConfig(Config):
  """
  Unit testing env.
  """
  DEBUG = True
  TESTING = True
  SERVER_NAME = "lvh.me:8888"
  SESSION_COOKIE_DOMAIN = ".lvh.me:8888"

  jinja_strict_undefined = True

  # Don"t send emails when running tests
  sendgrid_username = None
  sendgrid_password = None


class IntegrationConfig(Config):
  """
  Continuous integration env.
  """
  SERVER_NAME = "lvh.me:8888"

  jinja_strict_undefined = True

  # Don"t send emails when running tests
  sendgrid_username = None
  sendgrid_password = None


class QaConfig(Config):
  """
  Manual QA / Staging env.
  """
  SERVER_NAME = "gregorynicholas-qa.com"
  SESSION_COOKIE_DOMAIN = ".gregorynicholas-qa.com"
  # PREFERRED_URL_SCHEME = "https"

  facebook_app_id = ""
  facebook_secret = ""

  linkedin_app_id = ""
  linkedin_secret = ""

  twitter_app_id = ""
  twitter_secret = ""

  sentry_dsn = ""


class ProdConfig(Config):
  """
  Live production env.
  """
  DEBUG = True
  TESTING = False

  #: flask-debugtoolbar settings
  DEBUG_TB_PROFILER_ENABLED = False
  DEBUG_TB_INTERCEPT_REDIRECTS = True

  SERVER_NAME = "gregorynicholas.com"
  SESSION_COOKIE_DOMAIN = ".gregorynicholas.com"
  # PREFERRED_URL_SCHEME = "https"

  facebook_app_id = ""
  facebook_secret = ""

  linkedin_app_id = ""
  linkedin_secret = ""

  twitter_app_id = ""
  twitter_secret = ""

  sentry_dsn = None


_env_config = None


def _config():
  """
    :returns: reference to a Config class based on the current environment.
  """
  global _env_config
  if _env_config is not None:
    return _env_config
  _env_config = globals().get("{}Config".format(env_id.capitalize()))
  setattr(_env_config, "env_id", env_id)
  return _env_config

config = _config()

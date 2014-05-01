"""
  flask.ext.login_ndb
  ~~~~~~~~~~~~~~~~~~~

  bridges flask.ext.login to app engine ndb.  allows for the separation of
  storage implementation vs extension + flask integration.


  :copyright: (c) 2013 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals
from logging import getLogger
from cStringIO import StringIO
from flask.ext.login import UserMixin
from flask.ext.login_auth import MissingSessionError
from simplekv import KeyValueStore
from google.appengine.ext import ndb
from app.models.user import User

logger = getLogger(__name__)


class Session(ndb.Model):
  """
  represents a session model.
  """
  v = ndb.BlobProperty(indexed=False)

  def to_dict(self):
    value = ndb.Model.to_dict(self)
    value["id"] = self.key.id()
    return value


class SessionStore(KeyValueStore):
  """
  an ndb backed datastore session store.
  """

  def __init__(self):
    self.obj_class = Session

  def _delete(self, key):
    db_key = ndb.Key(self.obj_class, key)
    db_key.delete()

  def _get(self, key):
    obj = self.obj_class.get_by_id(id=key)
    if not obj:
      raise MissingSessionError(key)
    return obj.v

  def _has_key(self, key):
    rv = (None != self.obj_class.get_by_id(id=key))
    logger.info('result: %s', rv)
    return rv

  def iter_keys(self):
    qry_iter = self.obj_class.query().iter(keys_only=True)
    return (k.string_id() for k in qry_iter)

  def _open(self, key):
    return StringIO(self._get(key))

  def _put(self, key, data):
    obj = self.obj_class(id=key, v=data)
    obj.put()

    return obj.key.string_id()

  def _put_file(self, key, file):
    return self._put(key, file.read())


class FlaskUser(UserMixin):
  """
  user model for flask-Login.
  """

  @staticmethod
  def find_by_email(email):
    """
    finds a user with the specified email.

      :param email: valid email to search with.
    """
    try:
      user = User.find_by_email(email)
      if user:
        return FlaskUser(user)
    except Exception:
      import traceback as tb
      logger.warn("Could not find user with email : %s", tb.format_exc())
    logger.warn("Could not find user with email : %s", email)

  @staticmethod
  def find_by_id(id):
    """
    finds a user with the specified int gae id.

      :param id: An int id to search for.
    """
    user = User.get_by_id(int(id))
    if user:
      return FlaskUser(user)
    logger.warn("Could not find user with id : %s", id)

  def __init__(self, user):
    self.user = user

  def get_id(self):
    if self.user and self.user.key:
      return self.user.key.id()

  def password(self):
    return self.user.password

  def email(self):
    return self.user.email

  def is_active(self):
    """
      :returns: False if the user still has to verify their email address.
    """
    return self.user.active

  def check_password(self, password):
    return self.user.check_password(password)

  def session_ctx(self):
    """
    method used to get a dict of user data for use in the flask + jinja
    environments.

      :returns: a dict of user / anonymous user data.
    """
    rv = self.default_session_ctx()
    rv['anonymous'] = False
    rv['user_key'] = self.user.key
    rv['name'] = self.user.nickname
    rv['email'] = self.user.email
    rv['profile_thumb_url'] = self.user.profile_pic_url
    return rv

  @classmethod
  def default_session_ctx(cls):
    """
      :returns: dict with default values for an anonymous user.
    """
    return {"id": None, "anonymous": True}

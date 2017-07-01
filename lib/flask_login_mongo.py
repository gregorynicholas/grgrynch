"""
  flask.ext.login_mongo
  ~~~~~~~~~~~~~~~~~~~~~

  bridges flask.ext.login to mongoengine.  allows for the separation of
  storage implementation vs extension + flask integration.


  :copyright: (c) 2013 by gregorynicholas.

"""
from __future__ import unicode_literals
from logging import getLogger
from cStringIO import StringIO
from flask.ext.login import UserMixin
from flask.ext.login_auth import MissingSessionError
from simplekv import KeyValueStore
import mongoengine as mongo
# from bson.objectid import ObjectId

logger = getLogger(__name__)


class Session(mongo.Document):
  """
  represents a session model.
  """
  key = mongo.StringField()
  v = mongo.BinaryField()

  def to_dict(self):
    value = mongo.Document.to_mongo(self)
    return value


class SessionStore(KeyValueStore):
  """
  a mongoengine backed database session store.
  """
  def __init__(self):
    self.obj_class = Session

  def _delete(self, key):
    try:
      rv = self.obj_class.objects.get(key=key)
      rv.delete()
    except self.obj_class.DoesNotExist:
      pass

  def _get(self, key):
    try:
      rv = self.obj_class.objects.get(key=key)
    except mongo.ValidationError:
      raise MissingSessionError(key)
    return rv.v

  def _has_key(self, key):
    try:
      rv = self.obj_class.objects.get(key=key)
      if rv:
        return True
      else:
        raise mongo.ValidationError()
    except mongo.ValidationError:
      return False

  # todo: implement
  # def iter_keys(self):
  #   qry_iter = self.obj_class.objects().iter(keys_only=True)
  #   return (k.string_id() for k in qry_iter)

  def _open(self, key):
    return StringIO(self._get(key))

  def _put(self, key, data):
    rv, created = self.obj_class.objects.get_or_create(
      key=key, defaults={'v': data})
    if not created:
      rv.v = data
      rv.save()
    return rv.key

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
    from app.models.user import user
    try:
      user = user.User.find_by_email(email)
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
    from app import models
    user = models.User.get_by_id(id)
    if user:
      return FlaskUser(user)
    logger.warn("Could not find user with id : %s", id)

  def __init__(self, user):
    self.user = user

  def get_id(self):
    return self.user.key

  def is_active(self):
    """
      :returns: False if the user still has to verify their email address.
    """
    return self.user.active

  def session_ctx(self):
    """
    method used to get a dict of user data for use in the flask + jinja
    environments.

      :returns: a dict of user / anonymous user data.
    """
    rv = self.default_session_ctx()
    rv['anonymous'] = False
    rv['user_key'] = self.user.key
    rv['name'] = self.user.name
    rv['email'] = self.user.email
    rv['profile_pic_url'] = self.user.profile_pic_url
    return rv

  @classmethod
  def default_session_ctx(cls):
    """
      :returns: dict with default values for an anonymous user.
    """
    return {"id": None, "anonymous": True}

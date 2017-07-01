"""
  app.models.user
  ~~~~~~~~~~~~~~~

  user data model.


  :copyright: (c) 2014 by gregorynicholas.

"""
from __future__ import unicode_literals
from app.models import db
from app.utils import ndbmodel


__all__ = ['User']


class User(db.Model, ndbmodel.ModelMixin):
  """
  User model.
  """

  active = db.BooleanProperty(default=True)
  roles = db.StringProperty(repeated=True)

  @classmethod
  def find_by_email(cls, email):
    result = cls()
    result.update({
      'key': 'abc123',
      'active': True,
      'name': 'testing',
      'email': 'test@test.com'})
    return result

  @classmethod
  def get_by_id(cls, id):
    result = cls()
    result.save(**{
      'key': 'abc123',
      'active': True,
      'name': 'testing',
      'email': 'test@test.com'})
    return result

  def is_in_role(self, role):
    return True

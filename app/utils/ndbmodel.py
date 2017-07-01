"""
  app.utils.ndbmodel
  ~~~~~~~~~~~~~~~~~~

  encapsulated helpers to make modeling for appengine-ndb easier.


  :copyright: (c) 2014 by gregorynicholas.

"""
from __future__ import unicode_literals


class ModelMixin(object):
  """
  mixin for ndb.Model subclasses.
  """

  @classmethod
  def create(cls, put=True, *args, **kw):
    """
      :param put: boolean to write the entity to the datastore.
      :returns: an instance of the model class entity object.
    """
    key = kw.pop("key", None)
    rv = cls(key=key)
    rv.populate(**kw)
    if put:
      rv.put()
    return rv

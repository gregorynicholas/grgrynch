"""
  flask.ext.enum
  ~~~~~~~~~~~~~~

  enumeration. not pythonic, but using to help enforce data in
  mongodb, since that shit can get gnarly if schema get's fucked.


  :copyright: (c) 2014 by gregorynicholas.
"""
from __future__ import unicode_literals

__all__ = ["Enum"]


class EnumMeta(type):
  def __new__(cls, name, bases, attrs):
    _super_new = super(EnumMeta, cls).__new__

    _values = {}
    for k, v in attrs.iteritems():
      if k.startswith('__'):
        continue
      _values[k] = v
    attrs['_values'] = _values

    # create the new_class
    new_class = _super_new(cls, name, bases, attrs)
    return new_class

  def __getattr__(self, name):
    return self._values.get(name)

  def __setattr__(self, name, value):  # this makes it read-only
    raise NotImplementedError

  def __str__(self):
    args = {'name': self.__name__, 'values': ', '.join(self._values)}
    return '{name}({values})'.format(**args)

  def value(self, key):
    """
      :param key: string name of the key.
      :returns: value for the given key.
    """
    return self._values[key]

  def choices(self):
    """
      :returns: list of tuples for key/value pairs.
    """
    return self._values.items()

  def values(self):
    """
      :returns: list of values.
    """
    return self._values.values()


class Enum(object):
  __metaclass__ = EnumMeta

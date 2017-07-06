"""
  app.utils.ndbproperties
  ~~~~~~~~~~~~~~~~~~~~~~~

  encapsulated helpers to make modeling for appengine-ndb easier.


  :copyright: (c) 2013 by gregorynicholas.

"""
from __future__ import unicode_literals
from google.appengine.ext import ndb


class EnumProperty(ndb.IntegerProperty):
  """
  allows efficient storing of an enum-like choice property.
  """

  choices = {}
  default = None

  def __init__(self, *args, **kwargs):
    """
    constructor.

      :param choices: a list of hashables.
    """

    self.index_to_choice = {i: v for i, v in enumerate(self.choices)}
    self.choice_to_index = {v: k for k, v in self.index_to_choice.iteritems()}

    if self.default:
      kwargs["default"] = self.default

    super(ChoiceProperty, self).__init__(*args, **kwargs)

  def _validate(self, value):
    assert (value in self.choice_to_index.keys())

  def _to_base_type(self, value):
    """
    returns the choice corresponding to an index
    """
    return self.choice_to_index[value]

  def _from_base_type(self, value):
    """
    returns the index for a given choice
    """
    return self.index_to_choice[value]

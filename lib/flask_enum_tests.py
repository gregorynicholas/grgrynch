from __future__ import unicode_literals
from flask.ext import funktional
from app.main import flaskapp
from flask.ext import enum


class SomeEnum(enum.Enum):
  a = 0
  b = 1


class EnumTestCase(funktional.TestCase):

  flaskapp = flaskapp

  def test_enum_class(self):
    self.assertEquals(0, SomeEnum.a)
    self.assertEquals(1, SomeEnum.b)

  def test__values_attr(self):
    self.assertIn('a', SomeEnum._values)
    self.assertIn('b', SomeEnum._values)
    self.assertEquals(0, SomeEnum._values['a'])
    self.assertEquals(1, SomeEnum._values['b'])

  def test_choices_attr(self):
    choices = SomeEnum.choices()
    self.assertIsNotNone(choices)
    self.assertIsInstance(choices, list)
    self.assertEquals(2, len(choices))

    # assert `a` property..
    choice = choices[0]
    self.assertIsInstance(choice, tuple)
    self.assertEquals(choice[0], 'a')
    self.assertEquals(choice[1], 0)

    # assert `b` property..
    choice = choices[1]
    self.assertIsInstance(choice, tuple)
    self.assertEquals(choice[0], 'b')
    self.assertEquals(choice[1], 1)

  def test_values_attr(self):
    values = SomeEnum.values()
    self.assertIsNotNone(values)
    self.assertIsInstance(values, list)
    self.assertEquals(2, len(values))

    # assert `a` property..
    self.assertIsInstance(values[0], int)
    self.assertEquals(values[0], 0)

    # assert `b` property..
    self.assertIsInstance(values[1], int)
    self.assertEquals(values[1], 1)

  def test_set_attr_raises(self):
    with self.assertRaises(NotImplementedError):
      SomeEnum.a = 1

  def test_value_method(self):
    self.assertEquals(SomeEnum.value('a'), 0)

  def test_str_method(self):
    self.assertIsNotNone(str(SomeEnum))

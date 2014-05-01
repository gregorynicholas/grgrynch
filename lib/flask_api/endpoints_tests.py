#!/usr/bin/env python
from __future__ import unicode_literals
import unittest
from flask.ext import funktional
from flask import Flask, Response
from flask.ext import api
from flask.ext.api import Form, StringField


# setup..
# ---------------------------------------------------------------------------

endpoints = api.Endpoints("endpoints", __name__)


@endpoints.endpoint("/get_disabled_by_default")
def get_disabled_by_default():
  return Response("should be disabled!")


@endpoints.endpoint("/post_enabled_by_default")
def post_enabled_by_default():
  return Response("should be enabled")


class TestEndpointForm(Form):
  email = StringField()
  password = StringField()


@endpoints.endpoint("/endpoint_with_form")
@endpoints.form(TestEndpointForm)
def endpoint_with_form(form):
  return Response("endpoint with form")


class EndpointsTests(funktional.TestCase):

  def flaskapp(self):
    rv = Flask("test")
    rv.debug = True
    rv.secret_key = "666"
    rv.config["CSRF_ENABLED"] = False
    rv.register_blueprint(endpoints, url_prefix="/ep")
    return rv

  def assertEndpoint(self, endpoint):
    self.assertIn(
      "endpoints." + endpoint, self.app.view_functions,
      "the endpoint: {} is not registered on the app: {}".format(
        endpoint, self.app))
  assert_endpoint = assertEndpoint

  # test cases..
  # ---------------------------------------------------------------------------

  def test_endpoint_decorator_get_method(self):
    """
    test that the GET method is disabled by default
    """
    self.assert_endpoint("get_disabled_by_default")
    rv = self.get("endpoints.get_disabled_by_default")
    self.assertIsNotNone(rv)
    self.assert405(rv)

  def test_endpoint_decorator_post_method(self):
    """
    test that the POST method is enabled by default
    """
    self.assert_endpoint("post_enabled_by_default")
    rv = self.post("endpoints.post_enabled_by_default")
    self.assertIsNotNone(rv)
    self.assert200(rv)
    self.assertEquals(rv.data, "should be enabled")

  def test_endpoint_decorator_with_form(self):
    """
    test an endpoint definition with a form
    """
    self.assert_endpoint("endpoint_with_form")
    rv = self.post("endpoints.endpoint_with_form", data={"email": "test"})
    self.assertIsNotNone(rv)
    self.assert200(rv)
    self.assertEquals(rv.data, "endpoint with form")


if __name__ == "__main__":
  unittest.main()

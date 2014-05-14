"""
  flask.ext.api.testcase
  ~~~~~~~~~~~~~~~~~~~~~~

  test utils for Endpoint objects.


  :license: MIT, see LICENSE for more details.
  :copyright: (c) 2014 by gregorynicholas.
"""


class EndpointTestCase(object):
  """
  mixin class with helpers to test endpoints.
  """

  def assertBlueprintEndpoint(self, endpoint):
    self.assertIn(
      endpoint, self.app.view_functions,
      "the endpoint: {} is not registered on the app: {}".format(
        endpoint, self.app))
  assert_blueprint_endpoint = assertBlueprintEndpoint

  def assertEndpoint(self, api, endpoint):
    self.assertIn(
      api.name + "." + endpoint, self.app.view_functions,
      "the endpoint: {} is not registered on the app: {}".format(
        endpoint, self.app))
  assert_endpoint = assertEndpoint

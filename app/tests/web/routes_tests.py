"""
  app.tests.web.routes_tests
  ~~~~~~~~~~~~~~~~~~~~~~~~~~

  tests for the web routes.


  :copyright: (c) 2014 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals
from flask.ext import funktional_gae

from app.main import flaskapp
from app.config import config


class RoutesTestCase(funktional_gae.TestCase):
  """
  tests for the web routes.
  """

  flaskapp = flaskapp

  def test_login_page_returns_200(self):
    rv = self.get('login_get')
    self.assert200(rv)

  def test_logout_page_redirects(self):
    rv = self.get('logout_get', follow_redirects=False)
    self.assert302(rv)

  def test_admin_page_anonymous_redirects(self):
    rv = self.get('admin_get', follow_redirects=False)
    self.assert302(rv)

  def test_admin_page_logged_in_returns_200(self):
    rv = self.get('test_signin_get')
    self.assert200(rv)
    rv = self.get('admin_get', follow_redirects=False)

    rv = self.get('logout_get', follow_redirects=False)
    self.assert302(rv)

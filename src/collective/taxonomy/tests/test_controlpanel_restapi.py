from collective.taxonomy.testing import FUNCTIONAL_TESTING
from plone.app.testing import applyProfile
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing.interfaces import SITE_OWNER_NAME
from plone.app.testing.interfaces import SITE_OWNER_PASSWORD
from plone.restapi.testing import RelativeSession
from transaction import commit

import unittest


class TestControlPanelRestapi(unittest.TestCase):
    """Test JSON views."""

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()

        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        self.portal.portal_workflow.setDefaultChain("simple_publication_workflow")
        applyProfile(self.portal, "plone.app.contenttypes:plone-content")

        commit()

    def test_controlpanel_is_listed(self):
        response = self.api_session.get("/@taxonomy")

        titles = [x.get("title") for x in response.json()]
        self.assertIn("Test vocabulary", titles)

    def test_route_exists(self):
        response = self.api_session.get("/@taxonomy")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get("Content-Type"), "application/json")

    # def test_route_return_schema(self):
    #     response = self.api_session.get("/@taxonomy")

    #     self.assertIn("schema", response.json())

    def test_default_values_loaded(self):
        response = self.api_session.get("/@taxonomy")
        res = response.json()

        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["name"], "collective.taxonomy.test")
        self.assertEqual(res[0]["title"], "Test vocabulary")
        self.assertEqual(res[0]["count"], {"da": 4, "de": 1, "en": 6, "ru": 1})

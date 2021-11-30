# -*- coding: utf-8 -*-
from collective.taxonomy.testing import API_FUNCTIONAL_TESTING
from plone import api
from plone.app.testing import applyProfile
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing.interfaces import SITE_OWNER_NAME
from plone.app.testing.interfaces import SITE_OWNER_PASSWORD
from plone.restapi.testing import RelativeSession
from plone.testing.z2 import Browser
from transaction import commit

import unittest


class TestControlPanelRestapi(unittest.TestCase):
    """Test JSON views."""

    layer = API_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()

        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        self.portal.portal_workflow.setDefaultChain("simple_publication_workflow")
        applyProfile(self.portal, "plone.app.contenttypes:plone-content")

        self.document = api.content.create(
            container=self.portal, type="Document", title="Doc"
        )

        commit()

    def test_controlpanel_is_listed(self):
        response = self.api_session.get("/@controlpanels")

        titles = [x.get("title") for x in response.json()]
        self.assertIn("Taxonomies", titles)

    def test_route_exists(self):
        response = self.api_session.get("/@controlpanels/taxonomy")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get("Content-Type"), "application/json")

    def test_route_return_schema(self):
        response = self.api_session.get("/@controlpanels/taxonomy")

        self.assertIn("schema", response.json())

    def test_default_values_loaded(self):
        response = self.api_session.get("/@controlpanels/taxonomy")
        res = response.json()

        self.assertEqual(len(res["items"]), 1)
        self.assertEqual(res["items"][0]["name"], "collective.taxonomy.test")
        self.assertEqual(res["items"][0]["title"], "Test vocabulary")
        self.assertEqual(res["items"][0]["count"], {"da": 4, "de": 1, "en": 5, "ru": 1})

    def test_add_validation_fields(self):
        response = self.api_session.post(
            "/@controlpanels/taxonomy",
            json={},
        )

        self.assertEqual(response.status_code, 400)

        response = self.api_session.post(
            "/@controlpanels/taxonomy",
            json={
                "taxonomy": "new-taxonomy",
            },
        )
        self.assertEqual(response.status_code, 400)

        response = self.api_session.post(
            "/@controlpanels/taxonomy",
            json={
                "taxonomy": "new-taxonomy",
                "field_title": "new taxonomy",
            },
        )
        self.assertEqual(response.status_code, 400)

        response = self.api_session.post(
            "/@controlpanels/taxonomy",
            json={
                "taxonomy": "new-taxonomy",
                "field_title": "new taxonomy",
                "default_language": "en",
            },
        )
        self.assertEqual(response.status_code, 400)

        response = self.api_session.post(
            "/@controlpanels/taxonomy",
            json={
                "taxonomy": "new-taxonomy",
                "field_title": "new taxonomy",
                "default_language": "en",
                "is_required": False,
            },
        )
        self.assertEqual(response.status_code, 400)

        response = self.api_session.post(
            "/@controlpanels/taxonomy",
            json={
                "taxonomy": "foo",
                "field_title": "bar",
                "default_language": "en",
                "is_required": False,
                "is_single_select": True,
            },
        )
        self.assertEqual(response.status_code, 201)

    def test_add_taxonomy(self):
        response = self.api_session.post(
            "/@controlpanels/taxonomy",
            json={
                "taxonomy": "new-taxonomy",
                "field_title": "new taxonomy",
                "default_language": "en",
                "is_required": False,
                "is_single_select": True,
            },
        )
        self.assertEqual(response.status_code, 201)

        res = response.json()
        self.assertEqual(len(res["items"]), 2)
        self.assertEqual(res["items"][1]["name"], "collective.taxonomy.newtaxonomy")
        self.assertEqual(res["items"][1]["title"], "new taxonomy")

        taxonomy_response = self.api_session.get("/@controlpanels/taxonomy").json()
        self.assertEqual(res["items"], taxonomy_response["items"])

    def test_delete_taxonomy_raise_error_if_no_value_provided(self):
        response = self.api_session.delete("/@controlpanels/taxonomy")
        self.assertEqual(response.status_code, 400)

    def test_delete_taxonomy_raise_error_if_not_found(self):
        response = self.api_session.delete("/@controlpanels/taxonomy/foo")
        self.assertEqual(response.status_code, 400)

    def test_delete_taxonomy(self):
        self.api_session.post(
            "/@controlpanels/taxonomy",
            json={
                "taxonomy": "new-taxonomy",
                "field_title": "new taxonomy",
                "default_language": "en",
                "is_required": False,
                "is_single_select": True,
            },
        )
        taxonomy_response = self.api_session.get("/@controlpanels/taxonomy").json()
        self.assertEqual(len(taxonomy_response["items"]), 2)

        # now delete one
        delete_response = self.api_session.delete(
            "/@controlpanels/taxonomy/collective.taxonomy.test",
        )

        self.assertEqual(delete_response.status_code, 204)

        taxonomy_response = self.api_session.get("/@controlpanels/taxonomy").json()
        self.assertEqual(len(taxonomy_response["items"]), 1)
        self.assertEqual(taxonomy_response["items"][0]["title"], "new taxonomy")

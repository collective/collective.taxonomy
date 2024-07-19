from collective.taxonomy.testing import FUNCTIONAL_TESTING
from plone.app.testing import applyProfile
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing.interfaces import SITE_OWNER_NAME
from plone.app.testing.interfaces import SITE_OWNER_PASSWORD
from plone.restapi.testing import RelativeSession
from transaction import commit

import unittest


class TestTaxonomyEndpoint(unittest.TestCase):
    """Test JSON views."""

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()

        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.api_session = RelativeSession(self.portal_url, test=self)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        self.portal.portal_workflow.setDefaultChain("simple_publication_workflow")
        applyProfile(self.portal, "plone.app.contenttypes:plone-content")
        commit()

    def test_route_exists(self):
        response = self.api_session.get("/@taxonomy")
        self.assertEqual(response.status_code, 200)

    def test_get_without_parameters_return_all_taxonomies(self):
        response = self.api_session.get("/@taxonomy")
        res = response.json()

        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["name"], "collective.taxonomy.test")
        self.assertEqual(res[0]["title"], "Test vocabulary")
        self.assertEqual(res[0]["count"], {"da": 4, "de": 1, "en": 6, "ru": 1})

    def test_get_with_parameters_return_taxonomy_details(self):
        response = self.api_session.get("/@taxonomy/collective.taxonomy.test")
        res = response.json()

        self.assertEqual(res["name"], "collective.taxonomy.test")
        self.assertEqual(res["title"], "Test vocabulary")
        self.assertEqual(res["default_language"], "da")

    def test_add_validation_fields(self):
        response = self.api_session.post(
            "/@taxonomy",
            json={},
        )

        self.assertEqual(response.status_code, 400)

        response = self.api_session.post(
            "/@taxonomy",
            json={
                "taxonomy": "new-taxonomy",
            },
        )
        self.assertEqual(response.status_code, 400)

        response = self.api_session.post(
            "/@taxonomy",
            json={
                "taxonomy": "new-taxonomy",
                "field_title": "new taxonomy",
            },
        )
        self.assertEqual(response.status_code, 400)

        response = self.api_session.post(
            "/@taxonomy",
            json={
                "taxonomy": "new-taxonomy",
                "field_title": "new taxonomy",
                "default_language": "en",
            },
        )
        self.assertEqual(response.status_code, 201)

        response = self.api_session.post(
            "/@taxonomy",
            json={
                "taxonomy": "new-taxonomy",
                "field_title": "new taxonomy",
                "default_language": "en",
                "is_required": False,
            },
        )
        self.assertEqual(response.status_code, 201)

        response = self.api_session.post(
            "/@taxonomy",
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
            "/@taxonomy",
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
        self.assertEqual(res["name"], "collective.taxonomy.newtaxonomy")
        self.assertEqual(res["title"], "new taxonomy")

        # check that the new taxonomy is registered
        taxonomy_response = self.api_session.get("/@taxonomy").json()
        self.assertEqual(len(taxonomy_response), 2)

    def test_delete_taxonomy_return_400_if_no_name_provided(self):
        response = self.api_session.delete("/@taxonomy")
        self.assertEqual(response.status_code, 400)

    def test_delete_taxonomy_return_4040_if_not_found(self):
        response = self.api_session.delete("/@taxonomy/foo")
        self.assertEqual(response.status_code, 404)

    def test_delete_taxonomy(self):
        self.api_session.post(
            "/@taxonomy",
            json={
                "taxonomy": "new-taxonomy",
                "field_title": "new taxonomy",
                "default_language": "en",
                "is_required": False,
                "is_single_select": True,
            },
        )
        taxonomy_response = self.api_session.get("/@taxonomy").json()
        self.assertEqual(len(taxonomy_response), 2)

        # now delete one
        delete_response = self.api_session.delete(
            "/@taxonomy/collective.taxonomy.test",
        )

        self.assertEqual(delete_response.status_code, 204)

        taxonomy_response = self.api_session.get("/@taxonomy").json()
        self.assertEqual(len(taxonomy_response), 1)
        self.assertEqual(taxonomy_response[0]["title"], "new taxonomy")

    def test_get_AddTaxonomy_Schema(self):
        schema_response = self.api_session.get("/@taxonomySchema")
        response = schema_response.json()
        self.assertEqual(schema_response.status_code, 200)
        self.assertEqual(len(response["fieldsets"]), 1)
        fields = [x.get("fields") for x in response["fieldsets"]]
        self.assertIn("field_title", fields[0])
        self.assertIn("taxonomy", fields[0])
        self.assertNotEqual(response["properties"], {})

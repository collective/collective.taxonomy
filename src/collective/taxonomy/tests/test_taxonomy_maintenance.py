"""Keep the catalog and the querystring criteria in sync when a taxonomy
changes: its field prefix, or the terms of its tree."""

from collective.taxonomy.interfaces import ITaxonomy
from collective.taxonomy.testing import FUNCTIONAL_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing.interfaces import SITE_OWNER_NAME
from plone.app.testing.interfaces import SITE_OWNER_PASSWORD
from plone.restapi.testing import RelativeSession
from zope.component import queryUtility

import transaction
import unittest

NAME = "collective.taxonomy.space"
BEHAVIOR = "collective.taxonomy.generated.space"
CRITERION = "plone.app.querystring.field.{}.title"

TREE = [
    {
        "key": "mars",
        "title": "Mars",
        "children": [
            {"key": "mission", "title": "Mission", "children": []},
        ],
    },
    {"key": "venus", "title": "Venus", "children": []},
]


class TestTaxonomyMaintenance(unittest.TestCase):
    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.api_session = RelativeSession(self.portal.absolute_url())
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        response = self.api_session.post(
            "/@taxonomy",
            json={
                "taxonomy": "space",
                "field_title": "Space",
                "default_language": "en",
            },
        )
        self.assertEqual(response.status_code, 201, response.text)
        self.save_tree(TREE)

        fti = self.portal.portal_types.Document
        fti.manage_changeProperties(behaviors=tuple(fti.behaviors) + (BEHAVIOR,))
        self.doc = api.content.create(
            self.portal, type="Document", id="doc", title="Doc"
        )
        self.other = api.content.create(
            self.portal, type="Document", id="other", title="Other"
        )
        setattr(self.doc, "taxonomy_space", ["mission"])
        self.doc.reindexObject()
        transaction.commit()

    def tearDown(self):
        self.api_session.close()

    def save_tree(self, tree):
        """What volto-taxonomy sends when the tree editor is saved."""
        response = self.api_session.patch(
            f"/@taxonomy/{NAME}",
            json={
                "taxonomy": NAME,
                "title": "Space",
                "languages": ["en"],
                "tree": tree,
            },
        )
        self.assertEqual(response.status_code, 204, response.text)
        transaction.begin()

    def save_settings(self, **data):
        """What volto-taxonomy sends when the taxonomy settings are saved."""
        payload = {
            "taxonomy": NAME,
            "field_title": "Space",
            "default_language": "en",
        }
        payload.update(data)
        response = self.api_session.patch(f"/@taxonomy/{NAME}", json=payload)
        self.assertEqual(response.status_code, 204, response.text)
        transaction.begin()

    def find(self, index, key):
        catalog = api.portal.get_tool("portal_catalog")
        return sorted(b.getId for b in catalog(**{index: key}))

    def space_indexes(self):
        catalog = api.portal.get_tool("portal_catalog")
        return sorted(i for i in catalog.indexes() if i.endswith("space"))

    def has_criterion(self, field_name):
        registry = api.portal.get_tool("portal_registry")
        return CRITERION.format(field_name) in registry.records

    def test_terms_and_ancestors_are_indexed(self):
        self.assertEqual(self.find("taxonomy_space", "mission"), ["doc"])
        self.assertEqual(self.find("taxonomy_space", "mars"), ["doc"])

    def test_settings_save_with_unchanged_prefix_keeps_index_content(self):
        self.save_settings(field_prefix="taxonomy_")

        self.assertEqual(self.space_indexes(), ["taxonomy_space"])
        self.assertEqual(self.find("taxonomy_space", "mission"), ["doc"])

    def test_prefix_change_moves_index_and_criterion(self):
        self.save_settings(field_prefix="tax_")

        self.assertEqual(self.space_indexes(), ["tax_space"])
        catalog = api.portal.get_tool("portal_catalog")
        self.assertNotIn("taxonomy_space", catalog.schema())
        self.assertIn("tax_space", catalog.schema())
        self.assertFalse(self.has_criterion("taxonomy_space"))
        self.assertTrue(self.has_criterion("tax_space"))

    def test_prefix_change_keeps_assigned_terms(self):
        self.save_settings(field_prefix="tax_")

        self.assertEqual(getattr(self.portal.doc, "tax_space", None), ["mission"])
        self.assertFalse(hasattr(self.portal.doc.aq_base, "taxonomy_space"))
        self.assertEqual(self.find("tax_space", "mission"), ["doc"])
        self.assertEqual(self.find("tax_space", "mars"), ["doc"])

    def test_deleting_a_term_reindexes_content(self):
        self.save_tree(
            [
                {"key": "mars", "title": "Mars", "children": []},
                {"key": "venus", "title": "Venus", "children": []},
            ]
        )

        self.assertEqual(self.find("taxonomy_space", "mission"), [])
        self.assertEqual(self.find("taxonomy_space", "mars"), [])

    def test_moving_a_term_reindexes_content(self):
        self.save_tree(
            [
                {"key": "mars", "title": "Mars", "children": []},
                {
                    "key": "venus",
                    "title": "Venus",
                    "children": [
                        {"key": "mission", "title": "Mission", "children": []},
                    ],
                },
            ]
        )

        self.assertEqual(self.find("taxonomy_space", "mission"), ["doc"])
        self.assertEqual(self.find("taxonomy_space", "venus"), ["doc"])
        self.assertEqual(self.find("taxonomy_space", "mars"), [])

    def test_renaming_a_term_keeps_content(self):
        tree = [dict(t) for t in TREE]
        tree[0] = {
            "key": "mars",
            "title": "Red planet",
            "children": [{"key": "mission", "title": "Mission", "children": []}],
        }
        self.save_tree(tree)

        self.assertEqual(self.find("taxonomy_space", "mission"), ["doc"])
        self.assertEqual(self.find("taxonomy_space", "mars"), ["doc"])

    def test_usage_counts_terms_and_their_subtree(self):
        response = self.api_session.get(f"/@taxonomy/{NAME}")

        self.assertEqual(response.json()["usage"], {"mars": 1, "mission": 1})

    def test_usage_is_only_for_managers(self):
        # As on a Volto site, where members can use the REST API.
        self.portal.manage_permission(
            "plone.restapi: Use REST API", roles=["Member", "Manager"], acquire=True
        )
        setRoles(self.portal, TEST_USER_ID, ["Member"])
        transaction.commit()
        member = RelativeSession(self.portal.absolute_url())
        member.headers.update({"Accept": "application/json"})
        member.auth = (TEST_USER_NAME, TEST_USER_PASSWORD)
        response = member.get(f"/@taxonomy/{NAME}")
        member.close()

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("usage", response.json())


class TestTaxonomyDescription(unittest.TestCase):
    """The taxonomy description is stored, and never acquired from the site."""

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.portal.manage_changeProperties(description="The site description")
        self.api_session = RelativeSession(self.portal.absolute_url())
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        transaction.commit()

    def tearDown(self):
        self.api_session.close()

    def create(self, **data):
        payload = {
            "taxonomy": "space",
            "field_title": "Space",
            "default_language": "en",
        }
        payload.update(data)
        response = self.api_session.post("/@taxonomy", json=payload)
        self.assertEqual(response.status_code, 201, response.text)

    def test_description_is_stored(self):
        self.create(field_description="Planets and missions")

        response = self.api_session.get(f"/@taxonomy/{NAME}")

        self.assertEqual(response.json()["description"], "Planets and missions")

    def test_missing_description_is_not_acquired_from_the_site(self):
        self.create()
        # Taxonomies created before the fix have no description attribute.
        transaction.begin()
        taxonomy = queryUtility(ITaxonomy, name=NAME)
        taxonomy.__dict__.pop("description", None)
        taxonomy._p_changed = True
        transaction.commit()

        response = self.api_session.get(f"/@taxonomy/{NAME}")

        self.assertEqual(response.json()["description"], "")

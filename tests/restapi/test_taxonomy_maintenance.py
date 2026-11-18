"""Keep the catalog and the querystring criteria in sync when a taxonomy
changes: its field prefix, or the terms of its tree."""

from . import CRITERION
from . import SPACE_BEHAVIOR
from . import SPACE_NAME
from . import SPACE_TREE
from collective.taxonomy.interfaces import ITaxonomy
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from zope.component import queryUtility

import pytest
import transaction


def _find(index: str, key: str) -> list[str]:
    catalog = api.portal.get_tool("portal_catalog")
    return sorted(b.getId for b in catalog(**{index: key}))


def _space_indexes() -> list[str]:
    catalog = api.portal.get_tool("portal_catalog")
    return sorted(i for i in catalog.indexes() if i.endswith("space"))


def _has_criterion(field_name: str) -> bool:
    registry = api.portal.get_tool("portal_registry")
    return CRITERION.format(field_name) in registry.records


class TestTaxonomyMaintenance:
    @pytest.fixture(autouse=True)
    def _setup(self, portal, manager_request):
        self.portal = portal
        self.api_session = manager_request

        response = self.api_session.post(
            "/@taxonomy",
            json={
                "taxonomy": "space",
                "field_title": "Space",
                "default_language": "en",
            },
        )
        assert response.status_code == 201, response.text
        self.save_tree(SPACE_TREE)

        fti = portal.portal_types.Document
        fti.manage_changeProperties(behaviors=(*tuple(fti.behaviors), SPACE_BEHAVIOR))
        with api.env.adopt_roles(["Manager"]):
            doc = api.content.create(portal, type="Document", id="doc", title="Doc")
            api.content.create(portal, type="Document", id="other", title="Other")
        doc.taxonomy_space = ["mission"]
        doc.reindexObject()
        transaction.commit()

    def save_tree(self, tree: list[dict]) -> None:
        """What volto-taxonomy sends when the tree editor is saved."""
        response = self.api_session.patch(
            f"/@taxonomy/{SPACE_NAME}",
            json={
                "taxonomy": SPACE_NAME,
                "title": "Space",
                "languages": ["en"],
                "tree": tree,
            },
        )
        assert response.status_code == 204, response.text
        transaction.begin()

    def save_settings(self, **data) -> None:
        """What volto-taxonomy sends when the taxonomy settings are saved."""
        payload = {
            "taxonomy": SPACE_NAME,
            "field_title": "Space",
            "default_language": "en",
            **data,
        }
        response = self.api_session.patch(f"/@taxonomy/{SPACE_NAME}", json=payload)
        assert response.status_code == 204, response.text
        transaction.begin()

    def test_terms_and_ancestors_are_indexed(self):
        assert _find("taxonomy_space", "mission") == ["doc"]
        assert _find("taxonomy_space", "mars") == ["doc"]

    def test_settings_save_with_unchanged_prefix_keeps_index_content(self):
        self.save_settings(field_prefix="taxonomy_")

        assert _space_indexes() == ["taxonomy_space"]
        assert _find("taxonomy_space", "mission") == ["doc"]

    def test_prefix_change_moves_index_and_criterion(self):
        self.save_settings(field_prefix="tax_")

        assert _space_indexes() == ["tax_space"]
        catalog = api.portal.get_tool("portal_catalog")
        assert "taxonomy_space" not in catalog.schema()
        assert "tax_space" in catalog.schema()
        assert _has_criterion("taxonomy_space") is False
        assert _has_criterion("tax_space") is True

    def test_prefix_change_keeps_assigned_terms(self):
        self.save_settings(field_prefix="tax_")

        assert getattr(self.portal.doc, "tax_space", None) == ["mission"]
        assert not hasattr(self.portal.doc.aq_base, "taxonomy_space")
        assert _find("tax_space", "mission") == ["doc"]
        assert _find("tax_space", "mars") == ["doc"]

    def test_deleting_a_term_reindexes_content(self):
        self.save_tree([
            {"key": "mars", "title": "Mars", "children": []},
            {"key": "venus", "title": "Venus", "children": []},
        ])

        assert _find("taxonomy_space", "mission") == []
        assert _find("taxonomy_space", "mars") == []

    def test_moving_a_term_reindexes_content(self):
        self.save_tree([
            {"key": "mars", "title": "Mars", "children": []},
            {
                "key": "venus",
                "title": "Venus",
                "children": [
                    {"key": "mission", "title": "Mission", "children": []},
                ],
            },
        ])

        assert _find("taxonomy_space", "mission") == ["doc"]
        assert _find("taxonomy_space", "venus") == ["doc"]
        assert _find("taxonomy_space", "mars") == []

    def test_renaming_a_term_keeps_content(self):
        tree = [dict(t) for t in SPACE_TREE]
        tree[0] = {
            "key": "mars",
            "title": "Red planet",
            "children": [{"key": "mission", "title": "Mission", "children": []}],
        }
        self.save_tree(tree)

        assert _find("taxonomy_space", "mission") == ["doc"]
        assert _find("taxonomy_space", "mars") == ["doc"]

    def test_usage_counts_terms_and_their_subtree(self):
        response = self.api_session.get(f"/@taxonomy/{SPACE_NAME}")

        assert response.json()["usage"] == {"mars": 1, "mission": 1}

    def test_usage_is_only_for_managers(self, request_factory):
        # As on a Volto site, where members can use the REST API.
        self.portal.manage_permission(
            "plone.restapi: Use REST API", roles=["Member", "Manager"], acquire=True
        )
        setRoles(self.portal, TEST_USER_ID, ["Member"])
        transaction.commit()
        member = request_factory(basic_auth=(TEST_USER_NAME, TEST_USER_PASSWORD))
        response = member.get(f"/@taxonomy/{SPACE_NAME}")

        assert response.status_code == 200
        assert "usage" not in response.json()


class TestTaxonomyDescription:
    """The taxonomy description is stored, and never acquired from the site."""

    @pytest.fixture(autouse=True)
    def _setup(self, portal, manager_request):
        portal.manage_changeProperties(description="The site description")
        transaction.commit()
        self.api_session = manager_request

    def create(self, **data) -> None:
        payload = {
            "taxonomy": "space",
            "field_title": "Space",
            "default_language": "en",
            **data,
        }
        response = self.api_session.post("/@taxonomy", json=payload)
        assert response.status_code == 201, response.text

    def test_description_is_stored(self):
        self.create(field_description="Planets and missions")

        response = self.api_session.get(f"/@taxonomy/{SPACE_NAME}")

        assert response.json()["description"] == "Planets and missions"

    def test_missing_description_is_not_acquired_from_the_site(self):
        self.create()
        # Taxonomies created before the fix have no description attribute.
        transaction.begin()
        taxonomy = queryUtility(ITaxonomy, name=SPACE_NAME)
        taxonomy.__dict__.pop("description", None)
        taxonomy._p_changed = True
        transaction.commit()

        response = self.api_session.get(f"/@taxonomy/{SPACE_NAME}")

        assert response.json()["description"] == ""

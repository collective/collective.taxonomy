from . import NEW_TAXONOMY
from tests import TAXONOMY_COUNT
from tests import TAXONOMY_NAME
from tests import TAXONOMY_TITLE

import pytest


class TestTaxonomyList:
    @pytest.fixture(autouse=True)
    def _setup(self, portal, manager_request):
        self.api_session = manager_request

    def test_route_exists(self):
        response = self.api_session.get("/@taxonomy")
        assert response.status_code == 200
        assert response.headers.get("Content-Type") == "application/json"

    def test_controlpanel_is_listed(self):
        response = self.api_session.get("/@taxonomy")
        titles = [x.get("title") for x in response.json()]
        assert TAXONOMY_TITLE in titles

    def test_get_without_parameters_return_all_taxonomies(self):
        res = self.api_session.get("/@taxonomy").json()
        assert len(res) == 1
        assert res[0]["name"] == TAXONOMY_NAME
        assert res[0]["title"] == TAXONOMY_TITLE
        assert res[0]["count"] == TAXONOMY_COUNT

    def test_get_with_parameters_return_taxonomy_details(self):
        res = self.api_session.get(f"/@taxonomy/{TAXONOMY_NAME}").json()
        assert res["name"] == TAXONOMY_NAME
        assert res["title"] == TAXONOMY_TITLE
        assert res["default_language"] == "da"


class TestTaxonomyAdd:
    @pytest.fixture(autouse=True)
    def _setup(self, portal, manager_request):
        self.api_session = manager_request

    @pytest.mark.parametrize(
        "payload,status_code",
        [
            ({}, 400),
            ({"taxonomy": "new-taxonomy"}, 400),
            ({"taxonomy": "new-taxonomy", "field_title": "new taxonomy"}, 400),
            (
                {
                    "taxonomy": "new-taxonomy",
                    "field_title": "new taxonomy",
                    "default_language": "en",
                },
                201,
            ),
            (
                {
                    "taxonomy": "new-taxonomy",
                    "field_title": "new taxonomy",
                    "default_language": "en",
                    "is_required": False,
                },
                201,
            ),
            (
                {
                    "taxonomy": "foo",
                    "field_title": "bar",
                    "default_language": "en",
                    "is_required": False,
                    "is_single_select": True,
                },
                201,
            ),
        ],
    )
    def test_add_validation_fields(self, payload: dict, status_code: int):
        response = self.api_session.post("/@taxonomy", json=payload)
        assert response.status_code == status_code

    def test_add_taxonomy(self):
        response = self.api_session.post("/@taxonomy", json=NEW_TAXONOMY)
        assert response.status_code == 201

        res = response.json()
        assert res["name"] == "collective.taxonomy.newtaxonomy"
        assert res["title"] == "new taxonomy"

        # check that the new taxonomy is registered
        assert len(self.api_session.get("/@taxonomy").json()) == 2


class TestTaxonomyDelete:
    @pytest.fixture(autouse=True)
    def _setup(self, portal, manager_request):
        self.api_session = manager_request

    def test_delete_taxonomy_return_400_if_no_name_provided(self):
        response = self.api_session.delete("/@taxonomy")
        assert response.status_code == 400

    def test_delete_taxonomy_return_404_if_not_found(self):
        response = self.api_session.delete("/@taxonomy/foo")
        assert response.status_code == 404

    def test_delete_taxonomy(self):
        self.api_session.post("/@taxonomy", json=NEW_TAXONOMY)
        assert len(self.api_session.get("/@taxonomy").json()) == 2

        delete_response = self.api_session.delete(f"/@taxonomy/{TAXONOMY_NAME}")
        assert delete_response.status_code == 204

        taxonomies = self.api_session.get("/@taxonomy").json()
        assert len(taxonomies) == 1
        assert taxonomies[0]["title"] == "new taxonomy"


class TestTaxonomySchema:
    def test_get_add_taxonomy_schema(self, portal, manager_request):
        schema_response = manager_request.get("/@taxonomySchema")
        assert schema_response.status_code == 200
        response = schema_response.json()
        assert len(response["fieldsets"]) == 1
        fields = response["fieldsets"][0]["fields"]
        assert "field_title" in fields
        assert "taxonomy" in fields
        assert response["properties"] != {}

from collective.taxonomy.testing import INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing.helpers import login
from plone.app.testing.interfaces import TEST_USER_NAME

import json
import unittest


class TestJson(unittest.TestCase):
    """Test JSON views."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        super().setUp()
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_generate_json(self):
        login(self.portal, TEST_USER_NAME)
        import_json_view = self.portal.restrictedTraverse("@@taxonomy-import")
        input_data = [
            {
                "key": "animals",
                "translations": {"fr": "Animaux", "en": "Animals"},
                "subnodes": [],
            },
            {
                "key": "plants",
                "translations": {"fr": "Végétaux", "en": "Plants"},
                "subnodes": [],
            },
        ]
        output = import_json_view.generate_data_for_taxonomy(input_data, "fr")
        self.assertEqual(
            output, [("\u241fAnimaux", "animals"), ("\u241fVégétaux", "plants")]
        )

        input_data[0]["subnodes"] = [
            {
                "key": "birds",
                "translations": {"fr": "Oiseaux", "en": "Birds"},
                "subnodes": [
                    {
                        "key": "eagles",
                        "translations": {"fr": "Aigles", "en": "Eagles"},
                        "subnodes": [],
                    },
                    {
                        "key": "penguins",
                        "translations": {"fr": "Manchots", "en": "Penguins"},
                        "subnodes": [],
                    },
                ],
            },
            {
                "key": "mammals",
                "translations": {"fr": "Mammifères", "en": "Mammals"},
                "subnodes": [
                    {
                        "key": "cows",
                        "translations": {"fr": "Vaches", "en": "Cows"},
                        "subnodes": [],
                    },
                    {
                        "key": "lions",
                        "translations": {"fr": "Lions", "en": "Lions"},
                        "subnodes": [],
                    },
                ],
            },
            {
                "key": "reptiles",
                "translations": {"fr": "Reptiles", "en": "Reptiles"},
                "subnodes": [
                    {
                        "key": "pythons",
                        "translations": {"fr": "Pythons", "en": "Pythons"},
                        "subnodes": [],
                    },
                ],
            },
        ]
        output = import_json_view.generate_data_for_taxonomy(input_data, "fr")
        self.assertEqual(
            output,
            [
                ("\u241fAnimaux", "animals"),
                ("\u241fAnimaux\u241fOiseaux", "birds"),
                ("\u241fAnimaux\u241fOiseaux\u241fAigles", "eagles"),
                ("\u241fAnimaux\u241fOiseaux\u241fManchots", "penguins"),
                ("\u241fAnimaux\u241fMammifères", "mammals"),
                ("\u241fAnimaux\u241fMammifères\u241fVaches", "cows"),
                ("\u241fAnimaux\u241fMammifères\u241fLions", "lions"),
                ("\u241fAnimaux\u241fReptiles", "reptiles"),
                ("\u241fAnimaux\u241fReptiles\u241fPythons", "pythons"),
                ("\u241fVégétaux", "plants"),
            ],
        )


class TestEditDataJson(unittest.TestCase):
    """Test Edit Data JSON view."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        super().setUp()
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        login(self.portal, TEST_USER_NAME)
        self.request.set("taxonomy", "collective.taxonomy.test")
        self.view = self.portal.restrictedTraverse("@@taxonomy-edit-data")

    def test_get_data(self):
        data = json.loads(self.view.get_data())
        self.assertEqual(
            {
                "default_language": "da",
                "key": "0",
                "name": "collective.taxonomy.test",
                "subnodes": [
                    {
                        "key": "1",
                        "subnodes": [
                            {
                                "key": "2",
                                "subnodes": [
                                    {
                                        "key": "4",
                                        "subnodes": [],
                                        "translations": {"da": "Hest"},
                                    }
                                ],
                                "translations": {
                                    "da": "Bogsamling",
                                    "en": "Book Collecting",
                                },
                            },
                            {
                                "key": "3",
                                "subnodes": [],
                                "translations": {"da": "Kronologi", "en": "Chronology"},
                            },
                        ],
                        "translations": {
                            "da": "Informationsvidenskab",
                            "de": "Informatik",
                            "en": "Information Science",
                            "ru": "Информатику",
                        },
                    }
                ],
                "title": "Test vocabulary",
            },
            data,
        )

    def test_get_languages_mapping(self):
        data = json.loads(self.view.get_languages_mapping())
        self.assertEqual(
            {"da": "Dansk", "de": "Deutsch", "en": "English", "ru": "Русский"}, data
        )

    def test_get_resource_url(self):
        url = self.view.get_resource_url()
        self.assertEqual(
            "http://nohost/plone/++resource++taxonomy/js/edittaxonomydata.js", url
        )

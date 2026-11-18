from tests import path
from tests import TAXONOMY_NAME

import json
import pytest


ANIMALS_AND_PLANTS = [
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

ANIMAL_SUBNODES = [
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


@pytest.mark.portal(roles=["Manager"])
class TestImportJson:
    @pytest.fixture(autouse=True)
    def _setup(self, portal):
        self.view = portal.restrictedTraverse("@@taxonomy-import")

    def test_generate_flat_data(self):
        output = self.view.generate_data_for_taxonomy(ANIMALS_AND_PLANTS, "fr")
        assert output == [
            (path("Animaux"), "animals"),
            (path("Végétaux"), "plants"),
        ]

    def test_generate_nested_data(self):
        data = [dict(node) for node in ANIMALS_AND_PLANTS]
        data[0]["subnodes"] = ANIMAL_SUBNODES
        output = self.view.generate_data_for_taxonomy(data, "fr")
        assert output == [
            (path("Animaux"), "animals"),
            (path("Animaux", "Oiseaux"), "birds"),
            (path("Animaux", "Oiseaux", "Aigles"), "eagles"),
            (path("Animaux", "Oiseaux", "Manchots"), "penguins"),
            (path("Animaux", "Mammifères"), "mammals"),
            (path("Animaux", "Mammifères", "Vaches"), "cows"),
            (path("Animaux", "Mammifères", "Lions"), "lions"),
            (path("Animaux", "Reptiles"), "reptiles"),
            (path("Animaux", "Reptiles", "Pythons"), "pythons"),
            (path("Végétaux"), "plants"),
        ]


@pytest.mark.portal(roles=["Manager"])
class TestEditDataJson:
    @pytest.fixture(autouse=True)
    def _setup(self, portal, http_request):
        http_request.set("taxonomy", TAXONOMY_NAME)
        self.portal_url = portal.absolute_url()
        self.view = portal.restrictedTraverse("@@taxonomy-edit-data")

    def test_get_data(self):
        data = json.loads(self.view.get_data())
        assert data == {
            "default_language": "da",
            "key": "0",
            "name": TAXONOMY_NAME,
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
        }

    def test_get_languages_mapping(self):
        data = json.loads(self.view.get_languages_mapping())
        assert data == {
            "da": "Dansk",
            "de": "Deutsch",
            "en": "English",
            "ru": "Русский",
        }

    def test_get_resource_url(self):
        url = self.view.get_resource_url()
        assert url == f"{self.portal_url}/++resource++taxonomy/js/edittaxonomydata.js"

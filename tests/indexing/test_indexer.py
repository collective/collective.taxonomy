from plone.app.querystring.interfaces import IQuerystringRegistryReader
from plone.registry.interfaces import IRegistry
from tests import path
from tests import TAXONOMY_INDEX
from zope.component import queryUtility

import pytest


class TestIndexer:
    @pytest.fixture(autouse=True)
    def _setup(self, taxonomy, catalog, document, folder, notify_field_added):
        self.data = taxonomy.data["en"]
        self.catalog = catalog
        self.document = document
        self.folder = folder
        self.notify_field_added = notify_field_added

    def count(self, value: str) -> int:
        return len(self.catalog({TAXONOMY_INDEX: value}))

    def test_indexer_with_field(self):
        self.notify_field_added()
        index = self.catalog.Indexes[TAXONOMY_INDEX]
        assert index.numObjects() == 0

        self.document.taxonomy_test = []
        self.document.reindexObject()
        assert self.count("1") == 0

        taxo_val = self.data[path("Information Science", "Chronology")]
        self.document.taxonomy_test = [taxo_val]
        self.document.reindexObject()
        assert self.count("1") == 1
        assert self.catalog.Indexes[TAXONOMY_INDEX].numObjects() == 1

        self.document.taxonomy_test = set(taxo_val)
        self.document.reindexObject()
        assert self.catalog.Indexes[TAXONOMY_INDEX].numObjects() == 1

    def test_multilanguage_indexer(self):
        self.notify_field_added()
        taxo_val = self.data[path("Information Science", "Sport")]
        self.document.taxonomy_test = [taxo_val]
        self.document.reindexObject()
        assert self.count("5") == 1

    def test_index_single_select(self):
        self.notify_field_added()
        taxo_val = self.data[path("Information Science", "Carson")]
        self.document.taxonomy_test = taxo_val
        self.document.reindexObject()
        assert self.count("5") == 0
        # not Cars ...
        assert self.count("55") == 0
        # ... but Carson
        assert self.count("56") == 1

    def test_indexer_with_property(self, monkeypatch):
        index = self.catalog.Indexes[TAXONOMY_INDEX]
        assert index.numObjects() == 0

        # Override the field with a property. A real class would define the
        # property itself; monkeypatch removes it again after the test.
        taxo_val = self.data[path("Information Science", "Book Collecting")]
        # ``__class__``, not ``type()``: the folder is an Acquisition wrapper.
        monkeypatch.setattr(
            self.folder.__class__,
            TAXONOMY_INDEX,
            property(lambda self: taxo_val),
            raising=False,
        )

        self.folder.reindexObject()
        assert self.count("2") == 1
        assert self.catalog.Indexes[TAXONOMY_INDEX].numObjects() == 1

    def test_indexer_keeps_metadata_order(self):
        """The metadata column keeps the order the terms were added in."""
        self.notify_field_added()

        # The order of 3 and 5 is lexicographic in the Taxonomy list (see
        # nihms.xml); set them the other way around, because the user wants
        # the selected taxonomies shown in that specific order.
        self.document.taxonomy_test = ["5", "3"]
        self.document.reindexObject()

        brains = self.catalog.searchResults(portal_type="Document", id=self.document.id)
        assert len(brains) == 1
        brain_taxonomy_test = brains[0].taxonomy_test

        assert len(self.document.taxonomy_test) <= len(brain_taxonomy_test)
        for value in self.document.taxonomy_test:
            assert value in brain_taxonomy_test
            # The position in the brain can be later than on the document,
            # because the indexer also adds the parents of each term to the
            # index and to the metadata.
            assert self.document.taxonomy_test.index(
                value
            ) <= brain_taxonomy_test.index(value)


def test_querystring_widget(portal):
    registry = queryUtility(IRegistry)
    config = IQuerystringRegistryReader(registry)()
    assert sorted(config["indexes"][TAXONOMY_INDEX]["values"].items()) == [
        ("1", {"title": "Information Science"}),
        ("2", {"title": "Information Science » Book Collecting"}),
        ("3", {"title": "Information Science » Chronology"}),
        ("5", {"title": "Information Science » Sport"}),
        ("55", {"title": "Information Science » Cars"}),
        ("56", {"title": "Information Science » Carson"}),
    ]

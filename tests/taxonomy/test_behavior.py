from plone import api
from plone.app.querystring.interfaces import IQueryField
from plone.behavior.interfaces import IBehavior
from plone.dexterity.interfaces import IDexterityContent
from plone.indexer.interfaces import IIndexer
from plone.registry.interfaces import IRegistry
from Products.ZCatalog.interfaces import IZCatalog
from tests import TAXONOMY_INDEX
from zope.component import queryUtility
from zope.component.hooks import getSiteManager

import pytest


QUERYSTRING_PREFIX = f"plone.app.querystring.field.{TAXONOMY_INDEX}"


def _indexer():
    """The indexer adapter registered for the taxonomy field, or None."""
    return getSiteManager()._adapter_registrations.get(
        ((IDexterityContent, IZCatalog), IIndexer, TAXONOMY_INDEX), None
    )


class TestBehaviorRegistration:
    @pytest.fixture(autouse=True)
    def _setup(self, taxonomy):
        self.taxonomy = taxonomy
        self.catalog = api.portal.get_tool("portal_catalog")
        self.registry = queryUtility(IRegistry)

    def test_register_behavior(self):
        behavior = queryUtility(IBehavior, name=self.taxonomy.getGeneratedName())
        assert behavior is not None
        assert TAXONOMY_INDEX in self.catalog.indexes()
        assert _indexer() is not None
        assert self.registry is not None
        records = self.registry.forInterface(IQueryField, prefix=QUERYSTRING_PREFIX)
        assert records is not None

    def test_unregister_behavior(self):
        self.taxonomy.unregisterBehavior()

        assert queryUtility(IBehavior, name=self.taxonomy.getGeneratedName()) is None
        assert TAXONOMY_INDEX not in self.catalog.indexes()
        assert _indexer() is None
        assert self.registry is not None
        with pytest.raises(KeyError):
            self.registry.forInterface(IQueryField, prefix=QUERYSTRING_PREFIX)

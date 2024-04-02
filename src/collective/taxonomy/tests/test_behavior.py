from collective.taxonomy.interfaces import ITaxonomy
from collective.taxonomy.testing import INTEGRATION_TESTING
from plone import api
from plone.app.querystring.interfaces import IQueryField
from plone.behavior.interfaces import IBehavior
from plone.dexterity.interfaces import IDexterityContent
from plone.indexer.interfaces import IIndexer
from plone.registry.interfaces import IRegistry
from Products.ZCatalog.interfaces import IZCatalog
from zope.component import queryUtility
from zope.component.hooks import getSiteManager

import unittest


class TestBehaviorRegistration(unittest.TestCase):
    layer = INTEGRATION_TESTING

    def test_register_behavior(self):
        # Test taxonomy registration
        taxonomy = queryUtility(ITaxonomy, name="collective.taxonomy.test")
        self.assertIsNotNone(taxonomy)

        # Test behavior registration
        behavior = queryUtility(IBehavior, name=taxonomy.getGeneratedName())
        self.assertIsNotNone(behavior)

        # Test index creation
        pc = api.portal.get_tool("portal_catalog")
        self.assertIn("taxonomy_test", pc.indexes())

        # Test indexer registration
        sm = getSiteManager()
        indexer = sm._adapter_registrations.get(
            ((IDexterityContent, IZCatalog), IIndexer, "taxonomy_test"), None
        )
        self.assertIsNotNone(indexer)

        # Test querystring configuration
        registry = queryUtility(IRegistry)
        self.assertIsNotNone(registry)
        prefix = "plone.app.querystring.field.taxonomy_test"
        records = registry.forInterface(IQueryField, prefix=prefix)  # noqa
        self.assertIsNotNone(records)

    def test_unregister_behavior(self):
        # Test taxonomy registration
        taxonomy = queryUtility(ITaxonomy, name="collective.taxonomy.test")
        self.assertIsNotNone(taxonomy)

        # Unregister behavior
        taxonomy.unregisterBehavior()

        # Test behavior registration
        behavior = queryUtility(IBehavior, name=taxonomy.getGeneratedName())
        self.assertIsNone(behavior)

        # Test index creation
        pc = api.portal.get_tool("portal_catalog")
        self.assertNotIn("taxonomy_test", pc.indexes())

        # Test indexer registration
        sm = getSiteManager()
        indexer = sm._adapter_registrations.get(
            ((IDexterityContent, IZCatalog), IIndexer, "taxonomy_test"), None
        )
        self.assertIsNone(indexer)

        # Test querystring configuration
        registry = queryUtility(IRegistry)
        self.assertIsNotNone(registry)
        prefix = "plone.app.querystring.field.taxonomy_test"
        self.assertRaises(
            KeyError, registry.forInterface, IQueryField, prefix=prefix
        )  # noqa

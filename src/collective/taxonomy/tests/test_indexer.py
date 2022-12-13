# -*- coding: utf-8 -*-
from collective.taxonomy.interfaces import ITaxonomy
from collective.taxonomy.testing import INTEGRATION_TESTING
from plone import api
from plone.app.querystring.interfaces import IQuerystringRegistryReader
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.registry.interfaces import IRegistry
from plone.schemaeditor.utils import FieldAddedEvent
from plone.schemaeditor.utils import FieldRemovedEvent
from plone.schemaeditor.utils import IEditableSchema
from zope import schema
from zope.component import queryUtility
from zope.event import notify
from zope.lifecycleevent import ObjectAddedEvent
from zope.lifecycleevent import ObjectRemovedEvent

import unittest


class TestIndexer(unittest.TestCase):

    """Test JSON views."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.portal.invokeFactory("Document", "doc1", title="Doc", language="en")
        self.document = self.portal.doc1

        # add computed taxonomy field to Document schema
        self.taxonomy_test = schema.Set(
            title="taxonomy_test",
            description="taxonomy description schema",
            required=False,
            value_type=schema.Choice(vocabulary="collective.taxonomy.taxonomies"),
        )

        portal_types = api.portal.get_tool("portal_types")
        self.fti = portal_types.get("Document")
        self.document_schema = self.fti.lookupSchema()
        self.schemaeditor = IEditableSchema(self.document_schema)
        self.schemaeditor.addField(self.taxonomy_test, name="taxonomy_test")
        notify(ObjectAddedEvent(self.taxonomy_test, self.document_schema))
        notify(FieldAddedEvent(self.fti, self.taxonomy_test))

    def tearDown(self):
        portal = self.layer["portal"]
        portal.manage_delObjects(
            [
                "doc1",
            ]
        )
        self.schemaeditor.removeField("taxonomy_test")
        notify(ObjectRemovedEvent(self.taxonomy_test, self.document_schema))
        notify(FieldRemovedEvent(self.fti, self.taxonomy_test))

    def test_indexer_with_field(self):
        portal_catalog = api.portal.get_tool("portal_catalog")
        utility = queryUtility(ITaxonomy, name="collective.taxonomy.test")
        taxonomy = utility.data
        index = portal_catalog.Indexes["taxonomy_test"]
        self.assertEqual(index.numObjects(), 0)

        self.document.taxonomy_test = []
        self.document.reindexObject()
        query = {}
        query["taxonomy_test"] = "1"
        self.assertEqual(len(portal_catalog(query)), 0)

        taxo_val = taxonomy["en"]["\u241fInformation Science\u241fChronology"]
        self.document.taxonomy_test = [taxo_val]
        self.document.reindexObject()
        self.assertEqual(len(portal_catalog(query)), 1)
        index = portal_catalog.Indexes["taxonomy_test"]
        self.assertEqual(index.numObjects(), 1)

        self.document.taxonomy_test = set(taxo_val)
        self.document.reindexObject()
        index = portal_catalog.Indexes["taxonomy_test"]
        self.assertEqual(index.numObjects(), 1)

    def test_multilanguage_indexer(self):
        portal_catalog = api.portal.get_tool("portal_catalog")
        utility = queryUtility(ITaxonomy, name="collective.taxonomy.test")
        taxonomy = utility.data
        query = {}
        query["taxonomy_test"] = "5"
        taxo_val = taxonomy["en"]["\u241fInformation Science\u241fSport"]
        self.document.taxonomy_test = [taxo_val]
        self.document.reindexObject()
        self.assertEqual(len(portal_catalog(query)), 1)

    def test_querystring_widget(self):
        registry = queryUtility(IRegistry)
        config = IQuerystringRegistryReader(registry)()
        self.assertEqual(
            sorted(config["indexes"]["taxonomy_test"]["values"].items()),
            [
                ("1", {"title": "Information Science"}),
                ("2", {"title": "Information Science \xbb Book Collecting"}),
                ("3", {"title": "Information Science \xbb Chronology"}),
                ("5", {"title": "Information Science \xbb Sport"}),
                ("55", {"title": "Information Science \xbb Cars"}),
            ],
        )

    def test_index_single_select(self):
        portal_catalog = api.portal.get_tool("portal_catalog")
        utility = queryUtility(ITaxonomy, name="collective.taxonomy.test")
        taxonomy = utility.data
        taxo_val = taxonomy["en"]["\u241fInformation Science\u241fCars"]
        self.document.taxonomy_test = taxo_val
        self.document.reindexObject()
        self.assertEqual(len(portal_catalog({"taxonomy_test": "5"})), 0)
        self.assertEqual(len(portal_catalog({"taxonomy_test": "55"})), 1)

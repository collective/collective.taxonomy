# -*- coding: utf-8 -*-
from collective.taxonomy.testing import INTEGRATION_TESTING
from collective.taxonomy.interfaces import ITaxonomy
from plone import api
from plone.app.testing import applyProfile
from plone.schemaeditor.utils import FieldAddedEvent
from plone.schemaeditor.utils import IEditableSchema
from zope import schema
from zope.component import queryUtility
from zope.event import notify
from zope.lifecycleevent import ObjectAddedEvent
import unittest


class TestIndexer(unittest.TestCase):

    """Test JSON views."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.portal.portal_workflow.setDefaultChain(
            'simple_publication_workflow')
        applyProfile(self.portal, 'plone.app.contenttypes:plone-content')
        self.document = api.content.create(
            container=self.portal, type='Document', title='Doc')

    def test_indexer_with_field(self):
        portal_catalog = api.portal.get_tool('portal_catalog')
        utility = queryUtility(ITaxonomy, name='collective.taxonomy.test')
        taxonomy = utility.data
        taxonomy_test = schema.Set(
            title=u"taxonomy_test",
            description=u"taxonomy description schema",
            required=False,
            value_type=schema.Choice(
                vocabulary=u"collective.taxonomy.taxonomies"),
        )
        portal_types = api.portal.get_tool('portal_types')
        fti = portal_types.get('Document')
        document_schema = fti.lookupSchema()
        schemaeditor = IEditableSchema(document_schema)
        schemaeditor.addField(taxonomy_test, name='taxonomy_test')
        notify(ObjectAddedEvent(taxonomy_test, document_schema))
        notify(FieldAddedEvent(fti, taxonomy_test))

        index = portal_catalog.Indexes['taxonomy_test']
        self.assertEqual(index.numObjects(), 0)

        self.document.taxonomy_test = []
        self.document.reindexObject()
        query = {}
        query['taxonomy_test'] = '1'
        self.assertEqual(len(portal_catalog(query)), 0)

        simple_tax = [val for val in taxonomy['en'].values()]
        taxo_val = simple_tax[0]
        self.document.taxonomy_test = [taxo_val]
        self.document.reindexObject()
        self.assertEqual(len(portal_catalog(query)), 1)
        index = portal_catalog.Indexes['taxonomy_test']
        self.assertEqual(index.numObjects(), 1)

        self.document.taxonomy_test = set(taxo_val)
        self.document.reindexObject()
        index = portal_catalog.Indexes['taxonomy_test']
        self.assertEqual(index.numObjects(), 1)

# -*- coding: utf-8 -*-

from BTrees.OOBTree import OOBTree
from OFS.SimpleItem import SimpleItem

from zope.component import getMultiAdapter, queryUtility, getUtility
from zope.component.hooks import getSite
from zope.interface import implements

from Products.CMFCore.utils import getToolByName
from Products.PluginIndexes.KeywordIndex.KeywordIndex import KeywordIndex
from Products.ZCatalog.Catalog import CatalogError
from Products.ZCatalog.interfaces import IZCatalog

from plone.behavior.interfaces import IBehavior
from plone.dexterity.interfaces import IDexterityFTI, IDexterityContent
from plone.memoize import ram
from plone.registry.interfaces import IRegistry
from plone.registry import Record, field
from plone.indexer.interfaces import IIndexer

from persistent.dict import PersistentDict

from .behavior import TaxonomyBehavior
from .indexer import TaxonomyIndexer
from .interfaces import ITaxonomy
from .vocabulary import Vocabulary

import logging
logger = logging.getLogger("collective.taxonomy")


class Taxonomy(SimpleItem):
    implements(ITaxonomy)

    def __init__(self, name, title):
        super(Taxonomy, self).__init__(self)
        self.data = PersistentDict()
        self.name = name
        self.title = title

    def __call__(self, context):
        current_language = self.getCurrentLanguage()
        data = self.data[current_language]
        inverted_data = self.inverted_data[current_language]
        return Vocabulary(self.name, data, inverted_data)

    @property
    @ram.cache(lambda method, self: self.data._p_mtime)
    def inverted_data(self):
        inv_data = {}
        for (language, elements) in self.data.items():
            inv_data[language] = {}
            for (path, identifier) in elements.items():
                inv_data[language][identifier] = path
        return inv_data

    def getShortName(self):
        return self.name.split('.')[-1]

    def getCurrentLanguage(self):
        context = getSite()
        portal_state = getMultiAdapter((context.aq_parent,
                                        context.aq_parent.REQUEST),
                                       name=u'plone_portal_state')
        return portal_state.language().split('-', 1)[0]

    def registerBehavior(self, field_name, field_title='',
                         field_description='', is_required=False,
                         multi_select=False):
        context = getSite()
        sm = context.getSiteManager()
        behavior = TaxonomyBehavior(self.name, self.title,
                                    field_name, field_title,
                                    field_description, is_required,
                                    multi_select)

        sm.registerUtility(behavior, IBehavior,
                           name='collective.taxonomy.generated.' +
                                self.getShortName())

        sm.registerAdapter(
            TaxonomyIndexer(field_name, self.name),
            (IDexterityContent, IZCatalog),
            IIndexer, name=field_name)

        catalog = getToolByName(context, 'portal_catalog')

        idx_object = KeywordIndex(str(field_name))
        try:
            catalog.addIndex(field_name, idx_object)
        except CatalogError:
            logging.info("Index " + field_name +
                         " already exists, we hope it is proper configured")

        registry = getUtility(IRegistry)
        prefix = 'plone.app.querystring.field.' + field_name

        def add(name, value):
            registry.records[prefix + '.' + name] = value

        add('title', Record(field.TextLine(), unicode(field_name)))
        add('enabled', Record(field.Bool(), True))
        add('group', Record(field.TextLine(), unicode('Taxonomy')))
        add('operations', Record(field.List(),
            ['plone.app.querystring.operation.selection.is']))
        add('vocabulary', Record(field.TextLine(), unicode(self.name)))
        add('sortable', Record(field.Bool(), True))
        add('description', Record(field.Text(), unicode('')))

    def unregisterBehavior(self):
        context = getSite()
        sm = context.getSiteManager()
        behavior_name = 'collective.taxonomy.generated.' + self.getShortName()
        utility = queryUtility(IBehavior, name=behavior_name)
        if utility is None:
            logging.info("It looks like the behavior was already removed.")
            return

        field_name = utility.field_name
        if utility:
            sm.unregisterUtility(utility, IBehavior, name=behavior_name)

        sm.unregisterAdapter(TaxonomyIndexer, (IDexterityContent, IZCatalog),
                             IIndexer, name=field_name)

        catalog = getToolByName(context, 'portal_catalog')
        try:
            catalog.delIndex(field_name)
        except CatalogError:
            logging.info("Could not delete index " + field_name +
                         " something is not right..")

        registry = getUtility(IRegistry)
        prefix = 'plone.app.querystring.field.' + field_name
        for suffix in ('title', 'enabled', 'group',
                       'operations', 'vocabulary', 'sortable', 'description'):
            record_name = prefix + '.' + suffix
            if record_name in registry.records:
                del registry.records[record_name]

        for (name, fti) in sm.getUtilitiesFor(IDexterityFTI):
            if behavior_name in fti.behaviors:
                fti.behaviors = [behavior for behavior in
                                 fti.behaviors
                                 if behavior != behavior_name]

    def add(self, language, identifier, path):
        if not language in self.data:
            self.data[language] = OOBTree()

        self.data[language][path] = identifier

    def translate(self, msgid, mapping=None, context=None,
                  target_language=None, default=None):

        if target_language is None:
            target_language = self.getCurrentLanguage
        if target_language not in self.inverted_data:
            raise Exception("Target language is not defined")
        if int(msgid) not in self.inverted_data[target_language]:
            raise Exception("Translation not found")

        path = self.inverted_data[target_language][int(msgid)]
        pretty_path = path[1:].replace('/', u' » ')

        return pretty_path

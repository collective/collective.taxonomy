# -*- coding: utf-8 -*-

from BTrees.OOBTree import OOBTree
from OFS.SimpleItem import SimpleItem

from zope.component import getMultiAdapter, queryUtility, getUtility
from zope.component.hooks import getSite
from zope.interface import implements

from Products.CMFCore.utils import getToolByName
from Products.PluginIndexes.FieldIndex.FieldIndex import FieldIndex
from Products.ZCatalog.Catalog import CatalogError

from plone.behavior.interfaces import IBehavior
from plone.registry.interfaces import IRegistry
from plone.registry import Record, field

from persistent.dict import PersistentDict

from .behavior import TaxonomyBehavior
from .interfaces import ITaxonomy
from .vocabulary import Vocabulary


class Taxonomy(SimpleItem):
    implements(ITaxonomy)

    def __init__(self, name, title):
        super(Taxonomy, self).__init__(self)
        self.data = PersistentDict()
        self._v_inv_data = {}

        self.name = name
        self.title = title

    def __setstate__(self, state):
        super(Taxonomy, self).__setstate__(state)
        self._v_inv_data = {}
        for language in self.data.keys():
            for (path, identifier) in self.data[language].items():
                if language not in self._v_inv_data:
                    self._v_inv_data[language] = {}
                self._v_inv_data[language][identifier] = path

    def __call__(self, context):
        current_language = self.getCurrentLanguage()
        data = self.data[current_language]
        inv_data = self._v_inv_data[current_language]
        return Vocabulary(self.name, data, inv_data)

    def getShortName(self):
        return self.name.split('.')[-1]

    def getCurrentLanguage(self):
        context = getSite()
        portal_state = getMultiAdapter((context.aq_parent,
                                        context.aq_parent.REQUEST),
                                       name=u'plone_portal_state')
        (language_major, language_minor ) = \
            portal_state.language().split('-', 1)
        return language_major

    def registerBehavior(self, field_name, field_title='',
                         field_description='', is_required=False):
        """ Creating behaviour and register it as utility """
        context = getSite()
        sm = context.getSiteManager()
        behavior = TaxonomyBehavior(self.name, self.title,
                                    field_name, field_title,
                                    field_description, is_required)

        sm.registerUtility(behavior, IBehavior,
                           name='collective.taxonomy.generated.' +
                                self.getShortName())

        """ Adding catalog """
        catalog = getToolByName(context, 'portal_catalog')
        field_idx_object = FieldIndex(str(field_name))
        try:
            catalog.addIndex(field_name, field_idx_object)
        except CatalogError:
            pass

        """ Making the index usuable for collections """
        registry = getUtility(IRegistry)
        prefix = 'plone.app.querystring.field.' + field_name

        registry.records[prefix + '.title'] = \
            Record(field.TextLine(), unicode(field_name))
        registry.records[prefix + '.enabled'] = \
            Record(field.Bool(), True)
        registry.records[prefix + '.group'] = \
            Record(field.TextLine(), unicode('Taxonomy'))
        registry.records[prefix + '.operations'] = \
            Record(field.List(),
                   ['plone.app.querystring.operation.selection.is'])
        registry.records[prefix + '.vocabulary'] = \
            Record(field.TextLine(), unicode(self.name))
        registry.records[prefix + '.sortable'] = \
            Record(field.Bool(), True)
        registry.records[prefix + '.description'] = \
            Record(field.Text(), unicode(''))

    def unregisterBehavior(self):
        """ Unregister behavior """
        context = getSite()
        sm = context.getSiteManager()
        behavior_name = 'collective.taxonomy.generated.' + self.getShortName()
        utility = queryUtility(IBehavior, name=behavior_name)
        field_name = utility.field_name
        if utility:
            sm.unregisterUtility(utility, IBehavior, name=behavior_name)

        """ Deleting the index """
        catalog = getToolByName(context, 'portal_catalog')
        try:
            catalog.delIndex(field_name)
        except CatalogError:
            pass

        """ Deleting the registry entries """
        registry = getUtility(IRegistry)
        prefix = 'plone.app.querystring.field.' + field_name
        for suffix in ['title', 'enabled', 'group',
                       'operations', 'vocabulary', 'sortable', 'description']:
            if prefix + '.' + suffix in registry.records:
                del registry.records[prefix + '.' + suffix]

    def add(self, language, identifier, path):
        if not language in self.data:
            self.data[language] = OOBTree()
        if not language in self._v_inv_data:
            self._v_inv_data[language] = OOBTree()

        self.data[language][path] = identifier
        self._v_inv_data[language][identifier] = path

    def translate(self, msgid, mapping=None, context=None,
                  target_language=None, default=None):
        if target_language is None:
            target_language = self.getCurrentLanguage
        if target_language not in self._v_inv_data:
            raise Exception("Target language is not defined")
        if int(msgid) not in self._v_inv_data[target_language]:
            raise Exception("Translation not found")

        return self._v_inv_data[target_language][int(msgid)]

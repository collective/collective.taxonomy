import generated

from persistent import Persistent

from plone.directives import form
from plone.behavior.interfaces import IBehavior
from plone.memoize import ram
from plone.supermodel.model import SchemaClass, Schema
from plone.dexterity.interfaces import IDexterityContent
from plone.indexer.interfaces import IIndexer
from plone.registry.interfaces import IRegistry
from plone.registry import Record, field

from Products.CMFCore.utils import getToolByName
from Products.PluginIndexes.KeywordIndex.KeywordIndex import KeywordIndex
from Products.ZCatalog.Catalog import CatalogError
from Products.ZCatalog.interfaces import IZCatalog

from zope import schema
from zope.component.hooks import getSite
from zope.interface import implements, alsoProvides
from zope.component import getUtility

from .i18n import MessageFactory as _
from .indexer import TaxonomyIndexer

import logging
logger = logging.getLogger("collective.taxonomy")


class TaxonomyBehavior(Persistent):
    implements(IBehavior)

    def __init__(self, name, title, description, field_name,
                 field_title, field_description, is_required,
                 multi_select):
        self.name = name
        self.title = _(title)
        self.description = _(description)
        self.factory = None
        self.field_name = field_name
        self.field_title = field_title
        self.field_description = field_description
        self.is_required = is_required
        self.multi_select = multi_select

    def deactivateSearchable(self):
        registry = getUtility(IRegistry)
        prefix = 'plone.app.querystring.field.' + self.field_name
        for suffix in ('title', 'enabled', 'group',
                       'operations', 'vocabulary', 'sortable', 'description'):
            record_name = prefix + '.' + suffix
            if record_name in registry.records:
                del registry.records[record_name]

    def removeIndex(self):
        context = getSite()
        sm = context.getSiteManager()
        sm.unregisterAdapter(TaxonomyIndexer, (IDexterityContent, IZCatalog),
                             IIndexer, name=self.field_name)

        catalog = getToolByName(context, 'portal_catalog')
        try:
            catalog.delIndex(self.field_name)
        except CatalogError:
            logging.info("Could not delete index " + self.field_name +
                         " something is not right..")

    def activateSearchable(self):
        registry = getUtility(IRegistry)
        prefix = 'plone.app.querystring.field.' + self.field_name

        def add(name, value):
            registry.records[prefix + '.' + name] = value

        add('title', Record(field.TextLine(), unicode(self.field_name)))
        add('enabled', Record(field.Bool(), True))
        add('group', Record(field.TextLine(), unicode('Taxonomy')))
        add('operations', Record(field.List(),
            ['plone.app.querystring.operation.selection.is']))
        add('vocabulary', Record(field.TextLine(), unicode(self.name)))
        add('sortable', Record(field.Bool(), True))
        add('description', Record(field.Text(), unicode('')))

    def addIndex(self):
        context = getSite()
        sm = context.getSiteManager()
        sm.registerAdapter(
            TaxonomyIndexer(self.field_name, self.name),
            (IDexterityContent, IZCatalog),
            IIndexer, name=self.field_name)

        catalog = getToolByName(context, 'portal_catalog')
        idx_object = KeywordIndex(str(self.field_name))
        try:
            catalog.addIndex(self.field_name, idx_object)
        except CatalogError:
            logging.info("Index " + self.field_name +
                         " already exists, we hope it is proper configured")

    
    @property
    def short_name(self):
        return str(self.name.split('.')[-1])

    @property
    @ram.cache(lambda method, self: str(self.__dict__))
    def interface(self):

        single_select_field = schema.Choice(
            title=_(unicode(self.field_title)),
            description=_(unicode(self.field_description)),
            required=self.is_required,
            vocabulary='collective.taxonomy.' +
            self.short_name)

        multi_select_field = schema.List(
            title=_(unicode(self.field_title)),
            description=_(unicode(self.field_description)),
            value_type=schema.Choice(
                required=self.is_required,
                vocabulary='collective.taxonomy.' +
                self.short_name))

        schemaclass = SchemaClass(
            self.short_name, (Schema, ),
            __module__='collective.taxonomy.generated',
            attrs={str(self.field_name):
                   self.multi_select
                   and multi_select_field
                   or single_select_field }
        )

        alsoProvides(schemaclass, form.IFormFieldProvider)

        return schemaclass

    @property
    def marker(self):
        return self.interface

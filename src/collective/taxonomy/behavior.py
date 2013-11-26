import logging
import generated

from persistent import Persistent

from plone.autoform.interfaces import WIDGETS_KEY
from plone.directives import form
from plone.dexterity.interfaces import IDexterityContent
from plone.indexer.interfaces import IIndexer
from plone.registry.interfaces import IRegistry
from plone.registry import Record, field
from plone.supermodel.interfaces import FIELDSETS_KEY
from plone.supermodel.model import Fieldset
from plone.supermodel.model import SchemaClass
from plone.z3cform.fieldsets.extensible import FormExtender
from plone.z3cform.fieldsets.interfaces import IFormExtender

from Products.CMFCore.utils import getToolByName
from Products.PluginIndexes.KeywordIndex.KeywordIndex import KeywordIndex
from Products.ZCatalog.Catalog import CatalogError
from Products.ZCatalog.interfaces import IZCatalog

from zope import schema
from zope.component.hooks import getSite
from zope.interface import implements, alsoProvides, Interface
from zope.component import getUtility, adapts
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from z3c.form.interfaces import IForm, IAddForm, IEditForm
#, IAddForm

from .interfaces import ITaxonomyBehavior
from .i18n import MessageFactory as _
from .indexer import TaxonomyIndexer

logger = logging.getLogger("collective.taxonomy")

GROUP_PERMISSION_KEY = "collective.taxonomy.security.group"


class PermissionChecker(FormExtender):
    implements(IFormExtender)
    adapts(Interface, IDefaultBrowserLayer, IForm)

    def __init__(self, context, request, form):
        self.context = context
        self.request = request
        self.form = form

    def update(self):
        is_form = IEditForm.providedBy(self.form) or \
            IAddForm.providedBy(self.form)

        # Works only for dexterity add- and edit forms.
        if not hasattr(self.form, 'portal_type') or not is_form:
            return

        membership_tool = getToolByName(self.context, 'portal_membership')

        for field_group in self.form.groups:
            for (field_name, field_instance) in field_group.fields.items():
                interface = field_instance.interface
                group = interface.queryTaggedValue(GROUP_PERMISSION_KEY)
                if group:
                    current_member = membership_tool.getAuthenticatedMember()
                    if group not in current_member.getGroups():
                        field_group.fields = field_group.fields.omit(
                            field_name
                        )


class TaxonomyBehavior(Persistent):

    group = ''  # BBB
    is_single_select = False

    implements(ITaxonomyBehavior)

    def __init__(self, name, title, description, field_title,
                 field_description, is_required=False,
                 is_single_select=False, group_permission='',
                 default_language='en'):
        self.name = name
        self.title = _(title)
        self.description = _(description)
        self.factory = None
        self.field_title = field_title
        self.field_description = field_description
        self.is_single_select = is_single_select
        self.is_required = is_required
        self.default_language = default_language
        self.group_permission = group_permission

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

        add('title', Record(field.TextLine(), unicode(self.field_title)))
        add('enabled', Record(field.Bool(), True))
        add('group', Record(field.TextLine(), unicode('Taxonomy')))
        add('operations', Record(field.List(),
            ['plone.app.querystring.operation.selection.is']))
        add('vocabulary', Record(field.TextLine(), unicode(self.name)))
        add('sortable', Record(field.Bool(), False))
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

    def unregisterInterface(self):
        if hasattr(generated, self.short_name):
            delattr(generated, self.short_name)

    @property
    def short_name(self):
        return str(self.name.split('.')[-1])

    @property
    def field_name(self):
        return 'taxonomy_' + self.short_name

    @property
    def vocabulary_name(self):
        return 'collective.taxonomy.' + self.short_name

    @property
    def interface(self):
        return getattr(generated, self.short_name)

    @property
    def marker(self):
        return getattr(generated, self.short_name)

    def generateInterface(self):
        logger.debug('generating interface for %s' % self.short_name)

        if hasattr(self, 'is_single_select') and self.is_single_select:
            select_field = schema.Choice(
                title=_(unicode(self.field_title)),
                description=_(unicode(self.field_description)),
                required=self.is_required,
                vocabulary=self.vocabulary_name
            )
        else:
            select_field = schema.List(
                title=_(unicode(self.field_title)),
                description=_(unicode(self.field_description)),
                required=self.is_required,
                constraint=lambda value: self.is_required and bool(value) or True,
                value_type=schema.Choice(
                    vocabulary=self.vocabulary_name,
                    required=self.is_required
                )
            )

        schemaclass = SchemaClass(
            self.short_name, (form.Schema, ),
            __module__='collective.taxonomy.generated',
            attrs={
                str(self.field_name): select_field
            }
        )

        schemaclass.setTaggedValue(
            FIELDSETS_KEY,
            [Fieldset('categorization',
                      fields=[self.field_name])]
        )

        if hasattr(self, 'group_permission') and self.group_permission:
            schemaclass.setTaggedValue(
                GROUP_PERMISSION_KEY,
                self.group_permission
            )

        if hasattr(self, 'is_single_select') and not self.is_single_select:
            schemaclass.setTaggedValue(
                WIDGETS_KEY,
                {self.field_name:
                 'collective.taxonomy.widget.TaxonomySelectFieldWidget'}
            )

        alsoProvides(schemaclass, form.IFormFieldProvider)
        return schemaclass

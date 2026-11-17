from Acquisition import aq_base
from collective.taxonomy import generated
from collective.taxonomy.i18n import CollectiveTaxonomyMessageFactory as _
from collective.taxonomy.indexer import TaxonomyIndexer
from persistent import Persistent
from plone import api
from plone.autoform.interfaces import IFormFieldProvider
from plone.autoform.interfaces import WIDGETS_KEY
from plone.autoform.interfaces import WRITE_PERMISSIONS_KEY
from plone.base.utils import safe_text
from plone.behavior.interfaces import IBehavior
from plone.dexterity.interfaces import IDexterityContent
from plone.indexer.interfaces import IIndexer
from plone.registry import field
from plone.registry import Record
from plone.registry.interfaces import IRegistry
from plone.supermodel.interfaces import FIELDSETS_KEY
from plone.supermodel.model import Fieldset
from plone.supermodel.model import Schema
from plone.supermodel.model import SchemaClass
from Products.CMFCore.utils import getToolByName
from Products.PluginIndexes.KeywordIndex.KeywordIndex import KeywordIndex
from Products.ZCatalog.Catalog import CatalogError
from Products.ZCatalog.interfaces import IZCatalog
from zope import schema
from zope.component import getUtility
from zope.component.hooks import getSite
from zope.interface import alsoProvides
from zope.interface import implementer

import importlib
import logging

try:
    importlib.metadata.version("plone.app.multilingual")
except importlib.metadata.PackageNotFoundError:
    HAS_PAM = False
else:
    from plone.app.multilingual.dx.interfaces import ILanguageIndependentField

    HAS_PAM = True

logger = logging.getLogger("collective.taxonomy")


@implementer(IBehavior)
class TaxonomyBehavior(Persistent):
    is_single_select = False
    field_prefix = "taxonomy_"

    def __init__(
        self,
        name,
        title,
        description,
        field_title,
        field_description,
        is_required=False,
        is_single_select=False,
        write_permission="",
        field_prefix="taxonomy_",
        default_language="en",
        taxonomy_fieldset="categorization",
    ):
        self.name = name
        self.title = _(title)
        self.description = _(description)
        self.factory = None
        self.field_title = field_title
        self.field_description = field_description
        self.field_prefix = field_prefix
        self.is_single_select = is_single_select
        self.is_required = is_required
        self.write_permission = write_permission
        self.default_language = default_language
        self.taxonomy_fieldset = taxonomy_fieldset

    def deactivateSearchable(self):
        registry = getUtility(IRegistry)
        prefix = "plone.app.querystring.field." + self.field_name
        for suffix in (
            "title",
            "enabled",
            "group",
            "operations",
            "vocabulary",
            "fetch_vocabulary",
            "sortable",
            "description",
        ):
            record_name = prefix + "." + suffix
            if record_name in registry.records:
                del registry.records[record_name]

    def removeIndex(self):
        context = getSite()
        sm = context.getSiteManager()
        sm.unregisterAdapter(
            factory=None,
            required=(IDexterityContent, IZCatalog),
            provided=IIndexer,
            name=self.field_name,
        )
        catalog = getToolByName(context, "portal_catalog")
        try:
            catalog.delIndex(self.field_name)
        except CatalogError:
            logging.info(
                "Could not delete index {} .. something is not right.".format(
                    self.field_name
                )
            )

    def activateSearchable(self):
        registry = getUtility(IRegistry)
        prefix = "plone.app.querystring.field." + self.field_name

        def add(name, value):
            registry.records[prefix + "." + name] = value

        add("title", Record(field.TextLine(), safe_text(self.field_title)))
        add("enabled", Record(field.Bool(), True))
        add("group", Record(field.TextLine(), safe_text("Taxonomy")))
        add(
            "operations",
            Record(
                field.List(value_type=field.TextLine()),
                [
                    "plone.app.querystring.operation.selection.is",
                    "plone.app.querystring.operation.selection.all",
                    "plone.app.querystring.operation.selection.any",
                    "plone.app.querystring.operation.selection.none",
                ],
            ),
        )
        add(
            "vocabulary", Record(field.TextLine(), safe_text(self.vocabulary_name))
        )  # noqa: E501
        add("fetch_vocabulary", Record(field.Bool(), True))
        add("sortable", Record(field.Bool(), False))
        add("description", Record(field.Text(), safe_text("")))

    def addIndex(self):
        context = getSite()
        sm = context.getSiteManager()
        sm.registerAdapter(
            TaxonomyIndexer(self.field_name, self.vocabulary_name),
            (IDexterityContent, IZCatalog),
            IIndexer,
            name=self.field_name,
        )

        catalog = getToolByName(context, "portal_catalog")
        idx_object = KeywordIndex(str(self.field_name))
        try:
            catalog.addIndex(self.field_name, idx_object)
        except CatalogError:
            logging.info(
                "Index {} already exists, we hope it is proper configured".format(
                    self.field_name
                )  # noqa: E501
            )

    def addMetadata(self):
        catalog = api.portal.get_tool(name="portal_catalog")
        try:
            catalog.addColumn(self.field_name)
        except CatalogError:
            logging.info(f"Column {self.field_name} already exists")  # noqa: E501

    def removeMetadata(self):
        catalog = api.portal.get_tool(name="portal_catalog")
        try:
            catalog.delColumn(self.field_name)
        except (CatalogError, ValueError):
            logging.info(f"Column {self.field_name} does not exist")

    def _objectsWithField(self):
        """Content that may store a value for this behavior's field."""
        portal = api.portal.get()
        catalog = api.portal.get_tool(name="portal_catalog")
        paths = {
            brain.getPath()
            for brain in catalog.unrestrictedSearchResults(
                object_provides=self.interface.__identifier__
            )
        }
        index = catalog._catalog.indexes.get(self.field_name)
        if index is not None:
            paths.update(catalog.getpath(rid) for rid in index.referencedObjects())
        objects = []
        for path in sorted(paths):
            obj = portal.unrestrictedTraverse(path, None)
            if obj is None:
                continue
            base = aq_base(obj)
            # Load the object: the __dict__ of a ghost is empty.
            getattr(base, "_p_activate", lambda: None)()
            if self.field_name in base.__dict__:
                objects.append(obj)
        return objects

    def changeFieldPrefix(self, prefix):
        """Change the field prefix, and with it the field name.

        The index, the metadata column, the querystring criterion and the
        values stored on content all move to the new field name, so no
        criterion is left pointing to an index that no longer exists.
        Nothing happens when the prefix does not change, so saving the
        settings does not empty the index.
        """
        prefix = prefix or ""
        if prefix == (self.field_prefix or ""):
            return

        old_name = self.field_name
        objects = self._objectsWithField()

        self.deactivateSearchable()
        self.removeIndex()
        self.removeMetadata()

        self.field_prefix = prefix
        new_name = self.field_name

        for obj in objects:
            base = aq_base(obj)
            setattr(base, new_name, base.__dict__[old_name])
            delattr(base, old_name)

        self.addIndex()
        self.addMetadata()
        self.activateSearchable()

        for obj in objects:
            obj.reindexObject(idxs=[new_name])

        logging.info(
            "Renamed taxonomy field %s to %s (%d items)",
            old_name,
            new_name,
            len(objects),
        )

    def unregisterInterface(self):
        if hasattr(generated, self.short_name):
            delattr(generated, self.short_name)

    @property
    def short_name(self):
        return str(self.name.split(".")[-1])

    @property
    def field_name(self):
        return (self.field_prefix or "") + self.short_name

    @property
    def vocabulary_name(self):
        return "collective.taxonomy." + self.short_name

    @property
    def interface(self):
        return getattr(generated, self.short_name)

    @property
    def marker(self):
        return getattr(generated, self.short_name)

    @property
    def former_dotted_names(self):
        """
        This is needed to not broke versioning
        """
        return self.name

    def generateInterface(self):
        logger.debug("generating interface for %s" % self.short_name)

        if hasattr(self, "is_single_select") and self.is_single_select:
            select_field = schema.Choice(
                title=_(safe_text(self.field_title)),
                description=_(safe_text(self.field_description)),
                required=self.is_required,
                vocabulary=self.vocabulary_name,
            )
        else:
            select_field = schema.List(
                title=_(safe_text(self.field_title)),
                description=_(safe_text(self.field_description)),
                required=self.is_required,
                min_length=self.is_required and 1 or 0,
                value_type=schema.Choice(
                    vocabulary=self.vocabulary_name, required=self.is_required
                ),
            )

        schemaclass = SchemaClass(
            self.short_name,
            (Schema,),
            __module__="collective.taxonomy.generated",
            attrs={str(self.field_name): select_field},
        )

        if self.write_permission:
            schemaclass.setTaggedValue(
                WRITE_PERMISSIONS_KEY, {self.field_name: self.write_permission}
            )

        try:
            taxonomy_fieldset = self.taxonomy_fieldset
        except AttributeError:
            # Backwards compatible:
            taxonomy_fieldset = "categorization"
        if taxonomy_fieldset != "default":
            schemaclass.setTaggedValue(
                FIELDSETS_KEY, [Fieldset(taxonomy_fieldset, fields=[self.field_name])]
            )

        if hasattr(self, "is_single_select") and not self.is_single_select:
            schemaclass.setTaggedValue(
                WIDGETS_KEY,
                {
                    self.field_name: "collective.taxonomy.widget.TaxonomySelectFieldWidget"
                },
            )

        alsoProvides(schemaclass, IFormFieldProvider)

        if HAS_PAM:
            alsoProvides(schemaclass[self.field_name], ILanguageIndependentField)

        return schemaclass

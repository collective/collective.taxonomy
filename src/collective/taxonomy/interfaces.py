from .i18n import CollectiveTaxonomyMessageFactory as _
from plone import api
from plone.namedfile.field import NamedBlobFile
from plone.restapi.controlpanels.interfaces import IControlpanel
from zope import schema
from zope.i18n.interfaces import ITranslationDomain
from zope.interface import Interface
from zope.schema.interfaces import IVocabularyFactory


class ITaxonomySelectWidget(Interface):
    """Marker interface for the taxonomy select widget"""


class IBrowserLayer(Interface):
    """Add-on browser layer."""


class ITaxonomy(ITranslationDomain, IVocabularyFactory):
    """Persistent local utility."""

    def add(language, identifier, path):
        """Add or update entry.

        For example: `self.add('en', 'identifier', 'What a lovely day!')`
        """

    def replace(language, items):
        """Replace all items for a given language.

        Items are given as (path, identifier) tuples.

        Note that order will be assigned naively. It is assumed that
        items are given in depth-first order.
        """

    def __setitem__(identifier, term):
        """ """


# Control panel stuff


class ITaxonomySettings(Interface):
    """Schema for controlpanel settings"""

    taxonomies = schema.List(
        title=_("Taxonomies"),
        value_type=schema.Choice(
            description=_(
                "help_taxonomies",
                default="Select the taxonomies you desire to modify",
            ),
            required=False,
            vocabulary="collective.taxonomy.taxonomies",
        ),
        default=[],
        required=False,
    )


def taxonomyDefaultValue():
    taxonomy = api.portal.get().REQUEST.get("form.widgets.taxonomy")
    if not taxonomy:
        return ""
    return taxonomy


class ITaxonomyForm(Interface):
    taxonomy = schema.TextLine(
        title=_("Taxonomy"),
        description=_("The taxonomy identifier"),
        required=True,
        defaultFactory=taxonomyDefaultValue,
    )

    field_title = schema.TextLine(
        title=_("Title"),
        description=_("Will be used for the field title as well"),
        required=True,
    )

    field_description = schema.Text(
        title=_("Description"),
        description=_("Will be used for the field description as well"),
        required=False,
    )

    default_language = schema.Choice(
        title=_("Default language"),
        vocabulary="plone.app.vocabularies.AvailableContentLanguages",
        required=True,
        defaultFactory=api.portal.get_current_language,
    )

    import_file = NamedBlobFile(title=_("Upload VDEX xml file"), required=False)

    import_file_purge = schema.Bool(
        title=_("Purge entries on upload"),
        description=_(
            "Check this box if you want to purge all entries " "when uploading."
        ),
        required=False,
    )

    is_required = schema.Bool(
        title=_("Required"),
        description=_("Check this box if you want the field to be required"),
        required=False,
    )

    is_single_select = schema.Bool(
        title=_("Single select"),
        description=_("Check this box if you want the field to be mono-valued"),
        required=False,
    )

    write_permission = schema.Choice(
        title=_("Write permission"),
        description=_("Write permission for the field"),
        required=False,
        vocabulary="collective.taxonomy.permissions",
    )

    field_prefix = schema.ASCIILine(
        title=_("Field prefix"),
        description=_("Prefix used for behavior indexer."),
        default="taxonomy_",
        required=False,
    )

    taxonomy_fieldset = schema.TextLine(
        title=_("Fieldset"),
        description=_(
            "Fieldset for the taxonomy behavior field. "
            "Example: 'categorization'. Use 'default' for "
            "the first fieldset."
        ),
        default="categorization",
        required=False,
    )


class ITaxonomyView(Interface):
    def taxonomiesForContext(self):
        """ """

    def translate(self, msgid, domain, target_language):
        """ """


class ITaxonomyControlPanel(IControlpanel):
    """Taxonomy Control panel"""

# -*- coding: utf-8 -*-

from plone.namedfile.field import NamedBlobFile

from zope.interface import Interface
from zope.i18n.interfaces import ITranslationDomain
from zope import schema
from zope.schema.interfaces import IVocabularyFactory

from .i18n import MessageFactory as _


class ITaxonomySelectWidget(Interface):
    """ Marker interface for the taxonomy select widget """


class IBrowserLayer(Interface):
    """Add-on browser layer."""


class ITaxonomy(ITranslationDomain, IVocabularyFactory):
    """Persistent local utility."""

    def add(language, identifier, path):
        """
        For example: self.add('en', 'identifier', 'What a lovely day!')

        """

    def __setitem__(identifier, term):
        """ """

# Control panel stuff


class ITaxonomySettings(Interface):
    """ Schema for controlpanel settings """

    taxonomies = schema.List(
        title=_(u"Taxonomies"),
        value_type=schema.Choice(
            description=_(
                u"help_taxonomies",
                default=u"Select the taxnomies you desire to modify"
            ),
            required=False,
            vocabulary='collective.taxonomy.taxonomies',
        ),
        default=[],
    )


class ITaxonomyForm(Interface):
    taxonomy = schema.TextLine(
        title=_(u"Taxonomy"),
        required=False
    )

    field_title = schema.TextLine(
        title=_(u"Title"),
        description=_("Will be used for the field title as well"),
        required=True
    )

    field_description = schema.TextLine(
        title=_(u"Description"),
        description=_("Will be used for the field description as well"),
        required=True
    )

    default_language = schema.TextLine(
        title=_(u"Default language"),
        description=_("For example en, da, de, etc."),
        required=True
    )

    import_file = NamedBlobFile(
        title=_(u"Upload VDEX xml file"),
        description=_(u" "),
        required=False
    )

    is_required = schema.Bool(
        title=_(u"Required"),
        required=True
    )

    is_single_select = schema.Bool(
        title=_(u"Single select"),
        required=True
    )

    write_permission = schema.Choice(
        title=_(u"Write permission"),
        required=False,
        vocabulary='collective.taxonomy.permissions'
    )

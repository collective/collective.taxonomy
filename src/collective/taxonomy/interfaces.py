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
           >>> taxonomny.add('en', <identifier>, 'What a lovely day!')

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
    # Regular fields

    field_title = schema.TextLine(
        title=_(u"Field title"),
        required=True
    )

    field_description = schema.TextLine(
        title=_(u"Field description"),
        required=False
    )

    import_file = NamedBlobFile(
        title=_(u"Upload VDEX xml file"),
        description=_(u" "),
        required=False
    )

    is_required = schema.Bool(
        title=_(u"Is required?"),
        required=True
    )

    write_permission = schema.Choice(
        title=_(u"Write permission"),
        required=False,
        vocabulary='collective.taxonomy.permissions'
    )

    # Taxonomy hidden field
    taxonomy = schema.TextLine(
        title=_(u"Taxonomy"),
        required=False
    )

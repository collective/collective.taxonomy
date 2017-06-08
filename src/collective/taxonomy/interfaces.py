# -*- coding: utf-8 -*-

from plone import api
from plone.namedfile.field import NamedBlobFile

from zope.interface import Interface
from zope.i18n.interfaces import ITranslationDomain
from zope import schema
from zope.schema.interfaces import IVocabularyFactory

from .i18n import CollectiveTaxonomyMessageFactory as _


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


def taxonomyDefaultValue():
    request = api.portal.get().REQUEST
    if not request:
        return u''
    taxonomy = request.get('form.widgets.taxonomy')
    if not taxonomy:
        return u''
    return taxonomy


def get_lang_code(lang=None):
    try:
        if lang is None:
            lang = api.portal.get_current_language()
        return lang.split('-', 1)[0]
    except AttributeError:
        lang = api.portal.get_default_language()
        if lang:
            return lang.split('-', 1)[0]
        else:
            return 'en'


class ITaxonomyForm(Interface):

    taxonomy = schema.TextLine(
        title=_(u"Taxonomy"),
        description=_("The taxonomy identifier"),
        required=True,
        defaultFactory=taxonomyDefaultValue,
    )

    field_title = schema.TextLine(
        title=_(u"Title"),
        description=_("Will be used for the field title as well"),
        required=True
    )

    field_description = schema.Text(
        title=_(u"Description"),
        description=_("Will be used for the field description as well"),
        required=False
    )

    default_language = schema.Choice(
        title=_(u"Default language"),
        vocabulary='collective.taxonomy.languages',
        required=True,
        defaultFactory=get_lang_code
    )

    import_file = NamedBlobFile(
        title=_(u"Upload VDEX xml file"),
        description=_(u" "),
        required=False
    )

    is_required = schema.Bool(
        title=_(u"Required"),
        description=_(
            u"Check this box if you want the field to be required"),
        required=True
    )

    is_single_select = schema.Bool(
        title=_(u"Single select"),
        description=_(
            u"Check this box if you want the field to be mono-valued"),
        required=True
    )

    write_permission = schema.Choice(
        title=_(u"Write permission"),
        description=_(
            u"Write permission for the field"),
        required=False,
        vocabulary='collective.taxonomy.permissions'
    )

    taxonomy_fieldset = schema.TextLine(
        title=_(u"Fieldset"),
        description=_(u"Fieldset for the taxonomy behavior field. "
                      u"Example: 'categorization'. Use 'default' for "
                      u"the first fieldset."),
        default=u"categorization",
        required=False
    )



class ITaxonomyView(Interface):

    def taxonomiesForContext(self):
        """ """

    def translate(self, msgid, domain, target_language):
        """ """

# -*- coding: utf-8 -*-

from z3c.form import interfaces

from zope import schema
from zope.interface import Interface
from zope.i18n.interfaces import ITranslationDomain
from zope.schema.interfaces import IVocabularyFactory

from i18n import MessageFactory as _

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

class ITaxonomyForm(Interface):
    name = schema.TextLine(title=u'Name', required=True)
    title = schema.TextLine(title=u'Title', required=True)
    field_name = schema.TextLine(title=u'Field name', required=True)

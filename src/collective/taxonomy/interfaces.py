# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope.i18n.interfaces import ITranslationDomain
from zope.schema.interfaces import IVocabularyFactory


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

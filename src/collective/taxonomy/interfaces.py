# -*- coding: utf-8 -*-

from z3c.form import interfaces

from zope import schema
from zope.interface import Interface
from zope.i18n.interfaces import ITranslationDomain
from zope.schema.interfaces import IBaseVocabulary

from i18n import MessageFactory as _

class IBrowserLayer(Interface):
    """Add-on browser layer."""


class ITaxonomy(ITranslationDomain, IBaseVocabulary):
    """Persistent local utility."""

    def add(identifier, langstrings):
        """
           >>> taxonomny.add(<identifier>, en='What a lovely day!')

        """


    def __setitem__(identifier, term):
        # But in this method, we'll actually unpack ( ! ) the term !! ... into a compact, B-Tree representation ....
        # and discard the description ....
        pass

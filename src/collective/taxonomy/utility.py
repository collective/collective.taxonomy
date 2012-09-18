# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from BTrees.OOBTree import OOBTree
from persistent.dict import PersistentDict

from zope.interface import implements
from zope.component import getMultiAdapter
from zope.schema.interfaces import IVocabulary
from zope.schema.vocabulary import SimpleTerm

from .interfaces import ITaxonomy


class Taxonomy(PersistentDict):
    implements(ITaxonomy)

    def __init__(self, title):
        super(Taxonomy, self).__init__(self)
        self.title = title

    def add(self, language, identifier, path, parent_identifier):
        if not language in self:
            self[language] = OOBTree()

        self[language][path] = (identifier, parent_identifier)

    def translate(msgid, mapping=None, context=None,
                  target_language=None, default=None):
        import pdb
        pdb.set_trace()

    def __call__(self, context):
        context = aq_inner(context)
        portal_state = getMultiAdapter(
            (context, context.REQUEST),
            name=u'plone_portal_state')
        current_language = portal_state.language()
        data = self[current_language]
        return Vocabulary(data)


class Vocabulary(object):
    implements(IVocabulary)

    def __init__(self, data):
        self.data = data

    def getTerms(self):
        results = []

        for (path, (identifier, parent)) in \
                self.data.items():
            results.append(SimpleTerm(value=path, title=path))

        return results

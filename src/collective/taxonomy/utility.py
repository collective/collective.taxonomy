# -*- coding: utf-8 -*-

from zope.interface import implements
from BTrees.OOBTree import OOBTree
from persistent.dict import PersistentDict

from zope.schema.interfaces import IVocabulary

from .interfaces import ITaxonomy

class Taxonomy(PersistentDict):
    implements(ITaxonomy)

    def __init__(self, title):
        super(Taxonomy, self).__init__(self)
        self.title = title

    def add(self, language, identifier, path, parent_identifier):
        if not self.has_key(language):
            self[language] = OOBTree()

        self[language][path] = (identifier, parent_identifier)

    def translate(msgid, mapping=None, context=None, target_language=None, default=None):
        import pdb; pdb.set_trace()

    def __call__(self, context):
        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')
        current_language = portal_state.language()
        data = self[current_language]
        return Vocabulary(data)

class Vocabulary(object):
    implements(IVocabulary)

    def __init__(self, data):
        self.data = data

    def getTerms(self):
        return self.data.items()





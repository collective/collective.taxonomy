# -*- coding: utf-8 -*-

from BTrees.OOBTree import OOBTree
from OFS.SimpleItem import SimpleItem

from zope.component import getMultiAdapter
from zope.component.hooks import getSite
from zope.interface import implements

from plone.behavior.interfaces import IBehavior

from persistent.dict import PersistentDict

from .behavior import TaxonomyBehavior
from .interfaces import ITaxonomy
from .vocabulary import Vocabulary


class Taxonomy(SimpleItem):
    implements(ITaxonomy)

    def __init__(self, name, title):
        super(Taxonomy, self).__init__(self)
        self.data = PersistentDict()
        self._v_inv_data = {}

        self.name = name
        self.title = title

        self.registerBehaviour()

    def __setstate__(self, state):
        super(Taxonomy, self).__setstate__(state)
        self._v_inv_data = {}
        for language in self.data.keys():
            for (path, identifier) in self.data[language].items():
                if language not in self._v_inv_data:
                    self._v_inv_data[language] = {}
                self._v_inv_data[language][identifier] = path

    def __call__(self, context):
        current_language = self.getCurrentLanguage()
        data = self.data[current_language]
        inv_data = self._v_inv_data[current_language]
        return Vocabulary(self.name, data, inv_data)

    def getShortName(self):
        return self.name.split('.')[-1]

    def getCurrentLanguage(self):
        context = getSite()
        portal_state = getMultiAdapter((context.aq_parent,
                                        context.aq_parent.REQUEST),
                                       name=u'plone_portal_state')
        (language_major, language_minor ) = \
            portal_state.language().split('-', 1)
        return language_major

    def registerBehaviour(self):
        context = getSite()
        sm = context.getSiteManager()
        behavior = TaxonomyBehavior(self.name, self.title, 'TestField')

        sm.registerUtility(behavior, IBehavior,
                           name='collective.taxonomy.generated.' +
                                self.getShortName())

    def add(self, language, identifier, path):
        if not language in self.data:
            self.data[language] = OOBTree()
        if not language in self._v_inv_data:
            self._v_inv_data[language] = OOBTree()

        self.data[language][path] = identifier
        self._v_inv_data[language][identifier] = path

    def translate(self, msgid, mapping=None, context=None,
                  target_language=None, default=None):
        if target_language is None:
            target_language = self.getCurrentLanguage
        if target_language not in self._v_inv_data:
            raise Exception("Target language is not defined")
        if int(msgid) not in self._v_inv_data[target_language]:
            raise Exception("Translation not found")

        return self._v_inv_data[target_language][int(msgid)]

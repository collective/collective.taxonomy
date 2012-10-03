# -*- coding: utf-8 -*-

from BTrees.OOBTree import OOBTree
from OFS.SimpleItem import SimpleItem

from zope.component import getMultiAdapter, queryUtility
from zope.component.hooks import getSite
from zope.interface import implements


from plone.behavior.interfaces import IBehavior
from plone.memoize import ram

from persistent.dict import PersistentDict

from .behavior import TaxonomyBehavior
from .interfaces import ITaxonomy
from .vocabulary import Vocabulary

import logging
logger = logging.getLogger("collective.taxonomy")


class Taxonomy(SimpleItem):
    implements(ITaxonomy)

    def __init__(self, name, title, default_language):
        super(Taxonomy, self).__init__(self)
        self.data = PersistentDict()
        self.name = name
        self.title = title
        self.default_language = default_language

    def __call__(self, context):
        request = getattr(context, "REQUEST", None)

        current_language = self.getCurrentLanguage(request)
        data = self.data[current_language]
        inverted_data = self.inverted_data[current_language]

        return Vocabulary(self.name, data, inverted_data)

    @property
    @ram.cache(lambda method, self: self.data._p_mtime)
    def inverted_data(self):
        inv_data = {}
        for (language, elements) in self.data.items():
            inv_data[language] = {}
            for (path, identifier) in elements.items():
                inv_data[language][identifier] = path
        return inv_data

    def getShortName(self):
        return self.name.split('.')[-1]

    def getCurrentLanguage(self, request):
        portal_state = getMultiAdapter(
            (self, request), name=u'plone_portal_state'
        )

        language = portal_state.language().split('-', 1)[0]

        if language in self.data:
            return language
        elif self.default_language in self.data:
            return self.default_language
        else:
            # our best guess!
            return self.data.keys()[0]

    def registerBehavior(self, **kwargs):
        context = getSite()
        sm = context.getSiteManager()
        behavior = TaxonomyBehavior(self.name,
                                    self.title,
                                    u'Adds the named taxonomy to the field'
                                    'list', **kwargs)
        sm.registerUtility(behavior, IBehavior,
                           name='collective.taxonomy.generated.' +
                                self.getShortName())

        behavior.addIndex()
        behavior.activateSearchable()

    def unregisterBehavior(self):
        context = getSite()
        sm = context.getSiteManager()
        behavior_name = 'collective.taxonomy.generated.' + self.getShortName()
        utility = queryUtility(IBehavior, name=behavior_name)
        if utility is None:
            logging.info("It looks like the behavior was already removed,"
                         "indexes and stuff may still be there.")
            return

        if utility:
            utility.removeIndex()
            utility.deactivateSearchable()
            utility.cleanupFTI()
            sm.unregisterUtility(utility, IBehavior, name=behavior_name)

    def add(self, language, identifier, path):
        if not language in self.data:
            self.data[language] = OOBTree()

        self.data[language][path] = identifier

    def translate(self, msgid, mapping=None, context=None,
                  target_language=None, default=None):

        if target_language is None or \
                target_language not in self.inverted_data:
            target_language = self.getCurrentLanguage(
                getattr(context, 'REQUEST')
            )

        if msgid not in self.inverted_data[target_language]:
            return ''

        path = self.inverted_data[target_language][msgid]
        pretty_path = path[1:].replace('/', u' » ')

        return pretty_path

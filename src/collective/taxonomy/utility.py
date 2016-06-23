# -*- coding: utf-8 -*-

from .behavior import TaxonomyBehavior
from .interfaces import ITaxonomy
from .vocabulary import Vocabulary

from BTrees.OOBTree import OOBTree
from OFS.SimpleItem import SimpleItem

from persistent.dict import PersistentDict

from plone.behavior.interfaces import IBehavior
from plone.dexterity.fti import DexterityFTIModificationDescription
from plone.dexterity.interfaces import IDexterityFTI
from plone.memoize import ram

from zope.component import getMultiAdapter
from zope.component.hooks import getSite
from zope.component.interfaces import ComponentLookupError
from zope.interface import implements
from zope.lifecycleevent import modified

import generated
import logging

from copy import copy

from collective.taxonomy import PATH_SEPARATOR


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

        if not self.data:
            return Vocabulary(self.name, {}, {})

        request = getattr(context, "REQUEST", None)

        current_language = self.getCurrentLanguage(request)
        data = self.data[current_language]
        inverted_data = self.inverted_data[current_language]

        return Vocabulary(self.name, data, inverted_data)

    @property
    @ram.cache(lambda method, self: (self.name, self.data._p_mtime))
    def inverted_data(self):
        inv_data = {}
        for (language, elements) in self.data.items():
            inv_data[language] = {}
            for (path, identifier) in elements.items():
                inv_data[language][identifier] = path
        return inv_data

    def getShortName(self):
        return self.name.split('.')[-1]

    def getGeneratedName(self):
        return 'collective.taxonomy.generated.' + self.getShortName()

    def getVocabularyName(self):
        return 'collective.taxonomy.' + self.getShortName()

    def getCurrentLanguage(self, request):
        try:
            portal_state = getMultiAdapter(
                (self, request), name=u'plone_portal_state'
            )

            language = portal_state.language().split('-', 1)[0]
        except ComponentLookupError:
            language = ''  # Force to return default language.

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
        new_args = copy(kwargs)

        new_args['name'] = self.name
        new_args['title'] = self.title
        new_args['description'] = kwargs.get('field_description', u'')
        new_args['field_description'] = new_args['description']

        behavior = TaxonomyBehavior(**new_args)
        sm.registerUtility(behavior, IBehavior,
                           name=self.getGeneratedName())

        behavior.addIndex()
        behavior.activateSearchable()

    def cleanupFTI(self):
        """Cleanup the FTIs"""
        generated_name = self.getGeneratedName()
        context = getSite()
        sm = context.getSiteManager()
        for (name, fti) in sm.getUtilitiesFor(IDexterityFTI):
            if generated_name in fti.behaviors:
                fti.behaviors = [behavior for behavior in
                                 fti.behaviors
                                 if behavior != generated_name]
            modified(fti, DexterityFTIModificationDescription("behaviors", ''))

    def updateBehavior(self, **kwargs):
        sm = getSite().getSiteManager()

        behavior_name = self.getGeneratedName()
        short_name = self.getShortName()

        utility = sm.queryUtility(IBehavior, name=behavior_name)
        if utility:
            utility.deactivateSearchable()
            utility.activateSearchable()
            utility.title = kwargs['field_title']

        delattr(generated, short_name)

        for (name, fti) in sm.getUtilitiesFor(IDexterityFTI):
            if behavior_name in fti.behaviors:
                modified(fti, DexterityFTIModificationDescription("behaviors", ''))

    def unregisterBehavior(self):
        context = getSite()
        sm = context.getSiteManager()
        behavior_name = self.getGeneratedName()
        utility = sm.queryUtility(IBehavior, name=behavior_name)

        if utility is None:
            return

        self.cleanupFTI()

        utility.removeIndex()
        utility.deactivateSearchable()
        utility.unregisterInterface()

        sm.unregisterUtility(utility, IBehavior, name=behavior_name)

    def clean(self):
        self.data.clear()

    def add(self, language, identifier, path):
        if not language in self.data:
            self.data[language] = OOBTree()

        self.data[language][path] = identifier

    def translate(self, msgid, mapping=None, context=None,
                  target_language=None, default=None):

        if target_language is None or \
                target_language not in self.inverted_data:
            target_language = str(self.getCurrentLanguage(
                getattr(context, 'REQUEST')
            ))

        if msgid not in self.inverted_data[target_language]:
            return ''

        path = self.inverted_data[target_language][msgid]
        pretty_path = path[1:].replace(PATH_SEPARATOR, u' » ')

        return pretty_path

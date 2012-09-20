# -*- coding: utf-8 -*-

import generated

from BTrees.OOBTree import OOBTree
from OFS.SimpleItem import SimpleItem

from zope import schema
from zope.component import getMultiAdapter
from zope.component.hooks import getSite
from zope.interface import implements, alsoProvides
from zope.i18nmessageid import MessageFactory
from zope.schema.interfaces import IVocabulary
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.directives import form
from plone.behavior.interfaces import IBehavior
from plone.supermodel.model import SchemaClass, Schema
from plone.memoize import ram

from persistent.dict import PersistentDict
from persistent import Persistent

from .interfaces import ITaxonomy
from .i18n import MessageFactory as _


class TaxonomyBehavior(Persistent):
    implements(IBehavior)

    def __init__(self, title, description, field_name):
        self.title = _(title)
        self.description = _(description)
        self.factory = None
        self.field_name = field_name

    @property
    def short_name(self):
        return str(self.title.split('.')[-1])

    @property
    @ram.cache(lambda method, self: True)
    def interface(self):
        schemaclass = SchemaClass(
            self.short_name, (Schema, ),
            __module__='collective.taxonomy.generated',
            attrs={self.field_name:
                   schema.Choice(title=_(u'Wuhu'),
                                 description=_(u""),
                                 required=False,
                                 vocabulary='collective.taxonomy.' +
                                 self.short_name) }
        )

        alsoProvides(schemaclass, form.IFormFieldProvider)

        if not hasattr(generated, self.short_name):
            setattr(generated, self.short_name, schemaclass)

        return schemaclass

    @property
    def marker(self):
        return self.interface


class Taxonomy(SimpleItem):
    implements(ITaxonomy)

    def getCurrentLanguage(self):
        context = getSite()
        portal_state = getMultiAdapter((context.aq_parent,
                                        context.aq_parent.REQUEST),
                                       name=u'plone_portal_state')
        (language_major, language_minor ) = \
            portal_state.language().split('-', 1)
        return language_major

    def getShortName(self):
        return self.name.split('.')[-1]

    def registerBehaviour(self):

        context = getSite()
        sm = context.getSiteManager()
        behavior = TaxonomyBehavior(self.name, self.title, 'TestField')

        sm.registerUtility(behavior, IBehavior,
                           name='collective.taxonomy.generated.' +
                                self.getShortName())

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

    def __call__(self, context):
        current_language = self.getCurrentLanguage()
        data = self.data[current_language]
        inv_data = self._v_inv_data[current_language]
        return Vocabulary(self.name, data, inv_data)


class Vocabulary(object):
    implements(IVocabulary)

    def __init__(self, name, data, inv_data):
        self.data = data
        self.inv_data = inv_data
        self.message = MessageFactory(name)

    def __iter__(self):
        for term in self.getTerms():
            yield term

    def __len__(self):
        return len(self.getTerms())

    def __contains__(self, identifier):
        return self.getTerm(identifier) is not None

    def getTermByToken(self, input_identifier):
        return SimpleTerm(value=int(input_identifier),
                          title=self.message(int(input_identifier),
                                             self.inv_data[
                                                 int(input_identifier)]))

    def getTerm(self, input_identifier):
        return self.getTermByToken(input_identifier)

    def getTerms(self):
        results = []

        for (path, identifier) in self.data.items():
            term = SimpleTerm(value=identifier,
                              title=self.message(identifier, path))
            results.append(term)

        return results

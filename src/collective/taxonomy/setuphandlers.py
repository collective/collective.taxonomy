# -*- conding: utf-8 -*-
from collective.taxonomy.interfaces import ITaxonomy
from zope.component.hooks import getSite
from zope.i18n.interfaces import ITranslationDomain
from zope.schema.interfaces import IVocabularyFactory


def uninstall(context):
    sm = getSite().getSiteManager()
    utilities = sm.getUtilitiesFor(ITaxonomy)

    for uname, utility in utilities:
        utility.unregisterBehavior()
        sm.unregisterUtility(utility, ITaxonomy, name=uname)
        sm.unregisterUtility(utility, IVocabularyFactory, name=uname)
        sm.unregisterUtility(utility, ITranslationDomain, name=uname)

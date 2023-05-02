from collective.taxonomy.interfaces import ITaxonomy
from collective.taxonomy.utility import Taxonomy
from plone.i18n.normalizer.interfaces import IIDNormalizer
from zope.component import getUtility
from zope.component import queryUtility
from zope.i18n.interfaces import ITranslationDomain
from zope.schema.interfaces import IVocabularyFactory


def registerTaxonomy(context, name, title, default_language, description=""):
    if hasattr(context, "getSite"):
        site = context.getSite()
    else:
        site = context

    normalizer = getUtility(IIDNormalizer)

    normalized_name = normalizer.normalize(name).replace("-", "")
    utility_name = "collective.taxonomy." + normalized_name
    taxonomy = queryUtility(ITaxonomy, name=utility_name)

    if taxonomy is None:
        taxonomy = Taxonomy(utility_name, title, default_language)
        sm = site.getSiteManager()
        sm.registerUtility(taxonomy, ITaxonomy, name=utility_name)
        sm.registerUtility(taxonomy, IVocabularyFactory, name=utility_name)
        sm.registerUtility(taxonomy, ITranslationDomain, name=utility_name)
    else:
        taxonomy.title = title
        taxonomy.default_language = default_language

    return taxonomy

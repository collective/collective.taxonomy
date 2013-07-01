from elementtree import ElementTree

from plone.i18n.normalizer.interfaces import IIDNormalizer

from zope.component import queryUtility, getUtility
from zope.i18n.interfaces import ITranslationDomain
from zope.schema.interfaces import IVocabularyFactory

from .interfaces import ITaxonomy
from .utility import Taxonomy
from .vdex import ImportVdex, ExportVdex


class TaxonomyImportExportAdapter(object):
    IMSVDEX_NS = 'http://www.imsglobal.org/xsd/imsvdex_v1p0'

    def __init__(self, context):
        self.context = context

    def importDocument(self, document):
        # XXX: we should change this
        if hasattr(self.context, 'getSite'):
            site = self.context.getSite()
        else:
            site = self.context

        normalizer = getUtility(IIDNormalizer)

        tree = ElementTree.fromstring(document)
        default_language = tree.attrib['language']

        name = tree.find('./{%s}vocabIdentifier'
                         % (self.IMSVDEX_NS))
        title = tree.find('./{%s}vocabName/{%s}langstring'
                          % (self.IMSVDEX_NS, self.IMSVDEX_NS))

        normalized_name = normalizer.normalize(name.text).replace('-', '')
        utility_name = 'collective.taxonomy.' + normalized_name
        taxonomy = queryUtility(ITaxonomy, name=utility_name)

        if taxonomy is None:
            taxonomy = Taxonomy(utility_name, title.text, default_language)
            sm = site.getSiteManager()
            sm.registerUtility(taxonomy, ITaxonomy, name=utility_name)
            sm.registerUtility(taxonomy, IVocabularyFactory, name=utility_name)
            sm.registerUtility(taxonomy, ITranslationDomain, name=utility_name)
        else:
            taxonomy.title = title.text
            taxonomy.default_language = default_language

        taxonomy.clean()

        results = ImportVdex(tree, self.IMSVDEX_NS)()

        for (language, elements) in results.items():
            for (path, identifier) in elements.items():
                taxonomy.add(language, identifier, path)

        return utility_name

    def exportDocument(self, name):
        taxonomy = queryUtility(ITaxonomy, name=name)
        treestring = ExportVdex(taxonomy)(as_string=True)

        return treestring

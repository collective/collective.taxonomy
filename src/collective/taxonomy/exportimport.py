from elementtree import ElementTree

from zope.component import queryUtility
from zope.i18n.interfaces import ITranslationDomain
from zope.schema.interfaces import IVocabularyFactory

from .interfaces import ITaxonomy
from .utility import Taxonomy
from .vdex import ImportVdex, ExportVdex


def importTaxonomy(context):
    directory = context.listDirectory('taxonomies/')

    if not directory:
        return

    for filename in directory:
        body = context.readDataFile('taxonomies/' + filename)
        if body is not None:
            utility_name = filename.lower().replace('.xml', '')
            importer = TaxonomyImportExportAdapter(context)
            importer.importDocument('collective.taxonomy.' + utility_name,
                                    body)


def exportTaxonomy(context):
    site = context.getSite()
    for (name, taxonomy) in site.getSiteManager().getUtilitiesFor(ITaxonomy):
        short_name = name.split('.')[-1]
        exporter = TaxonomyImportExportAdapter(context)
        body = exporter.exportDocument(name)
        if body is not None:
            context.writeDataFile('taxonomies/' + short_name + '.xml',
                                  body, 'text/xml')


class TaxonomyImportExportAdapter(object):
    IMSVDEX_NS = 'http://www.imsglobal.org/xsd/imsvdex_v1p0'

    def __init__(self, context):
        self.context = context

    def importDocument(self, utility_name, document):
        # XXX: we should change this
        if hasattr(self.context, 'getSite'):
            site = self.context.getSite()
        else:
            site = self.context

        tree = ElementTree.fromstring(document)
        default_language = tree.attrib['language']

        title = tree.find('./{%s}vocabName/{%s}langstring'
                          % (self.IMSVDEX_NS, self.IMSVDEX_NS))

        taxonomy = queryUtility(ITaxonomy, name=utility_name)

        if not taxonomy:
            taxonomy = Taxonomy(utility_name, title.text, default_language)
            sm = site.getSiteManager()
            sm.registerUtility(taxonomy, ITaxonomy, name=utility_name)
            sm.registerUtility(taxonomy, IVocabularyFactory, name=utility_name)
            sm.registerUtility(taxonomy, ITranslationDomain, name=utility_name)

        results = ImportVdex(tree, self.IMSVDEX_NS)()

        for (language, elements) in results.items():
            for (path, identifier) in elements.items():
                taxonomy.add(language, identifier, path)

        return utility_name

    def exportDocument(self, name):
        taxonomy = queryUtility(ITaxonomy, name=name)
        treestring = ExportVdex(taxonomy)(as_string=True)

        return treestring

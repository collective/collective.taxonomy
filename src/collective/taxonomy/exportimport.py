from elementtree import ElementTree

from zope.interface import Interface, implements, implementedBy
from zope.component import queryUtility
from zope import schema

from zope.schema.interfaces import IField
from zope.schema.interfaces import IVocabularyTokenized
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.supermodel.utils import prettyXML, elementToValue, valueToElement, ns

from .interfaces import ITaxonomy
from .utility import Taxonomy


def importTaxonomy(context):
    logger = context.getLogger('collective.taxonomy')
    body = context.readDataFile('taxonomies.xml')
    if body is not None:
        importer = TaxonomyImportExportAdapter(context)
        importer.importDocument(body)


def exportTaxonomy(context):
    logger = context.getLogger('collective.taxonomy')
    exporter = TaxonomyImportExportAdapter(context)
    body = exporter.exportDocument()
    if body is not None:
        context.writeDataFile('taxonomies.xml', body, 'text/xml')


class TaxonomyImportExportAdapter(object):
    """Helper classt to import a registry file
    """

    LOGGER_ID = 'collective.taxonomy'
    IMSVDEX_NS = 'http://www.imsglobal.org/xsd/imsvdex_v1p0'

    def __init__(self, context, environ):
        self.context = context
        self.logger = environ.getLogger(self.LOGGER_ID)

    def importDocument(self, document):
        tree = ElementTree.fromstring(document)
        title = tree.find('{%s}vocabName' % self.IMSVDEX_NS)
        name = tree.find('{%s}vocabIdentifier' % self.IMSVDEX_NS)

        utility_name = 'collective.taxonomy.' + name.text

        taxonomy = queryUtility(ITaxonomy, name=name.text)

        if not taxonomy:
            taxonomy = Taxonomy(title.text)
            sm = self.context.getSiteManager()
            sm.registerUtility(taxonomy, ITaxonomy, name=utility_name)

        if taxonomy and self.environ.shouldPurge():
            taxonomy.clear()

        iterator = TermIterator(tree, self.IMSVDEX_NS)

        for (identifier, langstrings) in iterator:
            taxonomy.add(int(identifier), langstrings)

        return utility_name

    def exportDocument(self, name):
        taxonomy = queryUtility(ITaxonomy, name=name)

        root = ElementTree.Element('vdex', attrib={'xmlns' : "http://www.imsglobal.org/xsd/imsvdex_v1p0",
                                                   'xmlns:xsi' : "http://www.w3.org/2001/XMLSchema-instance",
                                                   'xsi:schemaLocation' : "http://www.imsglobal.org/xsd/imsvdex_v1p0 "
                                                                          "imsvdex_v1p0.xsd "
                                                                          "http://www.imsglobal.org/xsd/imsmd_rootv1p2p1 "
                                                                          "imsmd_rootv1p2p1.xsd",
                                                   'orderSignificant' : 'false',
                                                   'profileType' : 'hierarchicalTokenTerms',
                                                   'language' : 'en'})

        vocabName = ElementTree.Element('vocabName')
        root.append(vocabName)

        langstring = ElementTree.Element('langstring', attrib={'language' : 'en'})
        langstring.text = taxonomy.title

        vocabName.append(langstring)

        vocabIdentifier = ElementTree.Element('vocabIdentifier')
        vocabIdentifier.text = name

        root.append(vocabIdentifier)

        for i in taxonomy.items():
            print i

        return prettyXML(root)


class TermIterator(object):
    def __init__(self, tree, ns):
        self.tree = tree
        self.ns = ns

    def __iter__(self):
        for (k,v) in self.recurse(self.tree):
            yield (k,v)

    def recurse(self, tree, path=tuple()):
        result = []

        for node in tree.findall('./{%s}term' % self.ns):
            identifier = node.find('./{%s}termIdentifier' % self.ns)
            print identifier.text
            langstrings = node.findall('./{%s}caption/{%s}langstring' % (self.ns, self.ns))
            result += self.recurse(node, list(path) +  [identifier.text])
            result += [(identifier.text, '/'.join(path))]

        return result



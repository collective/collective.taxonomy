from elementtree import ElementTree

from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory

from .interfaces import ITaxonomy
from .utility import Taxonomy

from plone.supermodel.utils import indent


def importTaxonomy(context):
    for filename in context.listDirectory('taxonomies/'):
        body = context.readDataFile('taxonomies/' + filename)
        if body is not None:
            importer = TaxonomyImportExportAdapter(context)
            importer.importDocument(body)

def exportTaxonomy(context):
    site = context.getSite()
    for (name, taxonomy) in site.getSiteManager().getUtilitiesFor(ITaxonomy):
        short_name = name.split('.')[-1]
        exporter = TaxonomyImportExportAdapter(context)
        body = exporter.exportDocument(name)
        if body is not None:
            context.writeDataFile(short_name + '.xml', body, 'text/xml')


class ImportVdex(object):
    def __init__(self, tree, ns):
        self.tree = tree
        self.ns = ns

    def __call__(self):
        languages = set()
        results = self.recurse(self.tree, languages)
        final_results = {}
        for language in languages:
            final_results[language] = self.processLanguage(results, language)

        return final_results

    def processLanguage(self, results, language, path=('',)):
        result = {}
        for element in results.keys():
            (lang, identifier, children) = results[element]
            if lang == language:
                extended_path = '/'.join(path) + '/' + element
                result[extended_path] = identifier
                result.update(self.processLanguage(children, language,
                                                   path + (element,)))
        return result

    def recurse(self, tree, available_languages=set(),
                parent_language=None):
        result = {}

        for node in tree.findall('./{%s}term' % self.ns):
            identifier = node.find('./{%s}termIdentifier' % self.ns)
            langstrings = node.findall('./{%s}caption/{%s}langstring' %
                                       (self.ns, self.ns))
            for i in langstrings:
                if not parent_language or \
                        parent_language == i.attrib['language']:
                    result[i.text] = (
                        i.attrib['language'],
                        int(identifier.text),
                        self.recurse(node, available_languages,
                                     i.attrib['language'])
                    )

                available_languages.add(i.attrib['language'])

        return result


class ExportVdex(object):
    def __init__(self, taxonomy):
        self.taxonomy = taxonomy

    def buildFinalPathIndex(self, node, tree):
        results = {}

        for i in node:
            # leaf
            if not i in tree:
                results[i] = {}
            else:
                results[i] = self.buildFinalPathIndex(tree[i], tree)

        return results

    def buildPathIndex(self):
        pathIndex = {}

        for (language, children) in self.taxonomy.data.items():
            for (path, identifier) in children.items():
                parent_path = path.split('/')[:-1]
                parent_identifier = children.get('/'.join(parent_path))
                if not parent_identifier in pathIndex:
                    pathIndex[parent_identifier] = set()
                pathIndex[parent_identifier].add(identifier)

        if None not in pathIndex:
            raise Exception("No root node!")

        return self.buildFinalPathIndex(pathIndex[None], pathIndex)

    def makeTranslationTable(self):
        translationTable = {}

        for (language, children) in self.taxonomy.data.items():
            for (path, identifier) in children.items():
                if not identifier in translationTable:
                    translationTable[identifier] = {}

                translationTable[identifier][language] = \
                    path[path.rfind('/') + 1:]

        return translationTable

    def makeSubtree(self, index, table):
        termnodes = []
        for identifier in index.keys():
            termnode = ElementTree.Element('term')
            identifiernode = ElementTree.Element('termIdentifier')
            identifiernode.text = str(identifier)
            captionnode = ElementTree.Element('caption')

            translations = table[identifier].items()
            translations.sort(key=lambda (language, langstring): language)

            for (language, langstring) in translations:
                langstringnode = ElementTree.Element('langstring')
                langstringnode.text = langstring
                langstringnode.attrib['language'] = language
                captionnode.append(langstringnode)

            termnode.append(identifiernode)
            termnode.append(captionnode)

            for nestedtermnode in self.makeSubtree(index[identifier], table):
                termnode.append(nestedtermnode)

            # add to list
            termnodes.append(termnode)

        return termnodes


class TaxonomyImportExportAdapter(object):
    """Helper classt to import a registry file
    """

    IMSVDEX_NS = 'http://www.imsglobal.org/xsd/imsvdex_v1p0'
    IMSVDEX_ATTRIBS = {
        'xmlns': "http://www.imsglobal.org/xsd/imsvdex_v1p0",
        'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance",
        'xsi:schemaLocation': "http://www.imsglobal.org/xsd/imsvdex_v1p0 "
        "imsvdex_v1p0.xsd http://www.imsglobal.org/xsd/imsmd_rootv1p2p1 "
        "imsmd_rootv1p2p1.xsd",
        'orderSignificant': "false",
        'profileType': "hierarchicalTokenTerms",
        'language': "en"
    }
    IMSVDEX_ENCODING = 'utf-8'

    def __init__(self, context):
        self.context = context

    def importDocument(self, document):
        site = self.context.getSite()
        tree = ElementTree.fromstring(document)
        title = tree.find('./{%s}vocabName/{%s}langstring'
                          % (self.IMSVDEX_NS, self.IMSVDEX_NS))
        name = tree.find('./{%s}vocabIdentifier' % self.IMSVDEX_NS)

        utility_name = 'collective.taxonomy.' + name.text
        taxonomy = queryUtility(ITaxonomy, name=name.text)

        if not taxonomy:
            taxonomy = Taxonomy(utility_name, title.text)
            sm = site.getSiteManager()
            sm.registerUtility(taxonomy, ITaxonomy, name=utility_name)
            sm.registerUtility(taxonomy, IVocabularyFactory, name=utility_name)

        results = ImportVdex(tree, self.IMSVDEX_NS)()

        for (language, elements) in results.items():
            for (path, identifier) in elements.items():
                taxonomy.add(language, int(identifier), path)

        return utility_name

    def exportDocument(self, name):
        taxonomy = queryUtility(ITaxonomy, name=name)

        root = ElementTree.Element('vdex', attrib=self.IMSVDEX_ATTRIBS)

        vocabName = ElementTree.Element('vocabName')
        root.append(vocabName)

        langstring = ElementTree.Element('langstring',
                                         attrib={'language': 'en'})
        langstring.text = taxonomy.title

        vocabName.append(langstring)

        vocabIdentifier = ElementTree.Element('vocabIdentifier')
        vocabIdentifier.text = name.replace('collective.taxonomy.', '')

        root.append(vocabIdentifier)

        helper = ExportVdex(taxonomy)
        index = helper.buildPathIndex()
        table = helper.makeTranslationTable()
        for termnode in helper.makeSubtree(index, table):
            root.append(termnode)

        indent(root)
        treestring = ElementTree.tostring(root, self.IMSVDEX_ENCODING)
        header = """<?xml version="1.0" encoding="%s"?>""" % \
                 self.IMSVDEX_ENCODING.upper() + '\n'
        treestring = header + treestring
        return treestring

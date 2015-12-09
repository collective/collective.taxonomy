from elementtree import ElementTree
from plone.supermodel.utils import indent

from collective.taxonomy import PATH_SEPARATOR


LANG_SEPARATOR = '|'


class ImportVdex(object):
    """Helper class for import"""

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
            (identifier, children) = results[element]
            (lang, text) = element.split(LANG_SEPARATOR, 1)
            if lang == language:
                extended_path = PATH_SEPARATOR.join(path)
                extended_path = PATH_SEPARATOR.join((extended_path, text))
                result[extended_path] = identifier
                result.update(self.processLanguage(children, language,
                                                   path + (text,)))
        return result

    def recurse(self, tree, available_languages=set(), parent_language=None):
        result = {}

        for node in tree.findall('./{%s}term' % self.ns):
            identifier = node.find('./{%s}termIdentifier' % self.ns)
            langstrings = node.findall('./{%s}caption/{%s}langstring' %
                                       (self.ns, self.ns))
            for i in langstrings:
                if not parent_language or \
                        parent_language == i.attrib['language']:
                    if i.text is None:
                        text = ''
                    else:
                        text = i.text.strip('\n ')

                    element = LANG_SEPARATOR.join([i.attrib['language'], text])
                    result[element] = (
                        identifier.text,
                        self.recurse(node, available_languages,
                                     i.attrib['language'])
                    )

                available_languages.add(i.attrib['language'])

        return result


class TreeExport(object):

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
            if language == self.taxonomy.default_language:
                for (path, identifier) in children.items():
                    parent_path = path.split(PATH_SEPARATOR)[:-1]
                    parent_identifier = children.get(
                        PATH_SEPARATOR.join(parent_path))
                    if not parent_identifier in pathIndex:
                        pathIndex[parent_identifier] = set()
                    pathIndex[parent_identifier].add(identifier)

        if None not in pathIndex:
            raise ValueError("No root node!")

        return self.buildFinalPathIndex(pathIndex[None], pathIndex)

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
                langstringnode.attrib['language'] = language or self.taxonomy.default_language or ''
                captionnode.append(langstringnode)

            termnode.append(identifiernode)
            termnode.append(captionnode)

            for nestedtermnode in self.makeSubtree(index[identifier], table):
                termnode.append(nestedtermnode)

            # add to list
            termnodes.append(termnode)

        return termnodes

    def makeTranslationTable(self):
        translationTable = {}

        for (language, children) in self.taxonomy.data.items():
            for (path, identifier) in children.items():
                if not identifier in translationTable:
                    translationTable[identifier] = {}

                translationTable[identifier][language] = \
                    path[path.rfind(PATH_SEPARATOR) + 1:]

        return translationTable

    def buildTree(self, root):
        index = self.buildPathIndex()
        table = self.makeTranslationTable()
        for termnode in self.makeSubtree(index, table):
            root.append(termnode)

        return root


class ExportVdex(TreeExport):
    """Helper class for import"""

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

    def __init__(self, taxonomy):
        self.taxonomy = taxonomy

    def __call__(self, as_string=False):
        taxonomy = self.taxonomy

        attrib = self.IMSVDEX_ATTRIBS
        attrib['language'] = taxonomy.default_language or ''

        root = ElementTree.Element('vdex', attrib=attrib)

        vocabName = ElementTree.Element('vocabName')
        root.append(vocabName)

        langstring = ElementTree.Element(
            'langstring',
            attrib={'language': taxonomy.default_language or ''}
        )
        langstring.text = taxonomy.title
        vocabName.append(langstring)

        vocabIdentifier = ElementTree.Element('vocabIdentifier')
        vocabIdentifier.text = self.taxonomy.name.replace(
            'collective.taxonomy.', ''
        )
        root.append(vocabIdentifier)

        root = self.buildTree(root)

        if as_string:
            indent(root)
            treestring = ElementTree.tostring(root, self.IMSVDEX_ENCODING)
            header = """<?xml version="1.0" encoding="%s"?>""" % \
                     self.IMSVDEX_ENCODING.upper() + '\n'
            treestring = header + treestring
            return treestring
        else:
            return root

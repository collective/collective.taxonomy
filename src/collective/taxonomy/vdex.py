from collections import OrderedDict
from collective.taxonomy import PATH_SEPARATOR
from lxml import etree
from plone.supermodel.utils import indent


LANG_SEPARATOR = "|"


class ImportVdex:
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

    def processLanguage(self, results, language, path=("",)):
        result = []
        for element in results.keys():
            (identifier, children) = results[element]
            (lang, text) = element.split(LANG_SEPARATOR, 1)
            if lang == language:
                extended_path = PATH_SEPARATOR.join(path)
                extended_path = PATH_SEPARATOR.join((extended_path, text))
                result.append((extended_path, identifier))
                result.extend(self.processLanguage(children, language, path + (text,)))
        return result

    def recurse(self, tree, available_languages=set(), parent_language=None):
        result = OrderedDict()

        for node in tree.findall("./{%s}term" % self.ns):
            identifier = node.find("./{%s}termIdentifier" % self.ns)
            langstrings = node.findall(
                f"./{{{self.ns}}}caption/{{{self.ns}}}langstring"
            )
            for i in langstrings:
                if not parent_language or parent_language == i.attrib["language"]:
                    if i.text is None:
                        text = ""
                    else:
                        text = i.text.strip("\n ")

                    element = LANG_SEPARATOR.join([i.attrib["language"], text])
                    result[element] = (
                        identifier.text,
                        self.recurse(node, available_languages, i.attrib["language"]),
                    )

                available_languages.add(i.attrib["language"])

        return result


class TreeExport:
    def __init__(self, taxonomy):
        self.taxonomy = taxonomy

    def buildFinalPathIndex(self, node, tree):
        results = OrderedDict()

        for i in node:
            # leaf
            if i not in tree:
                results[i] = OrderedDict()
            else:
                results[i] = self.buildFinalPathIndex(tree[i], tree)

        return results

    def buildPathIndex(self):
        pathIndex = OrderedDict()

        for path, identifier, parent in self.taxonomy.iterLanguage():
            pathIndex.setdefault(parent, []).append(identifier)

        if None not in pathIndex:
            raise ValueError("No root node!")

        return self.buildFinalPathIndex(pathIndex[None], pathIndex)

    def makeSubtree(self, index, table):
        termnodes = []

        for identifier in index.keys():
            termnode = etree.Element("term")
            identifiernode = etree.Element("termIdentifier")
            identifiernode.text = str(identifier)
            captionnode = etree.Element("caption")
            translations = sorted(table[identifier].items())

            for language, langstring in translations:
                langstringnode = etree.Element("langstring")
                langstringnode.text = langstring
                langstringnode.attrib["language"] = (
                    language or self.taxonomy.default_language or ""
                )  # noqa: E501
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

        for lang in self.taxonomy.getLanguages():
            for path, identifier, parent in self.taxonomy.iterLanguage(lang):
                if identifier not in translationTable:
                    translationTable[identifier] = {}
                index = path.rfind(PATH_SEPARATOR) + 1
                translationTable[identifier][lang] = path[index:]

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
        "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation": "http://www.imsglobal.org/xsd/imsvdex_v1p0 "
        "imsvdex_v1p0.xsd http://www.imsglobal.org/xsd/imsmd_rootv1p2p1 "
        "imsmd_rootv1p2p1.xsd",
        "orderSignificant": "false",
        "profileType": "hierarchicalTokenTerms",
        "language": "en",
    }
    NSMAP = {
        None: "http://www.imsglobal.org/xsd/imsvdex_v1p0",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    }
    IMSVDEX_ENCODING = "utf-8"

    def __init__(self, taxonomy):
        self.taxonomy = taxonomy

    def __call__(self, as_string=False):
        taxonomy = self.taxonomy

        attrib = self.IMSVDEX_ATTRIBS
        attrib["language"] = taxonomy.default_language or ""

        root = etree.Element("vdex", attrib=attrib, nsmap=self.NSMAP)

        vocabName = etree.Element("vocabName")
        root.append(vocabName)

        langstring = etree.Element(
            "langstring", attrib={"language": taxonomy.default_language or ""}
        )
        langstring.text = taxonomy.title
        vocabName.append(langstring)

        vocabIdentifier = etree.Element("vocabIdentifier")
        vocabIdentifier.text = self.taxonomy.name.replace("collective.taxonomy.", "")
        root.append(vocabIdentifier)

        root = self.buildTree(root)

        if as_string:
            indent(root)
            treestring = etree.tostring(
                root, encoding=self.IMSVDEX_ENCODING, xml_declaration=True
            )
            return treestring
        else:
            return root

from collective.taxonomy.interfaces import ITaxonomy
from collective.taxonomy.restapi.utils import get_all_taxonomies
from collective.taxonomy.vdex import TreeExport
from lxml import etree
from plone.api import portal
from plone.restapi.services import Service
from zope.component import queryUtility
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse


@implementer(IPublishTraverse)
class TaxonomyGet(Service, TreeExport):
    def __init__(self, context, request):
        self.params = []
        self.taxonomy = []
        self.context = context
        self.request = request

    def publishTraverse(self, request, name):
        # Treat any path segments after /@taxonomy as parameters
        self.params.append(name)
        taxonomy = queryUtility(ITaxonomy, name=self.params[0])
        self.taxonomy = taxonomy
        return self

    def reply(self):
        if not self.params:
            return get_all_taxonomies(full_objects=False)
        if len(self.params) == 1:
            # taxonomy = get_taxonomy_by_name(name=self.params[0])
            taxonomy = self.get_data()
            if taxonomy is None:
                self.request.response.setStatus(404)
                return
            return taxonomy

        # any other case
        self.request.response.setStatus(404)
        return

    def get_data(self):
        """Get json data."""
        site = portal.get()
        root = etree.Element("vdex")
        try:
            root = self.buildTree(root)
        except ValueError:
            root = None
        result = {
            "key": "0",
            "name": self.taxonomy.name,
            "title": self.taxonomy.title,
            "description": self.taxonomy.description,
            "fieldset": getattr(self.taxonomy, "fieldset", "categorization"),
            "prefix": getattr(self.taxonomy, "prefix", "taxonomy_"),
            "@id": f"{site.absolute_url()}/@taxonomy/{self.taxonomy.name}",
            "tree": [],
            "default_language": self.taxonomy.default_language,
        }
        if root is not None:
            for term in root.findall("term"):
                result["tree"].append(self.generate_json(term))
        return result

    def generate_json(self, root):
        item = {}
        item["key"] = root.find("termIdentifier").text
        captionnode = root.find("caption")
        translations = {}
        for langstringnode in captionnode.getchildren():
            translations[langstringnode.get("language")] = langstringnode.text

        item["translations"] = translations
        item["title"] = translations.get(
            self.taxonomy.default_language, "en"
        )  # todo:support for translated titles
        item["children"] = []
        terms = root.findall("term")
        if terms:
            for child in terms:
                item["children"].append(self.generate_json(child))

        return item

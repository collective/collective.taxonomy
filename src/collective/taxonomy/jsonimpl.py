from BTrees.OOBTree import OOBTree
from collective.taxonomy import PATH_SEPARATOR
from collective.taxonomy.i18n import CollectiveTaxonomyMessageFactory as _
from collective.taxonomy.interfaces import ITaxonomy
from collective.taxonomy.vdex import TreeExport
from lxml import etree
from plone import api
from plone.app.vocabularies.language import AvailableContentLanguageVocabularyFactory
from Products.Five.browser import BrowserView
from zope.component import queryUtility
from zope.i18n import translate

import json
import os


class EditTaxonomyData(TreeExport, BrowserView):
    """Taxonomy tree edit view."""

    def __init__(self, context, request):
        self.context = context
        self.request = request
        utility_name = request.get("taxonomy", "")
        taxonomy = queryUtility(ITaxonomy, name=utility_name)
        if not taxonomy:
            raise ValueError(
                "Taxonomy `%s` could not be found." % utility_name
            )  # noqa: E501

        self.taxonomy = taxonomy

    def generate_json(self, root):
        item = {}
        item["key"] = root.find("termIdentifier").text
        captionnode = root.find("caption")
        translations = {}
        for langstringnode in captionnode.getchildren():
            translations[langstringnode.get("language")] = langstringnode.text

        item["translations"] = translations
        item["subnodes"] = []
        terms = root.findall("term")
        if terms:
            for child in terms:
                item["subnodes"].append(self.generate_json(child))

        return item

    def get_data(self):
        """Get json data."""
        root = etree.Element("vdex")
        try:
            root = self.buildTree(root)
        except ValueError:
            root = None

        result = {
            "key": "0",
            "name": self.taxonomy.name,
            "title": self.taxonomy.title,
            "subnodes": [],
            "default_language": self.taxonomy.default_language,
        }
        if root is not None:
            for term in root.findall("term"):
                result["subnodes"].append(self.generate_json(term))

        return json.dumps(result)

    def get_languages_mapping(self):
        """Get mapping token/value for languages."""
        vocab = AvailableContentLanguageVocabularyFactory(self.context)
        language_tool = api.portal.get_tool("portal_languages")
        plone_selected_languages = language_tool.supported_langs
        taxonomy_languages_translations = {
            language: vocab.getTermByToken(language).title
            for language in plone_selected_languages
        }
        # Add previous taxonomy translations that currently are not in Plone selected languages
        for language in self.taxonomy.inverted_data.keys():
            if language in taxonomy_languages_translations:
                continue
            term = vocab.getTermByToken(language)
            taxonomy_languages_translations[language] = getattr(term, "title", language)
        return json.dumps(taxonomy_languages_translations)

    def get_resource_url(self):
        """Return resource url."""
        node_env = os.environ.get("NODE_ENV", "production")
        if node_env == "development" and api.env.debug_mode():
            return "http://localhost:3000/static/edittaxonomydata.js"
        else:
            return "{}/++resource++taxonomy/js/edittaxonomydata.js".format(
                api.portal.get().absolute_url()
            )


class ImportJson(BrowserView):
    """Update taxonomy using json data."""

    def __call__(self):
        request = self.request
        if request.method == "POST":
            data = json.loads(request.get("BODY", ""))
            taxonomy = queryUtility(ITaxonomy, name=data["taxonomy"])
            tree = data["tree"]
            languages = data["languages"]
            for language in languages:
                if language not in taxonomy.data:
                    taxonomy.data[language] = OOBTree()

            for language in taxonomy.data.keys():
                data_for_taxonomy = self.generate_data_for_taxonomy(
                    tree["subnodes"], language
                )

                # Update taxonomy and use 'clear' since we want to remain with
                # just the items that were submitted by the user.
                taxonomy.update(language, data_for_taxonomy, True)

            return json.dumps(
                {
                    "status": "info",
                    "message": translate(
                        _("Your taxonomy has been saved with success."), context=request
                    ),
                }
            )

        return json.dumps(
            {
                "status": "error",
                "message": translate(
                    _("There seems to have been an error."), context=request
                ),
            }
        )

    def generate_data_for_taxonomy(self, parsed_data, language, path=PATH_SEPARATOR):
        result = []
        for item in parsed_data:
            new_key = item["key"]
            title = item["translations"].get(language, "")
            new_path = f"{path}{title}"
            result.append(
                (
                    new_path,
                    new_key,
                )
            )
            subnodes = item.get("subnodes", [])
            if subnodes:
                new_path = f"{new_path}{PATH_SEPARATOR}"
                result.extend(
                    self.generate_data_for_taxonomy(subnodes, language, new_path)
                )

        return result

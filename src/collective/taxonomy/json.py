from elementtree import ElementTree
import os
import simplejson

from BTrees.OOBTree import OOBTree
from Products.Five.browser import BrowserView
from plone import api
from zope.component import queryMultiAdapter, queryUtility
from zope.i18n import translate

from collective.taxonomy import PATH_SEPARATOR
from collective.taxonomy.i18n import MessageFactory as _
from collective.taxonomy.interfaces import ITaxonomy
from collective.taxonomy.vdex import TreeExport


class EditTaxonomyData(TreeExport, BrowserView):

    """Taxonomy tree edit view."""

    def __init__(self, context, request):
        self.context = context
        self.request = request
        utility_name = self.context.REQUEST.get('taxonomy', '')
        taxonomy = queryUtility(ITaxonomy, name=utility_name)
        if not taxonomy:
            raise ValueError('Taxonomy could not be found.')

        self.taxonomy = taxonomy

    def generate_json(self, root):
        item = {}
        item['key'] = root.find('termIdentifier').text
        captionnode = root.find('caption')
        translations = {}
        for langstringnode in captionnode.getchildren():
            translations[langstringnode.get('language')] = langstringnode.text

        item['translations'] = translations
        item['subnodes'] = []
        terms = root.findall('term')
        if terms:
            for child in terms:
                item['subnodes'].append(self.generate_json(child))

        return item

    def get_data(self):
        """Get json data."""
        root = ElementTree.Element('vdex')
        try:
            root = self.buildTree(root)
        except ValueError:
            root = None

        result = {
            'key': '0',
            'name': self.taxonomy.name,
            'title': self.taxonomy.title,
            'subnodes': [],
            'default_language': self.taxonomy.default_language,
        }
        if root:
            for term in root.findall('term'):
                result['subnodes'].append(self.generate_json(term))

        return simplejson.dumps(result)

    def get_languages_mapping(self):
        """Get mapping token/value for languages."""
        portal = api.portal.get()
        portal_state = queryMultiAdapter(
            (portal, portal.REQUEST), name=u'plone_portal_state')
        mapping = portal_state.locale().displayNames.languages
        language_tool = api.portal.get_tool('portal_languages')
        supported_langs = language_tool.supported_langs
        languages_mapping = dict(
            [(lang, mapping[lang].capitalize()) for lang in supported_langs])

        # add taxonomy's default language if it is not in supported langs
        default_lang = self.taxonomy.default_language
        languages_mapping[default_lang] = mapping[default_lang].capitalize()
        return simplejson.dumps(languages_mapping)

    def get_resource_url(self):
        """Return resource url."""
        node_env = os.environ.get('NODE_ENV', 'production')
        if node_env == 'development' and api.env.debug_mode():
            return "http://localhost:3000/static/edittaxonomydata.js"
        else:
            return '{}/++resource++taxonomy/edittaxonomydata.js'.format(
                api.portal.get().absolute_url())


class ImportJson(BrowserView):

    """Update taxonomy using json data."""

    def __call__(self):
        request = self.request
        if request.method == 'POST':
            request.stdin.seek(0)
            data = simplejson.loads(request.stdin.read())
            taxonomy = queryUtility(ITaxonomy, name=data['taxonomy'])
            tree = data['tree']
            languages = data['languages']
            for language in languages:
                if language not in taxonomy.data:
                    taxonomy.data[language] = OOBTree()

            for language in taxonomy.data.keys():
                data_for_taxonomy = self.generate_data_for_taxonomy(
                    tree['subnodes'], language)

                taxonomy.data[language] = OOBTree()
                for key, value in data_for_taxonomy:
                    taxonomy.data[language][key] = value

            return simplejson.dumps({
                'status': 'info',
                'message': translate(
                    _("Your taxonomy has been saved with success."),
                    context=request)
            })

        return simplejson.dumps({
            'status': 'error',
            'message': translate(
                _("There seems to have been an error."),
                context=request)
            })

    def generate_data_for_taxonomy(self, parsed_data, language,
                                   path=PATH_SEPARATOR):
        result = []
        for item in parsed_data:
            new_key = item['key']
            title = item['translations'].get(language, '')
            new_path = u'{}{}'.format(path, title)
            result.append((new_path, new_key, ))
            subnodes = item.get('subnodes', [])
            if subnodes:
                new_path = u'{}{}'.format(new_path, PATH_SEPARATOR)
                result.extend(self.generate_data_for_taxonomy(
                    subnodes, language, new_path))

        return result

from elementtree import ElementTree
import simplejson

from BTrees.OOBTree import OOBTree
from Products.Five.browser import BrowserView
from zope.component import queryUtility
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
            'default_language': self.taxonomy.default_language
        }
        if root:
            for term in root.findall('term'):
                result['subnodes'].append(self.generate_json(term))

        return simplejson.dumps(result)


class ImportJson(BrowserView):

    """Update taxonomy using json data."""

    def __call__(self):
        request = self.request
        if request.method == 'POST':
            request.stdin.seek(0)
            data = simplejson.loads(request.stdin.read())
            taxonomy = queryUtility(ITaxonomy, name=data['taxonomy'])
            tree = data['tree']
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
            new_path = path + item['translations'][language]
            result.append((new_path, new_key, ))
            for child in item.get('subnodes', []):
                title = item['translations'][language]
                new_path = path + title + PATH_SEPARATOR
                result.append(self.generate_data_for_taxonomy(
                    child, new_path, language))

        return result

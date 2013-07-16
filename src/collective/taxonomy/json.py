from elementtree import ElementTree

from BTrees.OOBTree import OOBTree
from Products.Five.browser import BrowserView
from zope.component import queryUtility

from interfaces import ITaxonomy
from vdex import TreeExport

import simplejson
import uuid


class Json(TreeExport, BrowserView):
    def __init__(self, context, request):
        self.context = context
        self.request = request

        utility_name = self.context.REQUEST.get('taxonomy', '')

        taxonomy = queryUtility(ITaxonomy, name=utility_name)
        if not taxonomy:
            raise ValueError('Taxonomy could not be found.')

        self.taxonomy = taxonomy

    def readJsonData(self, data):
        result = {}

        result['children'] = []
        for child in data.get('children', []):
            result['children'].append(self.readJsonData(child))

        result['title'] = data['title']
        result['key'] = data['key']

        return result

    def generateKey(self):
        return str(uuid.uuid4())

    def generateDataForTaxonomy(self, parsed_data, path='/', ignore=False):
        result = []
        if not ignore:
            new_key = not parsed_data['key'].startswith('_') and parsed_data['key'] or self.generateKey()
            new_path = path + parsed_data['title']
            result.append((new_path, new_key, ))

        for child in parsed_data.get('children', []):
            new_path = ignore and path or path + parsed_data['title'] + '/'
            result += self.generateDataForTaxonomy(child, new_path)

        return result

    def importJson(self):
        data = self.request.get('data', '')

        data = simplejson.loads(data)
        parsed_data = self.readJsonData(data)
        parsed_data = parsed_data['children'][0]

        # XXX: Support multiple languages
        language = self.taxonomy.default_language
        data_for_taxonomy = self.generateDataForTaxonomy(
            parsed_data, ignore=True
        )

        self.taxonomy.data[language] = OOBTree()
        for (key, value) in data_for_taxonomy:
            self.taxonomy.data[language][key] = value

    def generateJson(self, root):
        item = {}
        item['key'] = root.find('termIdentifier').text
        item['title'] = root.find('caption').find('langstring').text
        item['isFolder'] = True
        item['children'] = []

        for child in root.findall('term'):
            item['children'].append(self.generateJson(child))

        return item

    def exportJson(self):
        self.request.RESPONSE.setHeader('Content-type', 'application/json')
        root = ElementTree.Element('vdex')
        try:
            root = self.buildTree(root)
        except ValueError:
            root = None
            pass

        result = {
            'key': 'root',
            'title': 'Taxonomy',
            'children': [],
            'isFolder': True
        }
        if root:
            for term in root.findall('term'):
                result['children'].append(self.generateJson(term))

        return simplejson.dumps([result])

    def __call__(self):
        if 'update_taxonomy' in self.request:
            return self.importJson()
        else:
            return self.exportJson()

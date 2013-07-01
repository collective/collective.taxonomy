from elementtree import ElementTree

from Products.Five.browser import BrowserView
from zope.component import queryUtility

from interfaces import ITaxonomy
from vdex import TreeExport

import simplejson


class ExportJson(TreeExport, BrowserView):
    def __init__(self, context, request):
        self.context = context
        self.request = request

        utility_name = self.context.REQUEST.get('taxonomy', '')

        taxonomy = queryUtility(ITaxonomy, name=utility_name)
        if not taxonomy:
            raise ValueError('Taxonomy could not be found.')

        self.taxonomy = taxonomy

    def generateJson(self, root):
        item = {}
        item['key'] = root.find('termIdentifier').text
        item['title'] = root.find('caption').find('langstring').text
        item['isFolder'] = True
        item['children'] = []

        for child in root.findall('term'):
            item['children'].append(self.generateJson(child))

        return item

    def __call__(self):
        self.request.RESPONSE.setHeader('Content-type', 'application/json')
        root = ElementTree.Element('vdex')
        root = self.buildTree(root)
        result = []
        for term in root.findall('term'):
            result.append(self.generateJson(term))

        return simplejson.dumps(result)

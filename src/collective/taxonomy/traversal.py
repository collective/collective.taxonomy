import os

from zExceptions import BadRequest, NotFound

from zope.interface import implements
from zope.component import adapts,queryUtility
from zope.traversing.interfaces import ITraversable
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.publisher.interfaces.browser import IBrowserRequest

from interfaces import ITaxonomy

class TaxonomyTraverser(object):
    implements(ITraversable)
    adapts(IAttributeAnnotatable, IBrowserRequest)

    vdex_file_contents = open(os.path.dirname(__file__) +
                              "/tests/examples/nihms.xml").read()

    def __init__(self, context, request=None):
        self.context = context
        self.request = request

    @property
    def adapter(self):
        from collective.taxonomy.exportimport \
            import TaxonomyImportExportAdapter

        portal = self.context
        return TaxonomyImportExportAdapter(portal)

    def traverse(self, name, ignore):
        arr = name.split('.')
        (action, taxonomy, ) = arr

        if action == 'add':
            utility_name = self.adapter.importDocument(self.vdex_file_contents)
            utility = queryUtility(ITaxonomy, name=utility_name)




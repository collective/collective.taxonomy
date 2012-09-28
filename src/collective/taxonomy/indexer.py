from plone.indexer.interfaces import IIndexer
from plone.dexterity.interfaces import IDexterityContent
from Products.ZCatalog.interfaces import IZCatalog

from zope.component import adapts, provideAdapter
from zope.interface import implements


class TaxonomyIndexer(object):
    implements(IIndexer)
    adapts(IDexterityContent, IZCatalog)

    def __init__(self, context, catalog=None):
        self.context = context
        self.catalog = catalog
    def __call__(self):
        import pdb; pdb.set_trace()



from plone.indexer.interfaces import IIndexer
from plone.dexterity.interfaces import IDexterityContent

from Products.ZCatalog.interfaces import IZCatalog

from zope.component import adapts
from zope.interface import classImplements

from .interfaces import ITaxonomy

import collections
import logging
logger = logging.getLogger("collective.taxonomy")


class TaxonomyIndexerWrapper(object):

    def __init__(self, field_name, utility_name, context, catalog):
        self.context = context
        self.catalog = catalog
        self.field_name = field_name
        self.utility_name = utility_name

    def __call__(self):
        # Dirty hack to ensure that it is not an item in a
        # folder

        if self.field_name not in self.context.__dict__:
            return []

        sm = self.context.portal_url.getSiteManager()
        utility = sm.queryUtility(ITaxonomy, name=self.utility_name)

        if not utility:
            logging.info("Utility has disappeared..!")
            return []

        if not utility.data:
            # skip empty taxonomy
            return []

        found = []
        stored_element = getattr(self.context, self.field_name)
        if not isinstance(stored_element, collections.Iterable):
            stored_element = [stored_element]

        for (language, data) in utility.data.items():
            for (identifier, path) in utility.inverted_data[language].items():
                if identifier in stored_element:
                    found.append((identifier, language, path,))

        result = []
        for (key, value) in utility.inverted_data[language].items():
            for (found_identifier, found_language, found_path) in found:
                in_path = False
                for s in value.split('/'):
                    if s != '' and s in found_path.split('/'):
                        in_path = True
                    else:
                        in_path = False

                if in_path:
                    if key not in result:
                        result.append(key)

        return result


class TaxonomyIndexer(object):
    __name__ = 'TaxonomyIndexer'

    classImplements(IIndexer)
    adapts(IDexterityContent, IZCatalog)

    def __init__(self, field_name, utility_name):
        self.field_name = field_name
        self.utility_name = utility_name

    def __call__(self, context, catalog):
        return TaxonomyIndexerWrapper(self.field_name, self.utility_name,
                                      context, catalog)

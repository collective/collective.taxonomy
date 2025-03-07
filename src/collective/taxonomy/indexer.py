from Acquisition import aq_base
from Acquisition import aq_parent
from collections.abc import Iterable
from collective.taxonomy import PATH_SEPARATOR
from collective.taxonomy.interfaces import ITaxonomy
from plone import api
from plone.base.interfaces import IPloneSiteRoot
from plone.dexterity.interfaces import IDexterityContent
from plone.indexer.interfaces import IIndexer
from Products.ZCatalog.interfaces import IZCatalog
from zope.component import adapter
from zope.interface import implementer

import logging


logger = logging.getLogger("collective.taxonomy")


class TaxonomyIndexerWrapper:
    def __init__(self, field_name, utility_name, context, catalog):
        self.context = context
        self.catalog = catalog
        self.field_name = field_name
        self.utility_name = utility_name

    def __call__(self):
        # field needs to be defined in the context, not by acquisition or containment
        if not hasattr(aq_base(self.context), self.field_name):
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
        if not isinstance(stored_element, Iterable) or isinstance(stored_element, str):
            stored_element = [stored_element]

        lang = get_language(self.context)
        if lang not in utility.inverted_data:
            lang = utility.default_language

        for identifier in stored_element:
            path = utility.inverted_data[lang].get(identifier)
            if path is not None:
                found.append(
                    (
                        identifier,
                        lang,
                        path,
                    )
                )

        result = []

        for found_identifier, found_language, found_path in found:
            for key, value in utility.inverted_data[lang].items():
                value_split = value.split(PATH_SEPARATOR)
                found_split = found_path.split(PATH_SEPARATOR)[: len(value_split)]
                if found_split == value_split and key not in result:
                    result.append(key)

        return result


@adapter(IDexterityContent, IZCatalog)
@implementer(IIndexer)
class TaxonomyIndexer:
    __name__ = "TaxonomyIndexer"

    def __init__(self, field_name, utility_name):
        self.field_name = field_name
        self.utility_name = utility_name

    def __call__(self, context, catalog):
        return TaxonomyIndexerWrapper(
            self.field_name, self.utility_name, context, catalog
        )


def get_language(obj):
    lang = getattr(obj, "language", None)
    if lang:
        return lang
    elif not IPloneSiteRoot.providedBy(obj):
        lang = get_language(aq_parent(obj))
    else:
        lang = api.portal.get_default_language()
    return lang

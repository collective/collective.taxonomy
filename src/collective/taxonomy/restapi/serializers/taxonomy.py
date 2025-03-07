""" RestAPI Taxonomy serializer
"""

from collective.taxonomy import PATH_SEPARATOR
from collective.taxonomy.interfaces import ITaxonomy
from plone.api import portal
from plone.restapi.interfaces import ISerializeToJson
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(ISerializeToJson)
@adapter(ITaxonomy, Interface)
class TaxonomySerializer:
    """Taxonomy serializer"""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, full_objects=False):
        site = portal.get()
        util = self.context
        results = {
            "@id": f"{site.absolute_url()}/@taxonomy/{util.name}",
            "name": util.name,
            "title": util.title,
            "default_language": util.default_language,
            "count": dict(util.count),
        }

        if full_objects:
            results["data"] = {}
            results["order"] = {}
            for lang, langdata in util.data.items():
                # keys = [langdata.keys()[x] for x in order]
                results["data"][lang] = [
                    {
                        # TO DO: do subpaths
                        "title": k.replace(PATH_SEPARATOR, ""),
                        "token": langdata[k],
                    }
                    for k in langdata.keys()
                ]
                order = util.order[lang]
                results["order"][lang] = list(order)

        return results

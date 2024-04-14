from collective.taxonomy.interfaces import ITaxonomy
from plone.restapi.interfaces import ISerializeToJson
from zope.component import getMultiAdapter
from zope.component import getUtilitiesFor
from zope.globalrequest import getRequest


def get_all_taxonomies(full_objects=True):
    request = getRequest()
    utils = list(getUtilitiesFor(ITaxonomy))
    return [
        getMultiAdapter((util, request), ISerializeToJson)(full_objects=full_objects)
        for (_name, util) in utils
    ]


def get_taxonomy_by_name(name, full_objects=True):
    request = getRequest()
    utils = list(getUtilitiesFor(ITaxonomy))
    for _name, util in utils:
        if _name == name:
            return getMultiAdapter((util, request), ISerializeToJson)(
                full_objects=full_objects
            )
    return None

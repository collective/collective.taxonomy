# -*- coding: utf-8 -*-
from collective.taxonomy.interfaces import ITaxonomy
from plone.restapi.interfaces import ISerializeToJson
from zope.component import getMultiAdapter
from zope.component import getUtilitiesFor
from zope.globalrequest import getRequest


def get_all_taxonomies():
    request = getRequest()
    utils = list(getUtilitiesFor(ITaxonomy))
    return [
        getMultiAdapter((util, request), ISerializeToJson)(full_objects=True)
        for (_name, util) in utils
    ]


def get_taxonomy_by_name(name):
    request = getRequest()
    utils = list(getUtilitiesFor(ITaxonomy))
    for (_name, util) in utils:
        if _name == name:
            return getMultiAdapter((util, request), ISerializeToJson)(full_objects=True)
    return None

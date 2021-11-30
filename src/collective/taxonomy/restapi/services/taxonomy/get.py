# -*- coding: utf-8 -*-
from plone.restapi.services import Service
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse
from collective.taxonomy.restapi.utils import get_taxonomy_by_name
from collective.taxonomy.restapi.utils import get_all_taxonomies


@implementer(IPublishTraverse)
class TaxonomyGet(Service):
    def __init__(self, context, request):
        super().__init__(context, request)
        self.params = []

    def publishTraverse(self, request, name):
        # Treat any path segments after /@taxonomy as parameters
        self.params.append(name)
        return self

    def reply(self):
        if not self.params:
            return get_all_taxonomies()
        if len(self.params) == 1:
            taxonomy = get_taxonomy_by_name(name=self.params[0])
            if taxonomy is None:
                self.request.response.setStatus(404)
                return
            return taxonomy

        # any other case
        self.request.response.setStatus(404)
        return

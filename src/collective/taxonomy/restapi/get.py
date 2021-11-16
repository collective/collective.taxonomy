""" RestAPI GET
"""
# pylint: disable = R1710

from collective.taxonomy.interfaces import ITaxonomy
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.services import Service
from zope.component import getMultiAdapter, getUtilitiesFor, queryUtility
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse


@implementer(IPublishTraverse)
class TaxonomyGet(Service):
    """Taxonomy get service"""

    taxonomy_id = None

    def publishTraverse(self, request, name):  # noqa
        """Traverse"""
        if name:
            self.taxonomy_id = name

        return self

    def reply(self):
        """Reply"""
        if self.taxonomy_id:
            return self.reply_taxonomy()

        utils = list(getUtilitiesFor(ITaxonomy))
        res = {
            "@id": self.context.absolute_url() + "/@taxonomy-data",
            "items": [
                getMultiAdapter((util, self.request), ISerializeToJson)(
                    full_objects=True
                )
                for (_name, util) in utils
            ],
        }
        return res

    def reply_taxonomy(self):
        """Reply for taxonomy entry"""
        util = queryUtility(ITaxonomy, name=self.taxonomy_id)
        if util is None:
            self.request.response.setStatus(404)
            return

        serializer = getMultiAdapter((util, self.request), ISerializeToJson)
        return serializer(full_objects=True)

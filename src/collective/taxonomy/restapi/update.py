""" RestAPI PATCH
"""
from BTrees.OOBTree import OOBTree
from collective.taxonomy import PATH_SEPARATOR
from collective.taxonomy.interfaces import ITaxonomy
from plone.restapi.deserializer import json_body
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.services import Service
from zope.component import getMultiAdapter, queryUtility
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse


@implementer(IPublishTraverse)
class TaxonomyPatch(Service):
    """Patch a taxonomy"""

    taxonomy_id = None

    def publishTraverse(self, request, name):  # noqa
        """Traverse"""
        if name:
            self.taxonomy_id = name
        return self

    def reply(self):
        """Reply"""
        if not self.taxonomy_id:
            raise Exception("No taxonomy name provided")

        data = json_body(self.request)

        name = data.get("name")

        if name is None:
            raise Exception("No taxonomy name provided")

        taxonomy = queryUtility(ITaxonomy, name=name)
        if taxonomy is None:
            raise Exception("No taxonomy found for this name: {}".format(name))

        for language in data["data"].keys():
            tree = data["data"][language]
            order = data["order"][language]
            if language not in taxonomy.data:
                taxonomy.data[language] = OOBTree()

            data_for_taxonomy = []
            for i in order:
                item = tree[i]
                data_for_taxonomy.append(
                    [
                        u"{}{}".format(
                            PATH_SEPARATOR,
                            item["title"],
                        ),
                        item["token"],
                    ]
                )

            taxonomy.update(language, data_for_taxonomy, True)

        serializer = getMultiAdapter((taxonomy, self.request), ISerializeToJson)
        res = serializer(full_objects=True)

        return res

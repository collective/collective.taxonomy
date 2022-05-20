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

    def generate_data_for_taxonomy(self, parsed_data, language, path=PATH_SEPARATOR):
        result = []
        for item in parsed_data:
            new_key = item["key"]
            title = item["title"]
            new_path = "{}{}".format(path, title)
            result.append(
                (
                    new_path,
                    new_key,
                )
            )
            subnodes = item.get("children", [])
            if subnodes:
                new_path = "{}{}".format(new_path, PATH_SEPARATOR)
                result.extend(
                    self.generate_data_for_taxonomy(subnodes, language, new_path)
                )

        return result

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

        # for language in data["data"].keys():
        #     tree = data["data"][language]
        #     order = data["order"][language]
        #     if language not in taxonomy.data:
        #         taxonomy.data[language] = OOBTree()

        #     data_for_taxonomy = []
        #     for i in order:
        #         item = tree[i]
        #         data_for_taxonomy.append(
        #             [
        #                 "{}{}".format(
        #                     PATH_SEPARATOR,
        #                     item["title"],
        #                 ),
        #                 item["token"],
        #             ]
        #         )
        tree = data["tree"]
        languages = data["languages"]
        for language in languages:
            if language not in taxonomy.data:
                taxonomy.data[language] = OOBTree()

        for language in taxonomy.data.keys():
            data_for_taxonomy = self.generate_data_for_taxonomy(tree, language)

            taxonomy.update(language, data_for_taxonomy, True)

        # serializer = getMultiAdapter((taxonomy, self.request), ISerializeToJson)
        # res = serializer(full_objects=True)

        # from pprint import pprint
        # pprint(res)

        return self.reply_no_content()

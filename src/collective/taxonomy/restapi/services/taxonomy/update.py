"""RestAPI PATCH"""

from BTrees.OOBTree import OOBTree
from collective.taxonomy import PATH_SEPARATOR
from collective.taxonomy.controlpanel import TaxonomyEditFormAdapter
from collective.taxonomy.interfaces import ITaxonomy
from collective.taxonomy.interfaces import ITaxonomyForm
from plone.restapi.deserializer import json_body
from plone.restapi.interfaces import IFieldDeserializer
from plone.restapi.services import Service
from zExceptions import BadRequest
from zope.component import queryMultiAdapter
from zope.component import queryUtility
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse
from zope.schema import getFields
from zope.schema.interfaces import ValidationError


@implementer(IPublishTraverse)
class TaxonomyPatch(Service):
    """Patch a taxonomy"""

    taxonomy_id = None
    request = None

    def publishTraverse(self, request, name):  # noqa
        """Traverse"""
        self.request = request
        if name:
            self.taxonomy_id = name
        return self

    def generate_data_for_taxonomy(self, parsed_data, language, path=PATH_SEPARATOR):
        result = []
        for item in parsed_data:
            translations = item.get("translations", {})
            new_key = item["key"]
            title = item["title"]
            if language in translations:
                title = translations[language]
            new_path = f"{path}{title}"
            result.append(
                (
                    new_path,
                    new_key,
                )
            )
            subnodes = item.get("children", [])
            if subnodes:
                new_path = f"{new_path}{PATH_SEPARATOR}"
                result.extend(
                    self.generate_data_for_taxonomy(subnodes, language, new_path)
                )
        return result

    def reply(self):
        """Reply"""
        if not self.taxonomy_id:
            raise Exception("No taxonomy name provided")

        data = json_body(self.request)
        name = data.get("taxonomy")

        if name is None:
            raise Exception("No taxonomy name provided")

        languages = data.get("languages", [data.get("default_language", "en")])
        taxonomy = queryUtility(ITaxonomy, name=name)

        if taxonomy is None:
            raise Exception(f"No taxonomy found for this name: {name}")

        if "tree" in data:
            tree = data.get("tree", [])
            for language in languages:
                if language not in taxonomy.data:
                    taxonomy.data[language] = OOBTree()

            for language in taxonomy.data.keys():
                data_for_taxonomy = self.generate_data_for_taxonomy(tree, language)

                taxonomy.update(language, data_for_taxonomy, True)
        else:
            schema = ITaxonomyForm
            set_fields = TaxonomyEditFormAdapter(self.context, name)

            for field_name, field in getFields(schema).items():
                if field.readonly:
                    continue
                value = data.get(field_name, None)
                if value is None and field.required:
                    raise Exception(f"Field {field_name} is required")
                if value is not None:
                    deserializer = queryMultiAdapter(
                        (field, self.context, self.request), IFieldDeserializer
                    )

                    try:
                        # Make it sane
                        value = deserializer(value)
                        # Validate required etc
                        field.validate(value)
                    except ValueError as e:
                        raise BadRequest(
                            [{"message": str(e), "field": name, "error": e}]
                        )
                    except ValidationError as e:
                        raise BadRequest(
                            [{"message": e.doc(), "field": name, "error": e}]
                        )
                    else:
                        setattr(set_fields, field_name, value)

            del data["taxonomy"]
            taxonomy.updateBehavior(**data)

        return self.reply_no_content()

from collective.taxonomy.interfaces import ITaxonomyForm
from plone.restapi.serializer.controlpanels import get_jsonschema_for_controlpanel
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.services import Service
from plone.restapi.types.utils import create_form
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse


@implementer(IPublishTraverse)
class TaxonomyGetSchema(Service):
    def reply(self):
        form = create_form(self.context, self.request, ITaxonomyForm)
        json_schema = get_jsonschema_for_controlpanel(
            self,
            self.context,
            self.request,
            form=form,
        )
        # To-do: determine field defaults by serializing to volto schema
        return json_compatible(json_schema)

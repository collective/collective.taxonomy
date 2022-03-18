# -*- coding: utf-8 -*-
from collective.taxonomy.interfaces import ITaxonomy
from plone.restapi.services import Service
from collective.taxonomy.interfaces import ITaxonomyControlPanel
from collective.taxonomy.interfaces import ITaxonomyForm
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.serializer.controlpanels import ControlpanelSerializeToJson
from plone.restapi.serializer.controlpanels import get_jsonschema_for_controlpanel
from plone.restapi.types.utils import create_form
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.component import getUtilitiesFor
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse


@implementer(ISerializeToJson)
@adapter(ITaxonomyControlPanel)
class TaxonomyGetSchema(Service):
    def __call__(self, item=None):
        json = super().__call__()
        form = create_form(self.controlpanel, self.controlpanel.request, ITaxonomyForm)
        json_schema = get_jsonschema_for_controlpanel(
            self.controlpanel,
            self.controlpanel.context,
            self.controlpanel.request,
            form=form,
        )
        json["schema"] = json_schema

        utils = list(getUtilitiesFor(ITaxonomy))
        json["items"] = [
            getMultiAdapter((util, self.controlpanel.request), ISerializeToJson)(
                full_objects=True
            )
            for (_name, util) in utils
        ]
        return json

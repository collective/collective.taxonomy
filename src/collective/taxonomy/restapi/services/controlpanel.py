# -*- coding: utf-8 -*-
from collective.taxonomy.i18n import CollectiveTaxonomyMessageFactory as _
from collective.taxonomy.interfaces import IBrowserLayer
from collective.taxonomy.interfaces import ITaxonomyControlPanel
from collective.taxonomy.interfaces import ITaxonomyForm
from plone.protect.interfaces import IDisableCSRFProtection
from plone.restapi.controlpanels import RegistryConfigletPanel
from plone.restapi.deserializer import json_body
from plone.restapi.deserializer.controlpanels import FakeDXContext
from plone.restapi.interfaces import IDeserializeFromJson
from plone.restapi.interfaces import IFieldDeserializer
from plone.restapi.interfaces import IPloneRestapiLayer
from plone.restapi.interfaces import ISerializeToJson
from zExceptions import BadRequest
from zope.component import adapter
from zope.component import queryMultiAdapter
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import noLongerProvides
from zope.schema import getFields
from zope.schema.interfaces import ValidationError
from collective.taxonomy.utility import remove_taxonomy


@implementer(ITaxonomyControlPanel)
@adapter(Interface, IBrowserLayer)
class TaxonomyControlPanel(RegistryConfigletPanel):
    """Control Panel endpoint"""

    schema = Interface
    configlet_id = "taxonomies"
    configlet_category_id = "Products"
    title = _("Taxonomy settings")
    group = ""

    def add(self, names):
        schema = ITaxonomyForm
        data = json_body(self.request)
        # Validate schemata
        fake_context = FakeDXContext()
        form_data = {}
        errors = []
        for name, field in getFields(schema).items():
            if field.readonly:
                continue
            value = data.get(name, None)
            if value is None and field.required:
                errors.append(
                    {
                        "field": field.__name__,
                        "message": ("{} is a required field.".format(field.title),),
                    }
                )
                continue
            if value is not None:
                deserializer = queryMultiAdapter(
                    (field, fake_context, self.request), IFieldDeserializer
                )

                try:
                    # Make it sane
                    value = deserializer(value)
                    # Validate required etc
                    field.validate(value)
                except ValueError as e:
                    errors.append({"message": str(e), "field": name, "error": e})
                except ValidationError as e:
                    errors.append({"message": e.doc(), "field": name, "error": e})
                else:
                    form_data[name] = value

        if errors:
            raise BadRequest(errors)
        # Disable CSRF protection
        alsoProvides(self.request, IDisableCSRFProtection)

        if IPloneRestapiLayer.providedBy(self.request):
            noLongerProvides(self.request, IPloneRestapiLayer)

        add_view = queryMultiAdapter((self.context, self.request), name="taxonomy-add")
        add_view.add(form_data)
        return self.get(names=names)

    def get(self, names=[]):
        # name = names and [0] or None

        if IPloneRestapiLayer.providedBy(self.request):
            noLongerProvides(self.request, IPloneRestapiLayer)

        serializer = ISerializeToJson(self)()

        if "schema" in serializer:
            del serializer["schema"]
        return serializer

    def update(self, names):
        name = names[0]

        if IPloneRestapiLayer.providedBy(self.request):
            noLongerProvides(self.request, IPloneRestapiLayer)

        context = queryMultiAdapter(
            (self.context, self.request), name="dexterity-types"
        )
        context = context.publishTraverse(self.request, name)
        deserializer = IDeserializeFromJson(self)
        return deserializer(context)

    def delete(self, names):
        taxonomy = names[0]
        if not taxonomy:
            raise BadRequest(
                _(
                    "delete_taxonomies_no_taxonomies",
                    default=u"You need to provide a taxonomy to delete.",
                )
            )
        res = remove_taxonomy(name=taxonomy)
        if isinstance(res, dict):
            raise BadRequest(
                res.get(
                    "message",
                )
            )

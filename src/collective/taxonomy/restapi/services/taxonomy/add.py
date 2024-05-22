from collective.taxonomy.exportimport import TaxonomyImportExportAdapter
from collective.taxonomy.factory import registerTaxonomy
from collective.taxonomy.interfaces import ITaxonomyForm
from collective.taxonomy.restapi.utils import get_taxonomy_by_name
from plone.protect.interfaces import IDisableCSRFProtection
from plone.restapi.deserializer import json_body
from plone.restapi.deserializer.controlpanels import FakeDXContext
from plone.restapi.interfaces import IFieldDeserializer
from plone.restapi.interfaces import IPloneRestapiLayer
from plone.restapi.services import Service
from zExceptions import BadRequest
from zope.component import queryMultiAdapter
from zope.interface import alsoProvides
from zope.interface import noLongerProvides
from zope.schema import getFields
from zope.schema.interfaces import ValidationError


class TaxonomyPost(Service):
    """Creates a new taxonomy"""

    def reply(self):
        errors, form_data = self.validate_data()

        if errors:
            raise BadRequest(errors)

        # Disable CSRF protection
        alsoProvides(self.request, IDisableCSRFProtection)

        if IPloneRestapiLayer.providedBy(self.request):
            noLongerProvides(self.request, IPloneRestapiLayer)

        taxonomy = registerTaxonomy(
            self.context,
            name=form_data["taxonomy"],
            title=form_data["field_title"],
            description=form_data.get("field_description", ""),
            default_language=form_data["default_language"],
        )

        # Import
        adapter = TaxonomyImportExportAdapter(self.context)

        if "import_file" in form_data:
            if form_data["import_file"]:
                import_file = form_data["import_file"].data
                adapter.importDocument(taxonomy, import_file)
            del form_data["import_file"]

        del form_data["taxonomy"]
        if "import_file_purge" in form_data:
            del form_data["import_file_purge"]

        taxonomy.registerBehavior(**form_data)

        self.request.response.setStatus(201)
        return get_taxonomy_by_name(
            name=getattr(taxonomy, "name", ""), full_objects=False
        )

    def validate_data(self):
        schema = ITaxonomyForm
        data = json_body(self.request)
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
                        "message": (f"{field.title} is a required field.",),
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

        return errors, form_data

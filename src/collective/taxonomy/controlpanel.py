from collective.taxonomy.exportimport import TaxonomyImportExportAdapter
from collective.taxonomy.factory import registerTaxonomy
from collective.taxonomy.i18n import CollectiveTaxonomyMessageFactory as _
from collective.taxonomy.interfaces import ITaxonomy
from collective.taxonomy.interfaces import ITaxonomyForm
from collective.taxonomy.interfaces import ITaxonomySettings
from io import BytesIO
from plone import api
from plone.app.registry.browser import controlpanel
from plone.base.interfaces import IPloneSiteRoot
from plone.behavior.interfaces import IBehavior
from plone.memoize import view
from Products.Five.browser import BrowserView
from z3c.form import button
from z3c.form import field
from z3c.form import form
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.interfaces import HIDDEN_MODE
from zExceptions import NotFound
from zope.component import adapter
from zope.i18n.interfaces import ITranslationDomain
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory

import logging
import zipfile


logger = logging.getLogger("taxonomy.controlpanel")


class TaxonomySettingsControlPanelForm(controlpanel.RegistryEditForm):
    """A controlpanel for managing taxonomies"""

    id = "TaxonomySettings"
    label = _("Taxonomy settings")
    schema = ITaxonomySettings
    schema_prefix = "collective"
    description = _("Taxonomy settings")

    def updateFields(self):
        super().updateFields()
        self.fields["taxonomies"].widgetFactory = CheckBoxFieldWidget

    def updateActions(self):
        super(controlpanel.RegistryEditForm, self).updateActions()
        self.actions["add-taxonomy"].addClass("context")
        self.actions["edit-taxonomy"].addClass("context")
        self.actions["edit_data_taxonomy"].addClass("context")
        self.actions["delete-taxonomy"].addClass("context")
        self.actions["export"].addClass("context")

    @button.buttonAndHandler(
        _("label_add_taxonomy", default="Add"), name="add-taxonomy"
    )
    def handle_add_taxonomy_action(self, action):
        self.request.RESPONSE.redirect(self.context.portal_url() + "/@@taxonomy-add")

    @button.buttonAndHandler(
        _("label_edit_taxonomy", default="Edit"), name="edit-taxonomy"
    )
    def handle_edit_taxonomy_action(self, action):
        data, errors = self.extractData()
        if len(data.get("taxonomies", [])) > 0:
            self.request.RESPONSE.redirect(
                "{}/@@taxonomy-edit?form.widgets.taxonomy={}".format(
                    self.context.portal_url(), data.get("taxonomies")[0]
                )
            )
        else:
            api.portal.show_message(
                _("Please select one taxonomy."), request=self.request
            )

    @button.buttonAndHandler(
        _("label_edit_data_taxonomy", default="Edit taxonomy data"),
        name="edit_data_taxonomy",
    )
    def handle_edit_taxonomy_data_action(self, action):
        data, errors = self.extractData()
        if len(data.get("taxonomies", [])) > 0:
            self.request.RESPONSE.redirect(
                "{}/@@taxonomy-edit-data?taxonomy={}".format(
                    self.context.portal_url(), data.get("taxonomies")[0]
                )
            )
        else:
            api.portal.show_message(
                _("Please select one taxonomy."), request=self.request
            )

    @button.buttonAndHandler(
        _("label_delete_taxonomy", default="Delete taxonomy"), name="delete-taxonomy"
    )
    def handle_delete_taxonomy_action(self, action):
        data, errors = self.extractData()
        if len(data.get("taxonomies", [])) > 0:
            sm = self.context.getSiteManager()

            for item in data["taxonomies"]:
                utility = sm.queryUtility(ITaxonomy, name=item)
                utility.unregisterBehavior()

                sm.unregisterUtility(utility, ITaxonomy, name=item)
                sm.unregisterUtility(utility, IVocabularyFactory, name=item)
                sm.unregisterUtility(utility, ITranslationDomain, name=item)

                api.portal.show_message(_("Taxonomy deleted."), request=self.request)
        else:
            api.portal.show_message(
                _("Please select at least one taxonomy."), request=self.request
            )

        return self.request.RESPONSE.redirect(
            self.context.portal_url() + "/@@taxonomy-settings"
        )

    @button.buttonAndHandler(_("label_export", default="Export"), name="export")
    def handle_export_action(self, action):
        data, errors = self.extractData()
        taxonomies = data.get("taxonomies", [])

        if len(taxonomies) > 0:
            return self.request.RESPONSE.redirect(
                "{}/@@taxonomy-export?taxonomies={}".format(
                    self.context.portal_url(), ",".join(taxonomies)
                )
            )  # noqa


class TaxonomySettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = TaxonomySettingsControlPanelForm


class TaxonomyExport(BrowserView):
    def __call__(self, REQUEST):
        taxonomies = REQUEST.get("taxonomies")
        if not bool(taxonomies):
            raise NotFound()

        stream = BytesIO()
        z_file = zipfile.ZipFile(stream, "w", zipfile.ZIP_DEFLATED, True)
        sm = self.context.getSiteManager()
        adapter = TaxonomyImportExportAdapter(self.context)

        for taxonomy in taxonomies.split(","):
            utility = sm.queryUtility(ITaxonomy, name=taxonomy)
            if utility is None:
                continue
            result = adapter.exportDocument(utility)
            z_file.writestr("%s.xml" % taxonomy, result)

        z_file.close()
        self.request.RESPONSE.setHeader("Content-type", "application/x-zip-compressed")
        self.request.RESPONSE.setHeader(
            "Content-disposition", 'attachment; filename="taxonomy_export.zip"'
        )
        return stream.getvalue()


class TaxonomyAddForm(form.AddForm):
    fields = field.Fields(ITaxonomyForm)

    def updateWidgets(self):
        form.AddForm.updateWidgets(self)
        self.widgets["import_file_purge"].mode = HIDDEN_MODE

    def create(self, data):
        return data

    def add(self, data):
        # if "import_file" not in data:
        #     raise ValueError("Import file is not in form")
        taxonomy = registerTaxonomy(
            self.context,
            name=data["taxonomy"],
            title=data["field_title"],
            description=data.get("field_description", ""),
            default_language=data["default_language"],
        )

        # Import
        adapter = TaxonomyImportExportAdapter(self.context)

        if "import_file" in data:
            if data["import_file"]:
                import_file = data["import_file"].data
                adapter.importDocument(taxonomy, import_file)
            del data["import_file"]

        del data["taxonomy"]
        if "import_file_purge" in data:
            del data["import_file_purge"]

        taxonomy.registerBehavior(**data)
        api.portal.show_message(_("Taxonomy imported."), request=self.request)

        return self.request.RESPONSE.redirect(
            self.context.portal_url() + "/@@taxonomy-settings"
        )

    def nextURL(self):
        return self.context.portal_url() + "/@@taxonomy-settings"

    @button.buttonAndHandler(_("Add"), name="add")
    def handleAdd(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        obj = self.createAndAdd(data)
        if obj is not None:
            # mark only as finished if we get the new object
            self._finishedAdd = True

    @button.buttonAndHandler(_("Cancel"), name="cancel")
    def handleCancel(self, action):
        api.portal.show_message(_("Add cancelled"), request=self.request)
        self.request.response.redirect(
            f"{self.context.absolute_url()}/@@taxonomy-settings"
        )


class TaxonomyEditForm(form.EditForm):
    fields = field.Fields(ITaxonomyForm)

    def updateWidgets(self):
        self.fields["field_prefix"].showDefault = False
        form.EditForm.updateWidgets(self)
        self.widgets["taxonomy"].mode = HIDDEN_MODE

    @view.memoize
    def getContent(self):
        return TaxonomyEditFormAdapter(self.context)

    @button.buttonAndHandler(_("Save"), name="save")
    def handleApply(self, action):
        data, errors = self.extractData()

        if errors:
            self.status = self.formErrorsMessage
            return

        # This is sort of a hack; we need the import file purge setting to be
        # set before applying the file data.
        self.getContent().purge = data.pop("import_file_purge", False)
        self.applyChanges(data)

        sm = self.context.getSiteManager()
        utility = sm.queryUtility(ITaxonomy, name=data["taxonomy"])
        if utility is not None:
            del data["import_file"]
            del data["taxonomy"]
            utility.updateBehavior(**data)

            api.portal.show_message(_("Changes saved"), request=self.request)
        self.request.response.redirect(
            f"{self.context.absolute_url()}/@@taxonomy-settings"
        )

    @button.buttonAndHandler(_("Cancel"), name="cancel")
    def handleCancel(self, action):
        api.portal.show_message(_("Edit cancelled"), request=self.request)
        self.request.response.redirect(
            f"{self.context.absolute_url()}/@@taxonomy-settings"
        )


@adapter(IPloneSiteRoot)
@implementer(ITaxonomyForm)
class TaxonomyEditFormAdapter:
    purge = False

    def __init__(self, context, name=None):
        taxonomy = context.REQUEST.get("form.widgets.taxonomy") or name
        if taxonomy is None:
            return

        sm = context.getSiteManager()
        utility = sm.getUtility(ITaxonomy, name=taxonomy)
        generated_name = utility.getGeneratedName()

        self.__dict__["context"] = context
        self.__dict__["utility"] = utility
        self.__dict__["taxonomy"] = taxonomy
        self.__dict__["behavior"] = sm.queryUtility(IBehavior, name=generated_name)

    def __getattr__(self, attr):
        if "behavior" not in self.__dict__:
            return None

        if attr == "taxonomy":
            return self.__dict__["taxonomy"]

        return getattr(self.__dict__["behavior"], attr)

    def __setattr__(self, attr, value):
        if attr in ["taxonomy"]:
            return

        if attr == "purge":
            self.__dict__["purge"] = value
            return

        if attr == "taxonomy_fieldset":
            self.__dict__["utility"].fieldset = value
            return

        if attr == "field_prefix":
            self.__dict__["behavior"].removeIndex()
            setattr(self.__dict__["behavior"], attr, value or "")
            self.__dict__["behavior"].addIndex()
            self.__dict__["utility"].prefix = value
            return

        if attr == "import_file" and value is not None:
            import_file = value.data
            adapter = TaxonomyImportExportAdapter(self.__dict__["context"])
            purge = self.__dict__.get("purge", False)
            logger.info(
                "Importing document into '%s' (purge: %s)"
                % (self.__dict__["taxonomy"], str(purge).lower())
            )
            adapter.importDocument(self.utility, import_file, purge)
        else:
            if attr == "field_title":
                self.__dict__["utility"].title = value
            if attr == "field_description":
                self.__dict__["utility"].description = value
            if attr == "default_language":
                self.__dict__["utility"].default_language = value

            setattr(self.__dict__["behavior"], attr, value)

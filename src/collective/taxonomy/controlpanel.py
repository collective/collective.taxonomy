from plone.app.controlpanel.form import ControlPanelForm
from plone.app.form.widgets.multicheckboxwidget import MultiCheckBoxWidget \
    as BaseMultiCheckBoxWidget
from plone.behavior.interfaces import IBehavior

from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.statusmessages.interfaces import IStatusMessage

from zope.formlib import form as formlib
from zope.interface import implements
from zope.component import adapts
from zope.i18n.interfaces import ITranslationDomain
from zope.schema.interfaces import IVocabularyFactory

from z3c.form import form, field, button
from z3c.form.interfaces import HIDDEN_MODE

from .i18n import MessageFactory as _
from .interfaces import ITaxonomy, ITaxonomySettings, ITaxonomyForm
from .exportimport import TaxonomyImportExportAdapter

from rwproperty import getproperty, setproperty
from Acquisition import Implicit


class TaxonomySettingsControlPanelAdapter(SchemaAdapterBase):
    adapts(IPloneSiteRoot)
    implements(ITaxonomySettings)

    def __init__(self, context):
        super(TaxonomySettingsControlPanelAdapter, self).__init__(context)

    taxonomies = ProxyFieldProperty(ITaxonomySettings['taxonomies'])


class MultiCheckBoxWidget(BaseMultiCheckBoxWidget):

    def __init__(self, field, request):
        """Initialize the widget."""
        super(MultiCheckBoxWidget, self).__init__(field,
                                                  field.value_type.vocabulary,
                                                  request)


class TaxonomySettingsControlPanel(ControlPanelForm):
    form_fields = formlib.FormFields(ITaxonomySettings)
    form_fields['taxonomies'].custom_widget = MultiCheckBoxWidget

    label = _("Taxonomy settings")
    description = _("Taxonomy settings")
    form_name = _("Taxonomy settings")

    @formlib.action(_(u'label_add_taxonomy', default=u'Add taxonomy'),
                    name=u'add-taxonomy')
    def handle_add_taxonomy_action(self, action, data):
        self.context.REQUEST.RESPONSE.redirect(
            self.context.portal_url() + '/@@taxonomy-add'
        )

    @formlib.action(_(u'label_edit_taxonomy', default=u'Edit taxonomy'),
                    name=u'edit-taxonomy')
    def handle_edit_taxonomy_action(self, action, data):
        if len(data.get('taxonomies', [])) > 0:
            self.context.REQUEST.RESPONSE.redirect(
                self.context.portal_url() +
                '/@@taxonomy-edit?form.widgets.taxonomy=' +
                data.get('taxonomies')[0]
            )
        else:
            IStatusMessage(self.context.REQUEST).addStatusMessage(
                _(u"Please select one taxonomy."), type="info")

    @formlib.action(_(u'label_delete_taxonomy', default=u'Delete taxonomy'),
                    name=u'delete_taxonomy')
    def handle_delete_taxonomy_action(self, action, data):
        if len(data.get('taxonomies', [])) > 0:
            sm = self.context.getSiteManager()

            for item in data['taxonomies']:
                utility = sm.queryUtility(ITaxonomy, name=item)
                utility.unregisterBehavior()

                sm.unregisterUtility(utility, ITaxonomy, name=item)
                sm.unregisterUtility(utility, IVocabularyFactory, name=item)
                sm.unregisterUtility(utility, ITranslationDomain, name=item)

                IStatusMessage(self.context.REQUEST).addStatusMessage(
                    _(u"Taxonomy deleted."), type="info")
        else:
            IStatusMessage(self.context.REQUEST).addStatusMessage(
                _(u"Please select at least one taxonomy."), type="info")

        return self.context.REQUEST.RESPONSE.redirect(
            self.context.portal_url() + '/@@taxonomy-settings'
        )

    @formlib.action(_(u'label_export', default=u"Export"),
                    name=u'export')
    def handle_export_action(self, action, data):
        taxonomies = data.get('taxonomies', [])

        if len(taxonomies) > 0:
            adapter = TaxonomyImportExportAdapter(self.context)
            self.context.REQUEST.RESPONSE.setHeader('Content-type', 'text/xml')
            return adapter.exportDocument(taxonomies[0])

        return None


class TaxonomyAddForm(form.AddForm):
    fields = field.Fields(ITaxonomyForm)

    def updateWidgets(self):
        form.AddForm.updateWidgets(self)
        self.widgets['taxonomy'].mode = HIDDEN_MODE

    def create(self, data):
        return data

    def add(self, data):
        if 'import_file' not in data:
            raise ValueError("Import file is not in form")

        # Read import file
        import_file = data['import_file'].data
        del data['import_file']

        # This field is unused in add form.
        del data['taxonomy']

        # Import
        adapter = TaxonomyImportExportAdapter(self.context)
        taxonomy_name = adapter.importDocument(import_file)

        sm = self.context.getSiteManager()
        utility = sm.queryUtility(ITaxonomy,
                                  name=taxonomy_name)

        utility.registerBehavior(**data)

        IStatusMessage(self.context.REQUEST).addStatusMessage(
            _(u"Taxonomy imported."), type="info")

        return self.context.REQUEST.RESPONSE.redirect(
            self.context.portal_url() + '/@@taxonomy-settings'
        )

    def nextURL(self):
        return self.context.portal_url() + '/@@taxonomy-settings'

    @button.buttonAndHandler(_('Add'), name='add')
    def handleAdd(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        obj = self.createAndAdd(data)
        if obj is not None:
            # mark only as finished if we get the new object
            self._finishedAdd = True

    @button.buttonAndHandler(_(u'Cancel'), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(_(u"Add cancelled"),
                                                      "info")
        self.request.response.redirect(self.context.absolute_url() +
                                       '/@@taxonomy-settings')


class TaxonomyEditForm(form.EditForm):
    fields = field.Fields(ITaxonomyForm)

    def updateWidgets(self):
        form.EditForm.updateWidgets(self)
        self.widgets['taxonomy'].mode = HIDDEN_MODE

    def getContent(self):
        return TaxonomyEditFormAdapter(self.context)

    @button.buttonAndHandler(_(u'Save'), name='save')
    def handleApply(self, action):
        data, errors = self.extractData()

        if errors:
            self.status = self.formErrorsMessage
            return

        self.applyChanges(data)

        sm = self.context.getSiteManager()
        utility = sm.queryUtility(ITaxonomy,
                                  name=data['taxonomy'])
        if utility is not None:
            del data['import_file']
            del data['taxonomy']
            utility.updateBehavior(**data)

        IStatusMessage(self.request).addStatusMessage(_(u"Changes saved"),
                                                      "info")
        self.request.response.redirect(self.context.absolute_url() +
                                       '/@@taxonomy-settings')

    @button.buttonAndHandler(_(u'Cancel'), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(_(u"Edit cancelled"),
                                                      "info")
        self.request.response.redirect(self.context.absolute_url() +
                                       '/@@taxonomy-settings')


class TaxonomyEditFormAdapter(Implicit):
    adapts(IPloneSiteRoot)
    implements(ITaxonomyForm)

    def __init__(self, context):
        self.__parent__ = context

        if context.REQUEST.get('form.widgets.taxonomy') is None:
            return

        taxonomy = context.REQUEST.get('form.widgets.taxonomy')

        sm = context.getSiteManager()
        utility = sm.queryUtility(ITaxonomy,
                                  name=taxonomy)

        generated_name = utility.getGeneratedName()

        self.context = context
        self.taxonomy = context.REQUEST.get('taxonomy')
        self.behavior = sm.queryUtility(IBehavior,
                                        name=generated_name)

    """field_title"""
    @setproperty
    def field_title(self, value):
        self.behavior.field_title = value

    @getproperty
    def field_title(self):
        return self.behavior.field_title

    """field_description"""
    @setproperty
    def field_description(self, value):
        self.behavior.field_description = value

    @getproperty
    def field_description(self):
        return self.behavior.field_description

    """import_file"""
    @setproperty
    def import_file(self, value):
        if value:
            import_file = value.data
            adapter = TaxonomyImportExportAdapter(self.__dict__['context'])
            adapter.importDocument(import_file)

    @getproperty
    def import_file(self):
        return self.behavior.import_file

    """is_required"""
    @setproperty
    def is_required(self, value):
        self.behavior.is_required = value

    @getproperty
    def field_description(self):
        return self.behavior.is_required

    """group"""
    @setproperty
    def group(self, value):
        self.behavior.group = value

    @getproperty
    def group(self):
        return self.behavior.group

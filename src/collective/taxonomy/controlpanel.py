from plone.app.controlpanel.form import ControlPanelForm
from plone.app.form.widgets.multicheckboxwidget import MultiCheckBoxWidget \
    as BaseMultiCheckBoxWidget

from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.Five import BrowserView

from zope import schema
from zope.interface import Interface
from zope.formlib import form as formlib
from zope.interface import implements
from zope.component import adapts
from zope.i18n.interfaces import ITranslationDomain
from zope.schema.interfaces import IVocabularyFactory

from z3c.form import form, field
from z3c.form.interfaces import HIDDEN_MODE

from i18n import MessageFactory as _
from interfaces import ITaxonomy


class ITaxonomySettings(Interface):
    """ Schema for controlpanel settings """

    taxonomies = schema.List(title=_(u"Taxonomies"),
                             value_type=schema.Choice(
                                 description=_(u"help_taxonomies",
                                               default=u"Select the taxnomies"
                                               "you desire to modify"),
                                 required=False,
                                 vocabulary='collective.taxonomy.taxonomies',
                             ),
                             default=[],)


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

    @formlib.action(_(u'label_add_behavior', default=u'Add behavior'),
                    name=u'add-behavior')
    def handle_add_behavior_action(self, action, data):
        if len(data.get('taxonomies', [])) > 0:
            taxonomy = data['taxonomies'][0]
            self.context.REQUEST.RESPONSE.redirect(
                self.context.portal_url() + '/@@taxonomy-add-behavior' +
                '?taxonomy=' + taxonomy
            )

    @formlib.action(_(u'label_del_behavior', default=u'Delete behavior'),
                    name=u'del-behavior')
    def handle_del_behavior_action(self, action, data):
        if len(data.get('taxonomies', [])) > 0:
            taxonomy = data['taxonomies'][0]
            self.context.REQUEST.RESPONSE.redirect(
                self.context.portal_url() + '/@@taxonomy-del-behavior' +
                '?taxonomy=' + taxonomy
            )

    @formlib.action(_(u'label_delete', default=u'Delete'),
                    name=u'delete')
    def handle_delete_action(self, action, data):
        if len(data.get('taxonomies', [])) > 0:
            sm = self.context.getSiteManager()

            for item in data['taxonomies']:
                utility = sm.queryUtility(ITaxonomy, name=item)
                utility.unregisterBehavior()

                sm.unregisterUtility(utility, ITaxonomy, name=item)
                sm.unregisterUtility(utility, IVocabularyFactory, name=item)
                sm.unregisterUtility(utility, ITranslationDomain, name=item)


class ITaxonomyAddBehavior(Interface):
    # Regular fields
    field_name = schema.TextLine(title=_(u"Field name"),
                                 required=True)

    field_title = schema.TextLine(title=_(u"Field title"),
                                  required=True)

    field_description = schema.TextLine(title=_(u"Field description"),
                                        required=False)

    is_required = schema.Bool(title=_(u"Is required?"),
                              required=True)

    # Hidden fields
    taxonomy = schema.TextLine(title=_(u"Taxonomy name"))


class TaxonomyAddBehavior(form.AddForm):
    fields = field.Fields(ITaxonomyAddBehavior)

    def updateWidgets(self):
        form.AddForm.updateWidgets(self)
        context = self.context
        widgets = self.widgets
        widgets['taxonomy'].mode = HIDDEN_MODE
        widgets['taxonomy'].value = context.REQUEST.get('taxonomy', '')

    def create(self, data):
        return data

    def add(self, data):
        if 'taxonomy' not in data:
            raise Exception("Taxonomy name is not in form")

        sm = self.context.getSiteManager()
        utility = sm.queryUtility(ITaxonomy,
                                  name=data['taxonomy'])
        utility.registerBehavior(data['field_name'],
                                 data['field_title'],
                                 data['field_description'],
                                 data['is_required'])

    def nextURL(self):
        return self.context.portal_url() + '/@@taxonomy-settings'


class TaxonomyDelBehavior(BrowserView):
    def __call__(self):
        if 'taxonomy' not in self.context.REQUEST:
            raise Exception("Taxonomy name is not provided")

        taxonomy = self.context.REQUEST.get('taxonomy', '')

        sm = self.context.getSiteManager()
        utility = sm.queryUtility(ITaxonomy, name=taxonomy)
        utility.unregisterBehavior()

        return self.context.REQUEST.RESPONSE.redirect(
            self.context.portal_url() + '/@@taxonomy-settings'
        )

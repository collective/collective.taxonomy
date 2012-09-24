from zope import schema
from zope.interface import Interface
from zope.formlib import form
from zope.interface import implements
from zope.component import adapts, queryUtility
from zope.schema.interfaces import IVocabularyFactory

from i18n import MessageFactory as _
from plone.app.controlpanel.form import ControlPanelForm

from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFDefault.formlib.schema import SchemaAdapterBase

from Products.CMFPlone.interfaces import IPloneSiteRoot

from plone.app.form.widgets.multicheckboxwidget import MultiCheckBoxWidget \
    as BaseMultiCheckBoxWidget
from plone.dexterity.interfaces import IDexterityFTI

from interfaces import ITaxonomy


class ITaxonomySettings(Interface):
    """Global akismet settings. This describes records stored in the
    configuration registry and obtainable via plone.registry.
    """

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
    form_fields = form.FormFields(ITaxonomySettings)
    form_fields['taxonomies'].custom_widget = MultiCheckBoxWidget

    label = _("Taxonomy settings")
    description = _("Taxonomy settings")
    form_name = _("Taxonomy settings")

    @form.action(_(u'label_delete', default=u'Delete'), name=u'delete')
    def handle_delete_action(self, action, data):
        sm = self.context.getSiteManager()

        for item in data['taxonomies']:
            utility = sm.queryUtility(ITaxonomy, name=item)
            utility.unregisterBehavior()

            sm.unregisterUtility(utility, ITaxonomy, name=item)
            sm.unregisterUtility(utility, IVocabularyFactory, name=item)

            behavior_name = 'collective.taxonomy.generated.' + \
                            item.split('.')[-1]

            for (name, fti) in sm.getUtilitiesFor(IDexterityFTI):
                if behavior_name in fti.behaviors:
                    fti.behaviors = [behavior for behavior in
                                     fti.behaviors
                                     if behavior != behavior_name]

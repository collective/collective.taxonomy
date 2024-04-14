from collective.taxonomy.i18n import CollectiveTaxonomyMessageFactory as _
from collective.taxonomy.interfaces import IBrowserLayer
from collective.taxonomy.interfaces import ITaxonomyControlPanel
from plone.restapi.controlpanels import RegistryConfigletPanel
from plone.restapi.interfaces import IPloneRestapiLayer
from plone.restapi.interfaces import ISerializeToJson
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import noLongerProvides


@implementer(ITaxonomyControlPanel)
@adapter(Interface, IBrowserLayer)
class TaxonomyControlPanel(RegistryConfigletPanel):
    """Control Panel endpoint"""

    schema = Interface
    configlet_id = "taxonomies"
    configlet_category_id = "Products"
    title = _("Taxonomy settings")
    group = ""

    def get(self):
        if IPloneRestapiLayer.providedBy(self.request):
            noLongerProvides(self.request, IPloneRestapiLayer)

        serializer = ISerializeToJson(self)()
        if "schema" in serializer:
            del serializer["schema"]
        return serializer

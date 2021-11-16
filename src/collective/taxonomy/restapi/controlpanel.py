""" Control Panel RestAPI endpoint
"""
from collective.taxonomy.i18n import CollectiveTaxonomyMessageFactory as _
from collective.taxonomy.interfaces import IBrowserLayer
from plone.restapi.controlpanels import RegistryConfigletPanel
from zope.component import adapter
from zope.interface import Interface


@adapter(Interface, IBrowserLayer)
class TaxonomyControlPanel(RegistryConfigletPanel):
    """Control Panel endpoint"""

    schema = Interface
    configlet_id = "taxonomies"
    configlet_category_id = "Products"
    title = _("Taxonomy settings")
    group = ""

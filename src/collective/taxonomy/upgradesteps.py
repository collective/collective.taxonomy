from .interfaces import ITaxonomy
from logging import getLogger
from plone import api
from plone.behavior.interfaces import IBehavior
from Products.CMFCore.Expression import Expression


log = getLogger("collective.taxonomy:upgrades")


def reactivateSearchable(tool):
    """ """
    tool = tool.aq_parent
    sm = tool.getSiteManager()
    utilities = sm.getUtilitiesFor(IBehavior)
    for utility_name, utility in utilities:
        if utility_name.startswith("collective.taxonomy.generated."):
            utility.deactivateSearchable()
            utility.activateSearchable()
            log.info("Reactivated searchable for " + utility_name)


def import_registry(tool):
    tool.runImportStepFromProfile(
        "profile-collective.taxonomy:default",
        "plone.app.registry",
        run_dependencies=False,
        purge_old=False,
    )


def fix_metadata(tool):
    tool = tool.aq_parent
    sm = tool.getSiteManager()
    utilities = sm.getUtilitiesFor(ITaxonomy)
    for utility_name, utility in utilities:
        utility._fixup()
        for lang, data in utility.data.items():
            version = data.pop("#VERSION", None)
            if version is not None:
                utility.version[lang] = version

            count = data.pop("#COUNT", None)
            if count is not None:
                utility.count[lang] = count

            order = data.pop("#ORDER", None)
            if order is not None:
                utility.order[lang] = order


def update_configlet_properties(tool):
    tool.runImportStepFromProfile(
        "profile-collective.taxonomy:default",
        "rolemap",
    )
    pc = api.portal.get_tool("portal_controlpanel")
    for action in pc._actions:
        if action.id == "taxonomies":
            action.permissions = ("Manage taxonomies",)


def update_configlet_icon(tool):
    pc = api.portal.get_tool("portal_controlpanel")
    for action in pc._actions:
        if action.id == "taxonomies":
            action.icon_expr = Expression("string:puzzle")

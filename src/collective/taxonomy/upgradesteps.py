from zope.component import getUtilitiesFor

from logging import getLogger

from plone.behavior.interfaces import IBehavior

log = getLogger('collective.taxonomy:upgrades')


def reactivateSearchable(tool):
    """ """
    tool = tool.aq_parent
    sm = tool.getSiteManager()
    utilities = sm.getUtilitiesFor(IBehavior)
    for (utility_name, utility) in utilities:
        if utility_name.startswith('collective.taxonomy.generated.'):
            utility.deactivateSearchable()
            utility.activateSearchable()
            log.info('Reactivated searchable for ' + utility_name)

from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
from plone.testing import zope

import collective.taxonomy


class CollectiveTaxonomyLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity)

        self.loadZCML(package=collective.taxonomy)
        self.loadZCML("testing.zcml", package=collective.taxonomy)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.taxonomy:examples")


COLLECTIVE_TAXONOMY_FIXTURE = CollectiveTaxonomyLayer()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_TAXONOMY_FIXTURE,), name="TaxonomyFixture:Integration"
)

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_TAXONOMY_FIXTURE, zope.WSGI_SERVER_FIXTURE),
    name="TaxonomyFixture:Functional",
)

ROBOT_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_TAXONOMY_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="CollectiveTaxonomy:Acceptance",
)


class CollectiveTaxonomyE2ELayer(PloneSandboxLayer):
    """Fixture for the Cypress end-to-end test in resources/.

    Same as the robot fixture, plus the default workflow: the e2e scenario
    publishes the content it creates, and plone.app.testing switches all
    workflows off. Run it with
    ``bin/robot-server collective.taxonomy.testing.E2E_TESTING``.
    """

    defaultBases = (COLLECTIVE_TAXONOMY_FIXTURE,)

    def setUpPloneSite(self, portal):
        portal.portal_workflow.setDefaultChain("simple_publication_workflow")


COLLECTIVE_TAXONOMY_E2E_FIXTURE = CollectiveTaxonomyE2ELayer()

E2E_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_TAXONOMY_E2E_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="CollectiveTaxonomy:E2E",
)

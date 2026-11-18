from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing.zope import WSGI_SERVER_FIXTURE

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
    bases=(COLLECTIVE_TAXONOMY_FIXTURE, WSGI_SERVER_FIXTURE),
    name="TaxonomyFixture:Functional",
)


class CollectiveTaxonomyAcceptanceLayer(PloneSandboxLayer):
    """Fixture for the Playwright acceptance tests in resources/acceptance.

    The example taxonomy, plus the default workflow: the acceptance tests
    publish the content they create, and plone.app.testing switches all
    workflows off. Run it with ``make acceptance-backend-start``.
    """

    defaultBases = (COLLECTIVE_TAXONOMY_FIXTURE,)

    def setUpPloneSite(self, portal):
        portal.portal_workflow.setDefaultChain("simple_publication_workflow")


ACCEPTANCE_FIXTURE = CollectiveTaxonomyAcceptanceLayer()

ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        ACCEPTANCE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        WSGI_SERVER_FIXTURE,
    ),
    name="CollectiveTaxonomy:Acceptance",
)

# Kept for test code written against 4.1.1 and earlier.
ROBOT_TESTING = ACCEPTANCE_TESTING
E2E_TESTING = ACCEPTANCE_TESTING

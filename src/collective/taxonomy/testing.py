from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting


class Fixture(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        import collective.taxonomy
        self.loadZCML(package=collective.taxonomy)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'collective.taxonomy:default')

FIXTURE = Fixture()
INTEGRATION_TESTING = IntegrationTesting(bases=(FIXTURE,), name="TaxonomyFixture:Integration")

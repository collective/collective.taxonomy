# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.testing import z2


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        super(Fixture, self).setUpZope(
            app, configurationContext)
        z2.installProduct(app, 'Products.DateRecurringIndex')
        import collective.taxonomy
        self.loadZCML(package=collective.taxonomy,
                      name='testing.zcml')

    def tearDownZope(self, app):
        # Uninstall products installed above
        z2.uninstallProduct(app, 'Products.DateRecurringIndex')

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'collective.taxonomy:default')
        self.applyProfile(portal, 'collective.taxonomy:examples')
        setRoles(portal, TEST_USER_ID, ['Manager'])


FIXTURE = Fixture()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name="TaxonomyFixture:Integration")

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name="TaxonomyFixture:Functional")

ROBOT_TESTING = FunctionalTesting(
    bases=(FIXTURE,
           REMOTE_LIBRARY_BUNDLE_FIXTURE,
           z2.ZSERVER_FIXTURE),
    name="CollectiveTaxonomy:Acceptance"
)

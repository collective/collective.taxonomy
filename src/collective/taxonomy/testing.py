# from StringIO import StringIO
# from plone.app.testing import IntegrationTesting
# from plone.app.testing import PLONE_FIXTURE
# from plone.app.testing import PloneSandboxLayer
# from plone.app.testing import TEST_USER_ID
# from plone.app.testing import setRoles
# from zope.configuration import xmlconfig
# import logging


# class Layer(PloneSandboxLayer):

#     defaultBases = (PLONE_FIXTURE,)

#     def __init__(self, *args, **kwargs):
#         super(Layer, self).__init__(*args, **kwargs)
#         self.log = None
#         self.log_handler = None

#     def setUpZope(self, app, configurationContext):
#         import collective.taxonomy
#         xmlconfig.file('configure.zcml', collective.taxonomy,
#                        context=configurationContext)
#         import collective.taxonomy.tests
#         xmlconfig.file('configure.zcml',
#                        collective.taxonomy.tests,
#                        context=configurationContext)

#     def setUpPloneSite(self, portal):
#         setRoles(portal, TEST_USER_ID, ['Manager'])

#     def testSetUp(self):
#         super(Layer, self).testSetUp()
#         self.log = StringIO()
#         self.log_handler = logging.StreamHandler(self.log)
#         logging.root.addHandler(self.log_handler)
#         self['read_log'] = self.read_log

#     def testTearDown(self):
#         super(Layer, self).testTearDown()
#         logging.root.removeHandler(self.log_handler)

#     def read_log(self):
#         self.log.seek(0)
#         return self.log.read().strip()


# TAXONOMY_FIXTURE = Layer()
# TAXONOMY_INTEGRATION_TESTING = IntegrationTesting(
#     bases=(TAXONOMY_FIXTURE,),
#     name="collective.taxonomy:Integration")


from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import applyProfile


class Fixture(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        import collective.taxonomy
        self.loadZCML(package=collective.taxonomy)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'collective.taxonomy:default')



FIXTURE = Fixture()

INTEGRATION_TESTING = IntegrationTesting(bases=(FIXTURE,), name="TaxonomyFixture:Integration")

# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneWithPackageLayer
from plone.testing import z2
from plone.restapi.testing import PloneRestApiDXLayer

import collective.taxonomy


FIXTURE = PloneWithPackageLayer(
    name="TAXONOMY_FIXTURE",
    zcml_package=collective.taxonomy,
    zcml_filename="testing.zcml",
    gs_profile_id="collective.taxonomy:examples",
    additional_z2_products=["Products.DateRecurringIndex"],
)

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name="TaxonomyFixture:Integration"
)

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name="TaxonomyFixture:Functional"
)

ROBOT_TESTING = FunctionalTesting(
    bases=(FIXTURE, REMOTE_LIBRARY_BUNDLE_FIXTURE, z2.ZSERVER_FIXTURE),
    name="CollectiveTaxonomy:Acceptance",
)


class CollectiveTaxonomyRestApiLayer(PloneWithPackageLayer, PloneRestApiDXLayer):
    """ """


API_FIXTURE = CollectiveTaxonomyRestApiLayer(
    name="TAXONOMY_API_FIXTURE",
    zcml_package=collective.taxonomy,
    zcml_filename="testing.zcml",
    gs_profile_id="collective.taxonomy:examples",
    additional_z2_products=(["Products.DateRecurringIndex", "plone.restapi"]),
)
API_INTEGRATION_TESTING = IntegrationTesting(
    bases=(API_FIXTURE,),
    name="CollectiveTaxonomyRestApiLayer:Integration",
)

API_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(API_FIXTURE, z2.ZSERVER_FIXTURE),
    name="CollectiveTaxonomyRestApiLayer:Functional",
)

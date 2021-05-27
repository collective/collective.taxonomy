# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneWithPackageLayer
from plone.testing import z2
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

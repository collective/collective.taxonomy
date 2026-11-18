from collective.taxonomy.interfaces import ITaxonomy
from collective.taxonomy.testing import FUNCTIONAL_TESTING
from collective.taxonomy.testing import INTEGRATION_TESTING
from pytest_plone import fixtures_factory
from tests import TAXONOMY_NAME
from zope.component import queryUtility

import pytest


pytest_plugins = ["pytest_plone"]


globals().update(
    fixtures_factory((
        (FUNCTIONAL_TESTING, "functional"),
        (INTEGRATION_TESTING, "integration"),
    ))
)


@pytest.fixture
def taxonomy(portal) -> ITaxonomy:
    """The example taxonomy registered by the test layer."""
    utility = queryUtility(ITaxonomy, name=TAXONOMY_NAME)
    assert utility is not None
    return utility

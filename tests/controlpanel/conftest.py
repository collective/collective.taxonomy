from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.testing.zope import Browser

import pytest
import transaction


@pytest.fixture
def portal(functional_portal):
    """The functional portal, with its state committed for HTTP requests."""
    transaction.commit()
    return functional_portal


@pytest.fixture
def browser(portal, functional_app) -> Browser:
    """A test browser logged in as the site owner."""
    browser = Browser(functional_app)
    browser.handleErrors = False
    browser.addHeader("Authorization", f"Basic {SITE_OWNER_NAME}:{SITE_OWNER_PASSWORD}")
    return browser

"""Setup tests for this package."""

from collective.taxonomy.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.base.utils import get_installer

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.taxonomy is properly installed."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_product_installed(self):
        """Test if collective.taxonomy is installed."""
        self.assertTrue(self.installer.is_product_installed("collective.taxonomy"))

    def test_browserlayer(self):
        """Test that IBrowserLayer is registered."""
        from collective.taxonomy.interfaces import IBrowserLayer
        from plone.browserlayer import utils

        self.assertIn(IBrowserLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("collective.taxonomy")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.taxonomy is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed("collective.taxonomy"))

    def test_browserlayer_removed(self):
        """Test that IBrowserLayer is removed."""
        from collective.taxonomy.interfaces import IBrowserLayer
        from plone.browserlayer import utils

        self.assertNotIn(IBrowserLayer, utils.registered_layers())

    def test_persistent_utility_uninstalled(self):
        from collective.taxonomy.interfaces import ITaxonomy

        sm = self.portal.getSiteManager()
        utilities = sm.getUtilitiesFor(ITaxonomy)
        self.assertTrue(len(list(utilities)) == 0)

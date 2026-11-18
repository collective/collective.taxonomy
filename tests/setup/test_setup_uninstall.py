from collective.taxonomy import PACKAGE_NAME
from collective.taxonomy.interfaces import ITaxonomy
from plone import api

import pytest


class TestSetupUninstall:
    @pytest.fixture(autouse=True)
    def _setup(self, portal, installer):
        self.portal = portal
        with api.env.adopt_roles(["Manager"]):
            installer.uninstall_product(PACKAGE_NAME)

    def test_addon_uninstalled(self, installer):
        """collective.taxonomy is cleanly uninstalled."""
        assert installer.is_product_installed(PACKAGE_NAME) is False

    def test_browserlayer_not_registered(self, browser_layers):
        """IBrowserLayer is removed."""
        from collective.taxonomy.interfaces import IBrowserLayer

        assert IBrowserLayer not in browser_layers

    def test_persistent_utility_uninstalled(self):
        """The persistent taxonomy utilities are removed."""
        sm = self.portal.getSiteManager()
        assert list(sm.getUtilitiesFor(ITaxonomy)) == []

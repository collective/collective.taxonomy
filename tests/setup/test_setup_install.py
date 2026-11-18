from collective.taxonomy import PACKAGE_NAME
from plone import api


class TestSetupInstall:
    def test_addon_installed(self, portal):
        """collective.taxonomy is installed, with no upgrade pending."""
        assert api.addon.get(PACKAGE_NAME).flags == ["installed"]

    def test_browserlayer(self, browser_layers):
        """IBrowserLayer is registered."""
        from collective.taxonomy.interfaces import IBrowserLayer

        assert IBrowserLayer in browser_layers

    def test_latest_version(self, profile_last_version):
        """The default profile is at its latest version."""
        assert profile_last_version(f"{PACKAGE_NAME}:default") == "2001"

from collective.taxonomy.testing import FUNCTIONAL_TESTING
from plone import api
from plone.app.testing import applyProfile
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing.interfaces import SITE_OWNER_NAME
from plone.app.testing.interfaces import SITE_OWNER_PASSWORD
from plone.testing.z2 import Browser
from transaction import commit

import unittest


class TestControlPanel(unittest.TestCase):
    """Test JSON views."""

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.portal.portal_workflow.setDefaultChain("simple_publication_workflow")
        applyProfile(self.portal, "plone.app.contenttypes:plone-content")
        self.document = api.content.create(
            container=self.portal, type="Document", title="Doc"
        )
        self.browser = Browser(self.layer["app"])
        self.browser.handleErrors = False
        self.browser.addHeader(
            "Authorization",
            f"Basic {SITE_OWNER_NAME}:{SITE_OWNER_PASSWORD}",
        )
        commit()

    def test_configlet_permission(self):
        permission = "Manage taxonomies"
        roles = self.portal.rolesOfPermission(permission)
        roles = [r["name"] for r in roles if r["selected"]]
        expected = ["Manager", "Site Administrator"]
        self.assertListEqual(roles, expected)

    def test_add_vocabulary(self):
        self.browser.open(self.portal.absolute_url() + "/@@taxonomy-settings")
        self.assertIn('id="TaxonomySettings"', self.browser.contents)
        self.browser.getControl("Add").click()
        self.browser.getControl(name="form.widgets.taxonomy").value = "foobar"
        self.browser.getControl(name="form.widgets.field_title").value = (
            "Foo Bar Vocabulary"
        )
        self.browser.getControl(name="form.widgets.default_language:list").value = [
            "en"
        ]
        self.browser.getForm(id="form").submit("Add")
        self.assertIn(
            '<span class="label">Foo Bar Vocabulary</span>', self.browser.contents
        )

    def test_edit_vocabulary(self):
        self.browser.open(self.portal.absolute_url() + "/@@taxonomy-settings")
        self.assertIn('id="TaxonomySettings"', self.browser.contents)
        taxonomies = self.browser.getControl(name="form.widgets.taxonomies:list")
        taxonomies.controls[0].selected = True
        self.browser.getForm(id="TaxonomySettings").submit(
            name="form.buttons.edit-taxonomy"
        )
        self.browser.getControl(name="form.widgets.field_title").value = (
            "Edited Test Vocabulary"
        )
        self.browser.getForm(id="form").submit("Save")
        self.assertIn(
            '<span class="label">Edited Test Vocabulary</span>', self.browser.contents
        )

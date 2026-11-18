SETTINGS_FORM_ID = 'id="TaxonomySettings"'


def test_configlet_permission(portal):
    roles = portal.rolesOfPermission("Manage taxonomies")
    assert [r["name"] for r in roles if r["selected"]] == [
        "Manager",
        "Site Administrator",
    ]


class TestControlPanelForm:
    def test_add_vocabulary(self, portal, browser):
        browser.open(f"{portal.absolute_url()}/@@taxonomy-settings")
        assert SETTINGS_FORM_ID in browser.contents
        browser.getControl("Add").click()
        browser.getControl(name="form.widgets.taxonomy").value = "foobar"
        browser.getControl(name="form.widgets.field_title").value = "Foo Bar Vocabulary"
        browser.getControl(name="form.widgets.default_language:list").value = ["en"]
        browser.getForm(id="form").submit("Add")
        assert '<span class="label">Foo Bar Vocabulary</span>' in browser.contents

    def test_edit_vocabulary(self, portal, browser):
        browser.open(f"{portal.absolute_url()}/@@taxonomy-settings")
        assert SETTINGS_FORM_ID in browser.contents
        taxonomies = browser.getControl(name="form.widgets.taxonomies:list")
        taxonomies.controls[0].selected = True
        browser.getForm(id="TaxonomySettings").submit(name="form.buttons.edit-taxonomy")
        browser.getControl(
            name="form.widgets.field_title"
        ).value = "Edited Test Vocabulary"
        browser.getForm(id="form").submit("Save")
        assert '<span class="label">Edited Test Vocabulary</span>' in browser.contents

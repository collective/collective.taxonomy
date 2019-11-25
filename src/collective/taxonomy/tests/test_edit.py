# -*- coding: utf-8 -*-
from collective.taxonomy.testing import FUNCTIONAL_TESTING
from plone import api
from plone.app.testing.interfaces import SITE_OWNER_NAME
from plone.app.testing.interfaces import SITE_OWNER_PASSWORD
import unittest
from transaction import commit
from plone.testing.z2 import Browser


class TestEditing(unittest.TestCase):
    """Test Taxonomy Editing"""

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.document = api.content.create(
            container=self.portal, type='Document', title='Doc')
        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization', 'Basic {0}:{1}'.format(
                SITE_OWNER_NAME, SITE_OWNER_PASSWORD))
        commit()

    def test_edit_doc(self):
        self.browser.open(self.portal.absolute_url() + '/doc/edit')

        # check for editing buttons
        self.assertIn(
            'name="form.widgets.test.taxonomy_test.from"',
            self.browser.contents)
        self.assertIn(
            'name="form.widgets.test.taxonomy_test.to"',
            self.browser.contents)
        self.assertIn('name="from2toButton"', self.browser.contents)
        self.assertIn('name="to2fromButton"', self.browser.contents)
        self.assertIn('name="moveUpButton"', self.browser.contents)
        self.assertIn('name="moveDownButton"', self.browser.contents)

        tax_from = self.browser.getControl(
            name='form.widgets.test.taxonomy_test.from')
        self.assertEqual(tax_from.options, ['1', '2', '3', '5'])

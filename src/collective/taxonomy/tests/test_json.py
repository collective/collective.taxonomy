# -*- coding: utf8 -*-
import unittest

from plone.app.testing.helpers import login
from plone.app.testing.interfaces import TEST_USER_NAME

from collective.taxonomy.testing import INTEGRATION_TESTING


class TestJson(unittest.TestCase):

    """Test JSON views."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        super(TestJson, self).setUp()
        self.portal = self.layer['portal']

    def test_generate_json(self):
        login(self.portal, TEST_USER_NAME)
        import_json_view = self.portal.restrictedTraverse("@@taxonomy-import")
        input_data = [
            {
                'key': 'animals',
                'translations': {'fr': u'Animaux', 'en': u'Animals'},
                'subnodes': [],
            },
            {
                'key': 'plants',
                'translations': {'fr': u'Végétaux', 'en': u'Plants'},
                'subnodes': [],
            },
        ]
        output = import_json_view.generate_data_for_taxonomy(input_data, 'fr')
        self.assertEqual(
            output,
            [(u'/Animaux', 'animals'), (u'/Végétaux', 'plants')])

        input_data[0]['subnodes'] = [
            {
                'key': 'birds',
                'translations': {'fr': u'Oiseaux', 'en': u'Birds'},
                'subnodes': [
                    {
                        'key': 'eagles',
                        'translations': {'fr': u'Aigles', 'en': u'Eagles'},
                        'subnodes': []
                    },
                    {
                        'key': 'penguins',
                        'translations': {'fr': u'Manchots', 'en': u'Penguins'},
                        'subnodes': []
                    },
                ],
            },
            {
                'key': 'mammals',
                'translations': {'fr': u'Mammifères', 'en': u'Mammals'},
                'subnodes': [
                    {
                        'key': 'cows',
                        'translations': {'fr': u'Vaches', 'en': u'Cows'},
                        'subnodes': []
                    },
                    {
                        'key': 'lions',
                        'translations': {'fr': u'Lions', 'en': u'Lions'},
                        'subnodes': []
                    },
                ],
            },
            {
                'key': 'reptiles',
                'translations': {'fr': u'Reptiles', 'en': u'Reptiles'},
                'subnodes': [
                    {
                        'key': 'pythons',
                        'translations': {'fr': u'Pythons', 'en': u'Pythons'},
                        'subnodes': []
                    },
                ],
            },
        ]
        output = import_json_view.generate_data_for_taxonomy(input_data, 'fr')
        self.assertEqual(
            output,
            [(u'/Animaux', 'animals'),
             (u'/Animaux/Oiseaux', 'birds'),
             (u'/Animaux/Oiseaux/Aigles', 'eagles'),
             (u'/Animaux/Oiseaux/Manchots', 'penguins'),
             (u'/Animaux/Mammifères', 'mammals'),
             (u'/Animaux/Mammifères/Vaches', 'cows'),
             (u'/Animaux/Mammifères/Lions', 'lions'),
             (u'/Animaux/Reptiles', 'reptiles'),
             (u'/Animaux/Reptiles/Pythons', 'pythons'),
             (u'/Végétaux', 'plants')])

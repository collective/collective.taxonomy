# -*- coding: utf-8 -*-
import unittest

from zope.component import queryUtility

from collective.taxonomy.interfaces import ITaxonomy
from collective.taxonomy.testing import INTEGRATION_TESTING


class TestUtility(unittest.TestCase):
    layer = INTEGRATION_TESTING

    def test_make_tree(self):
        taxonomy = queryUtility(ITaxonomy, name="collective.taxonomy.test")
        self.assertIsNotNone(taxonomy)

        tree = taxonomy.makeVocabulary("en").makeTree()
        self.assertIn("Information Science", tree)
        self.assertEqual(len(tree["Information Science"]), 4)

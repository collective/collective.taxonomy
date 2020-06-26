# -*- coding: utf-8 -*-
import unittest

from collective.taxonomy.interfaces import ITaxonomy
from collective.taxonomy.testing import INTEGRATION_TESTING
from zope.component import queryUtility


class TestUtility(unittest.TestCase):
    layer = INTEGRATION_TESTING

    def test_make_tree(self):
        taxonomy = queryUtility(ITaxonomy, name="collective.taxonomy.test")
        self.assertIsNotNone(taxonomy)

        tree = taxonomy.makeVocabulary("en").makeTree()
        self.assertIn(u"Information Science", tree)
        self.assertEqual(len(tree[u"Information Science"]), 3)

# -*- coding: utf-8 -*-
from collective.taxonomy.testing import INTEGRATION_TESTING
from collective.taxonomy.browser import VocabularyTuplesView
from collective.taxonomy.vocabulary import Vocabulary

import unittest


class TestTaxonomyTraverser(unittest.TestCase):
    """Test taxonomy traverser"""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]

    def test_traverser(self):
        view = self.portal.restrictedTraverse("++taxonomy++test")

        self.assertIsInstance(view, VocabularyTuplesView)
        self.assertIsInstance(view.vocabulary, Vocabulary)

        keys, labels = zip(*view())

        self.assertIn(u"Information Science", labels)

        keys, labels = zip(*view(target_language="de"))

        self.assertIn(u"Informatik", labels)
        self.assertNotIn(u"Information Science", labels)

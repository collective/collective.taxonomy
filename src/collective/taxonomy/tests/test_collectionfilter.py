from collective.taxonomy.collectionfilter import TaxonomyLabel
from collective.taxonomy.interfaces import ITaxonomy
from collective.taxonomy.testing import INTEGRATION_TESTING
from unittest import mock
from zope.component import getGlobalSiteManager
from zope.component import queryUtility
from zope.interface import implementer

import unittest


@implementer(ITaxonomy)
class DummyTaxonomy:
    default_language = "en"

    def __init__(self, name, label):
        self.name = name
        self.label = label
        self.inverted_data = {"en": {}}

    def translate(self, token, target_language=None):
        return f"{self.label}:{token}:{target_language}"


class TestTaxonomyLabel(unittest.TestCase):
    """TaxonomyLabel must not keep the persistent utility of the request that
    built the IGroupByCriteria registry (ConnectionStateError once that ZODB
    connection is closed); it resolves the utility by name on every call."""

    name = "collective.taxonomy.dummy"

    def tearDown(self):
        gsm = getGlobalSiteManager()
        util = gsm.queryUtility(ITaxonomy, name=self.name)
        if util is not None:
            gsm.unregisterUtility(util, ITaxonomy, name=self.name)

    def _register(self, label):
        util = DummyTaxonomy(self.name, label)
        getGlobalSiteManager().registerUtility(util, ITaxonomy, name=self.name)
        return util

    @mock.patch("plone.api.portal.get_current_language", return_value="en")
    def test_display_resolves_utility_per_call(self, _lang):
        first = self._register("first")
        label = TaxonomyLabel(first)
        self.assertNotIn("taxonomy", vars(label))
        self.assertEqual(label.display("tok"), "first:tok:en")
        # the utility object changes (new ZODB connection, re-registered
        # taxonomy) -- the label built earlier must pick up the current one
        self.tearDown()
        self._register("second")
        self.assertEqual(label.display("tok"), "second:tok:en")

    @mock.patch("plone.api.portal.get_current_language", return_value="fr")
    def test_display_falls_back_to_default_language(self, _lang):
        label = TaxonomyLabel(self._register("x"))
        self.assertEqual(label.display("tok"), "x:tok:en")

    def test_display_without_utility_returns_token(self):
        label = TaxonomyLabel(DummyTaxonomy(self.name, "gone"))
        self.assertEqual(label.display("tok"), "tok")

    def test_display_without_name_returns_token(self):
        self.assertEqual(TaxonomyLabel(None).display("tok"), "tok")


class TestTaxonomyLabelIntegration(unittest.TestCase):
    layer = INTEGRATION_TESTING

    def test_display_translates_with_registered_taxonomy(self):
        taxonomy = queryUtility(ITaxonomy, name="collective.taxonomy.test")
        label = TaxonomyLabel(taxonomy)
        token = next(iter(taxonomy.inverted_data["en"]))
        self.assertEqual(
            label.display(token),
            taxonomy.translate(token, target_language="en"),
        )

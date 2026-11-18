"""TaxonomyLabel must not keep the persistent utility of the request that
built the IGroupByCriteria registry (ConnectionStateError once that ZODB
connection is closed); it resolves the utility by name on every call."""

from . import DUMMY_NAME
from collective.taxonomy.collectionfilter import TaxonomyLabel
from collective.taxonomy.interfaces import ITaxonomy
from zope.component import getGlobalSiteManager
from zope.interface import implementer

import pytest


@implementer(ITaxonomy)
class DummyTaxonomy:
    default_language = "en"

    def __init__(self, name: str, label: str):
        self.name = name
        self.label = label
        self.inverted_data = {"en": {}}

    def translate(self, token, target_language=None):
        return f"{self.label}:{token}:{target_language}"


def _unregister() -> None:
    gsm = getGlobalSiteManager()
    util = gsm.queryUtility(ITaxonomy, name=DUMMY_NAME)
    if util is not None:
        gsm.unregisterUtility(util, ITaxonomy, name=DUMMY_NAME)


@pytest.fixture
def register():
    """Register a DummyTaxonomy globally; unregister it after the test."""

    def func(label: str) -> DummyTaxonomy:
        util = DummyTaxonomy(DUMMY_NAME, label)
        getGlobalSiteManager().registerUtility(util, ITaxonomy, name=DUMMY_NAME)
        return util

    yield func
    _unregister()


@pytest.fixture
def current_language(monkeypatch):
    """Set what plone.api reports as the current language."""

    def func(language: str) -> None:
        monkeypatch.setattr(
            "plone.api.portal.get_current_language", lambda *a, **kw: language
        )

    return func


class TestTaxonomyLabel:
    def test_display_resolves_utility_per_call(self, register, current_language):
        current_language("en")
        label = TaxonomyLabel(register("first"))
        assert "taxonomy" not in vars(label)
        assert label.display("tok") == "first:tok:en"
        # the utility object changes (new ZODB connection, re-registered
        # taxonomy) -- the label built earlier must pick up the current one
        _unregister()
        register("second")
        assert label.display("tok") == "second:tok:en"

    def test_display_falls_back_to_default_language(self, register, current_language):
        current_language("fr")
        label = TaxonomyLabel(register("x"))
        assert label.display("tok") == "x:tok:en"

    def test_display_without_utility_returns_token(self):
        label = TaxonomyLabel(DummyTaxonomy(DUMMY_NAME, "gone"))
        assert label.display("tok") == "tok"

    def test_display_without_name_returns_token(self):
        assert TaxonomyLabel(None).display("tok") == "tok"


class TestTaxonomyLabelIntegration:
    def test_display_translates_with_registered_taxonomy(self, taxonomy):
        label = TaxonomyLabel(taxonomy)
        token = next(iter(taxonomy.inverted_data["en"]))
        assert label.display(token) == taxonomy.translate(token, target_language="en")

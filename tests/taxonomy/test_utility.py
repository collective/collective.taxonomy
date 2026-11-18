from collective.taxonomy.browser import VocabularyTuplesView
from collective.taxonomy.vocabulary import Vocabulary


class TestUtility:
    def test_make_tree(self, taxonomy):
        tree = taxonomy.makeVocabulary("en").makeTree()
        assert "Information Science" in tree
        assert len(tree["Information Science"]) == 5


class TestTaxonomyTraverser:
    def test_traverser(self, portal):
        view = portal.restrictedTraverse("++taxonomy++test")

        assert isinstance(view, VocabularyTuplesView)
        assert isinstance(view.vocabulary, Vocabulary)

        _keys, labels = zip(*view(), strict=True)
        assert "Information Science" in labels

        _keys, labels = zip(*view(target_language="de"), strict=True)
        assert "Informatik" in labels
        assert "Information Science" not in labels

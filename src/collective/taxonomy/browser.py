from collective.taxonomy.interfaces import ITaxonomy
from Products.Five.browser import BrowserView
from zope.component import getSiteManager
from zope.i18n import translate
from zope.interface import implementer_only
from zope.publisher.interfaces import NotFound
from zope.schema.interfaces import IVocabularyFactory
from zope.traversing.interfaces import ITraversable


class TaxonomyView(BrowserView):
    def taxonomiesForContext(self, short_names=[]):
        results = []

        sm = getSiteManager()
        utilities = sm.getUtilitiesFor(ITaxonomy)
        for (utility_name, utility,) in utilities:
            short_name = utility.getShortName()

            if short_names and short_name not in short_names:
                continue

            if getattr(self.context, "taxonomy_" + short_name, None):
                for taxon in getattr(self.context, "taxonomy_" + short_name):
                    results.append(
                        self.translate(
                            taxon, domain="collective.taxonomy." + short_name
                        )
                    )

        return results

    def translate(self, msgid, domain="", target_language=None):
        """ Eq to context.translate(msgid, domain) """
        sm = getSiteManager()
        utility = sm.queryUtility(ITaxonomy, name=domain)
        return utility.translate(
            msgid, context=self.context, target_language=target_language
        )  # noqa: E501


class VocabularyTuplesView(BrowserView):
    def __init__(self, context, request, vocabulary):
        super(VocabularyTuplesView, self).__init__(context, request)
        self.vocabulary = vocabulary

    def __call__(self, target_language=None):
        return (
            (
                term.token,
                translate(
                    term.title, context=self.request, target_language=target_language
                ),
            )
            for term in self.vocabulary
        )


@implementer_only(ITraversable)
class TaxonomyTraverser(BrowserView):
    def traverse(self, name, remaining):
        sm = getSiteManager()
        domain = "collective.taxonomy." + name
        factory = sm.queryUtility(IVocabularyFactory, name=domain)

        if factory is not None:
            vocabulary = factory(self.context)
        else:
            raise NotFound(self.context, name, self.request)

        return VocabularyTuplesView(self.context, self.request, vocabulary)

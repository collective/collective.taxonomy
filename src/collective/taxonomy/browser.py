from Products.Five.browser import BrowserView
from collective.taxonomy.interfaces import ITaxonomy
from zope.component import getSiteManager
from zope.publisher.interfaces import NotFound
from zope.traversing.interfaces import ITraversable
from zope.schema.interfaces import IVocabularyFactory
from zope.interface import implements


class TaxonomyView(BrowserView):

    def taxonomiesForContext(self, short_names=[]):
        results = []

        sm = getSiteManager()
        utilities = sm.getUtilitiesFor(ITaxonomy)
        for (utility_name, utility,) in utilities:
            short_name = utility.getShortName()

            if short_names and short_name not in short_names:
                continue

            if getattr(self.context, 'taxonomy_' + short_name, None):
                for taxon in getattr(self.context, 'taxonomy_' + short_name):
                    results.append(self.translate(
                        taxon,
                        domain='collective.taxonomy.' + short_name
                    )
                )

        return results

    def translate(self, msgid, domain='', target_language=None):
        """ Eq to context.translate(msgid, domain) """
        sm = getSiteManager()
        utility = sm.queryUtility(ITaxonomy, name=domain)
        return utility.translate(msgid, context=self.context, target_language=target_language)


class VocabularyTuplesView(BrowserView):

    def __init__(self, context, request, vocabulary):
        self.context = context
        self.request = request
        self.vocabulary = vocabulary

    def __call__(self):
        return ((term.token, term.title) for term in self.vocabulary)


class TaxonomyTraverser(object):

    implements(ITraversable)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def traverse(self, name, remaining):
        sm = getSiteManager()
        domain = 'collective.taxonomy.' + name
        factory = sm.queryUtility(IVocabularyFactory, name=domain)

        if factory is not None:
            vocabulary = factory(self.context)
        else:
            raise NotFound(self.context, name, self.request)

        return VocabularyTuplesView(self.context, self.request, vocabulary)

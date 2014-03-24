from Products.Five.browser import BrowserView
from collective.taxonomy.interfaces import ITaxonomy
from zope.component import getSiteManager


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

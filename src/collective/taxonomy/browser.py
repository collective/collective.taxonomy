from Products.Five.browser import BrowserView
from collective.taxonomy.interfaces import ITaxonomy


class TaxonomyView(BrowserView):

    def translate(self, msgid, domain='', target_language='en'):
        sm = self.context.getSiteManager()
        utility = sm.queryUtility(ITaxonomy, name=domain)
        return utility.translate(msgid, context=self.context)

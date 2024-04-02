from collective.taxonomy.i18n import CollectiveTaxonomyMessageFactory as _
from collective.taxonomy.interfaces import ITaxonomy
from plone.restapi.services import Service
from zExceptions import BadRequest
from zope.i18n.interfaces import ITranslationDomain
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse
from zope.schema.interfaces import IVocabularyFactory


@implementer(IPublishTraverse)
class TaxonomyDelete(Service):
    """Deletes a field/fieldset from content type"""

    def __init__(self, context, request):
        super().__init__(context, request)
        self.params = []

    def publishTraverse(self, request, name):
        # Treat any path segments after /@types as parameters
        self.params.append(name)
        return self

    def reply(self):
        if not self.params:
            raise BadRequest(
                _(
                    "delete_taxonomies_no_taxonomies",
                    default="You need to provide a taxonomy to delete.",
                )
            )
        if len(self.params) > 1:
            self.request.response.setStatus(404)
            return

        name = self.params[0]
        sm = self.context.getSiteManager()
        utility = sm.queryUtility(ITaxonomy, name=name)
        if utility is None:
            self.request.response.setStatus(404)
            return
        utility.unregisterBehavior()
        sm.unregisterUtility(utility, ITaxonomy, name=name)
        sm.unregisterUtility(utility, IVocabularyFactory, name=name)
        sm.unregisterUtility(utility, ITranslationDomain, name=name)

        return self.reply_no_content()

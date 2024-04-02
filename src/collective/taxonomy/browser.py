from collective.taxonomy.interfaces import ITaxonomy
from plone import api
from plone.app.contenttypes.browser.collection import CollectionView
from plone.app.vocabularies.metadatafields import get_field_label
from plone.base.utils import safe_callable
from plone.behavior.interfaces import IBehavior
from Products.Five.browser import BrowserView
from zope.component import getSiteManager
from zope.component import queryUtility
from zope.component.hooks import getSite
from zope.i18n import translate
from zope.interface import implementer_only
from zope.publisher.interfaces import NotFound
from zope.schema.interfaces import IVocabularyFactory
from zope.traversing.interfaces import ITraversable

import Missing


class TaxonomyView(BrowserView):
    def taxonomiesForContext(self, short_names=[]):
        results = []

        sm = getSiteManager()
        utilities = sm.getUtilitiesFor(ITaxonomy)
        for (
            utility_name,
            utility,
        ) in utilities:
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
        """Eq to context.translate(msgid, domain)"""
        sm = getSiteManager()
        utility = sm.queryUtility(ITaxonomy, name=domain)
        return utility.translate(
            msgid, context=self.context, target_language=target_language
        )  # noqa: E501


class VocabularyTuplesView(BrowserView):
    def __init__(self, context, request, vocabulary):
        super().__init__(context, request)
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


class TaxonomyCollectionView(CollectionView):
    """Extend CollectionView (tabular) to resolve taxonomy tokens into values."""

    def tabular_fielddata(self, item, fieldname):
        value = getattr(item, fieldname, "")
        if safe_callable(value):
            value = value()
        if fieldname in [
            "CreationDate",
            "ModificationDate",
            "Date",
            "EffectiveDate",
            "ExpirationDate",
            "effective",
            "expires",
            "start",
            "end",
            "created",
            "modified",
            "last_comment_date",
        ]:
            value = self.toLocalizedTime(value, long_format=1)
        if value == Missing.Value:
            value = ""
        value = self.resolveTaxonomyValue(fieldname, value)
        return {
            "value": value,
        }

    def tabular_field_label(self, field):
        """Return the internationalized label (Message object) corresponding
        to the field.
        """
        label = get_field_label(field)
        label = self.resolveTaxonomyTitle(label)
        return label

    def _get_taxonomy_utilities(self):
        # import pdb; pdb.set_trace()
        sm = getSite().getSiteManager()
        return sm.getUtilitiesFor(ITaxonomy)

    def resolveTaxonomyTitle(self, fieldname):
        """resolve taxonolomy title from behavior."""
        utilities = self._get_taxonomy_utilities()
        sm = getSite().getSiteManager()
        for uname, util in utilities:
            behavior = sm.queryUtility(IBehavior, name=util.getGeneratedName())
            shortname = uname[len("collective.taxonomy.") :]
            if shortname != fieldname[len(behavior.field_prefix) :]:
                continue
            return util.title
        return fieldname

    def resolveTaxonomyValue(self, fieldname, value):
        sm = getSite().getSiteManager()
        utilities = self._get_taxonomy_utilities()
        taxonomies = {}
        taxonomy_field_prefix = ""
        for uname, util in utilities:
            taxonomies[uname[len("collective.taxonomy.") :]] = uname
            if taxonomy_field_prefix:
                continue
            behavior = sm.queryUtility(IBehavior, name=util.getGeneratedName())
            taxonomy_field_prefix = behavior.field_prefix
        if not taxonomies:
            return value
        taxonomy_shortname = fieldname[len(taxonomy_field_prefix) :]
        if taxonomy_shortname not in taxonomies:
            return value
        taxonomy = queryUtility(ITaxonomy, name=taxonomies.get(taxonomy_shortname))
        if not taxonomy:
            return value
        lang = api.portal.get_current_language()
        lang = lang in taxonomy.data and lang or taxonomy.default_language
        translated_terms = [taxonomy.translate(v, target_language=lang) for v in value]
        return ", ".join(translated_terms)

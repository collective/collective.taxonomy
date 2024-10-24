from collective.collectionfilter.interfaces import IGroupByCriteria
from collective.collectionfilter.interfaces import IGroupByModifier
from collective.taxonomy.interfaces import ITaxonomy
from plone import api
from plone.behavior.interfaces import IBehavior
from zope.component import adapter
from zope.component.hooks import getSite
from zope.interface import implementer


class TaxonomyLabel:
    taxonomy = None

    def __init__(self, taxonomy):
        self.taxonomy = taxonomy

    def display(self, token, *args, **kw):
        if self.taxonomy is None:
            return token
        lang = api.portal.get_current_language()
        lang = (
            lang in self.taxonomy.inverted_data
            and lang
            or self.taxonomy.default_language
        )
        term = self.taxonomy.translate(token, target_language=lang)
        return term


@implementer(IGroupByModifier)
@adapter(IGroupByCriteria)
def groupby_modifier(groupby):
    sm = getSite().getSiteManager()
    utilities = sm.getUtilitiesFor(ITaxonomy)
    for uname, util in utilities:
        behavior = sm.queryUtility(IBehavior, name=util.getGeneratedName())
        taxonomy_field_prefix = behavior.field_prefix
        taxonomy_shortname = util.getShortName()
        taxonomy_index_name = f"{taxonomy_field_prefix}{taxonomy_shortname}"
        taxonomy_label = TaxonomyLabel(util)
        groupby._groupby[taxonomy_index_name] = {
            "index": taxonomy_index_name,
            "metadata": taxonomy_index_name,
            "display_modifier": taxonomy_label.display,
        }

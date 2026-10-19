from collective.collectionfilter.interfaces import IGroupByCriteria
from collective.collectionfilter.interfaces import IGroupByModifier
from collective.taxonomy.interfaces import ITaxonomy
from plone import api
from plone.behavior.interfaces import IBehavior
from zope.component import adapter
from zope.component import queryUtility
from zope.component.hooks import getSite
from zope.interface import implementer


class TaxonomyLabel:
    """Display modifier for one taxonomy index.

    Instances live in the process-wide IGroupByCriteria registry, so they must
    not hold the persistent Taxonomy utility itself: it belongs to the ZODB
    connection of the request that built the registry and raises
    ConnectionStateError once that connection is closed. Keep the utility name
    and look the utility up on every call.
    """

    name = None

    def __init__(self, taxonomy):
        self.name = getattr(taxonomy, "name", None)

    @property
    def taxonomy(self):
        if not self.name:
            return None
        return queryUtility(ITaxonomy, name=self.name)

    def display(self, token, *args, **kw):
        taxonomy = self.taxonomy
        if taxonomy is None:
            return token
        lang = api.portal.get_current_language()
        lang = lang in taxonomy.inverted_data and lang or taxonomy.default_language
        return taxonomy.translate(token, target_language=lang)


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

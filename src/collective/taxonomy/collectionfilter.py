from collective.collectionfilter.interfaces import IGroupByCriteria, IGroupByModifier
from collective.taxonomy import PATH_SEPARATOR, PRETTY_PATH_SEPARATOR, utility
from collective.taxonomy.interfaces import ITaxonomy
from plone import api
from plone.behavior.interfaces import IBehavior
from zope.component import adapter
from zope.component.hooks import getSite
from zope.component import queryUtility
from zope.interface import implementer


def resolve_title(token, index_name):
    sm = getSite().getSiteManager()
    utilities = sm.getUtilitiesFor(ITaxonomy)
    taxonomies = [uname for uname, util in utilities]
    shortname = None
    taxonomy_name = None
    for tax in taxonomies:
        shortname = tax[len("collective.taxonomy.") :]
        if not index_name.endswith(shortname):
            continue
        taxonomy_name = tax
    if not shortname or not taxonomy_name:
        return token
    taxonomy = queryUtility(ITaxonomy, name=taxonomy_name)
    lang = api.portal.get_current_language()
    lang = lang in taxonomy.inverted_data and lang or taxonomy.default_language
    term = taxonomy.translate(token, target_language=lang)
    return term


@implementer(IGroupByModifier)
@adapter(IGroupByCriteria)
def groupby_modifier(groupby):
    sm = getSite().getSiteManager()
    utilities = sm.getUtilitiesFor(ITaxonomy)
    for taxonomy in utilities:
        behavior = sm.queryUtility(IBehavior, name=taxonomy[1].getGeneratedName())
        taxonomy_field_prefix = behavior.field_prefix
        taxonomy_shortname = taxonomy[1].getShortName()
        taxonomy_index_name = "{0}{1}".format(taxonomy_field_prefix, taxonomy_shortname)
        groupby._groupby[taxonomy_index_name] = {
            "index": taxonomy_index_name,
            "metadata": taxonomy_index_name,
            "display_modifier": lambda it, idx: resolve_title(it, idx),
        }

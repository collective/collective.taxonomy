from collective.taxonomy.interfaces import ITaxonomySelectWidget
from plone import api
from plone.memoize import ram
from z3c.form import interfaces
from z3c.form.widget import FieldWidget

import zope.component
import zope.interface
import zope.schema.interfaces


try:
    # Plone 6.1
    from plone.app.z3cform.widgets.orderedselect import OrderedSelectWidget
except ImportError:
    from z3c.form.browser.orderedselect import OrderedSelectWidget


def _items_cachekey(fun, self):
    # try to get modified time of taxonomy utility
    try:
        mtime = self.terms.terms.data._p_mtime
        lng = api.portal.get_current_language()
        key = f"{self.field.__name__}-{lng}-{mtime}"
        return key
    except AttributeError:
        # XXX: this happens with newly created taxonomies
        # from profiles/xxx/taxonomies ... why are they not an utility?
        # do not cache this.
        raise ram.DontCache()


@zope.interface.implementer(ITaxonomySelectWidget, interfaces.IOrderedSelectWidget)
class TaxonomySelectWidget(OrderedSelectWidget):
    @ram.cache(_items_cachekey)
    def _get_items(self):
        return [self.getItem(term, count) for count, term in enumerate(self.terms)]

    def update(self):
        """See z3c.form.interfaces.IWidget."""
        super().update()
        self.items = self._get_items()
        self.selectedItems = [
            self.getItem(self.terms.getTermByToken(token), count)
            for count, token in enumerate(self.value)
        ]
        self.notselectedItems = self.deselect()


@zope.component.adapter(zope.schema.interfaces.ISequence, interfaces.IFormLayer)
@zope.interface.implementer(interfaces.IFieldWidget)
def TaxonomySelectFieldWidget(field, request):
    """IFieldWidget factory for SelectWidget."""
    return FieldWidget(field, TaxonomySelectWidget(request))

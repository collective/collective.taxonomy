from time import time
from plone.memoize import ram
import zope.interface
import zope.component
import zope.schema.interfaces

from z3c.form import interfaces
from z3c.form.browser.orderedselect import OrderedSelectWidget
from z3c.form.widget import FieldWidget
from z3c.form.widget import SequenceWidget
from z3c.form.browser import widget

from interfaces import ITaxonomySelectWidget

ONE_DAY = 60 * 60 * 24


def _cache_one_day(fun, self):
    key = '{0}{1}'.format(
        self.field.__name__,
        time() // ONE_DAY
    )
    return key


@zope.interface.implementer(ITaxonomySelectWidget,
                            interfaces.IOrderedSelectWidget)
class TaxonomySelectWidget(OrderedSelectWidget):

    @ram.cache(_cache_one_day)
    def _get_items(self):
        return [
            self.getItem(term, count)
            for count, term in enumerate(self.terms)
            ]

    def update(self):
        """See z3c.form.interfaces.IWidget."""
        SequenceWidget.update(self)
        widget.addFieldClass(self)
        self.items = self._get_items()
        self.selectedItems = [
            self.getItem(self.terms.getTermByToken(token), count)
            for count, token in enumerate(self.value)]
        self.notselectedItems = self.deselect()


@zope.component.adapter(zope.schema.interfaces.ISequence,
                        interfaces.IFormLayer)
@zope.interface.implementer(interfaces.IFieldWidget)
def TaxonomySelectFieldWidget(field, request):
    """IFieldWidget factory for SelectWidget."""
    return FieldWidget(field, TaxonomySelectWidget(request))

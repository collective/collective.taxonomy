import zope.interface
import zope.component
import zope.schema.interfaces

from z3c.form import interfaces
from z3c.form.browser.orderedselect import OrderedSelectWidget
from z3c.form.widget import FieldWidget

from interfaces import ITaxonomySelectWidget


class TaxonomySelectWidget(OrderedSelectWidget):
    zope.interface.implements(ITaxonomySelectWidget,
                              interfaces.IOrderedSelectWidget)


@zope.component.adapter(zope.schema.interfaces.ISequence,
                        interfaces.IFormLayer)
@zope.interface.implementer(interfaces.IFieldWidget)
def TaxonomySelectFieldWidget(field, request):
    """IFieldWidget factory for SelectWidget."""
    return FieldWidget(field, TaxonomySelectWidget(request))

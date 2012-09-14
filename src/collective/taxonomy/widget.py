# -*- coding: utf-8 -*-
import Acquisition
import zope.interface
import zope.schema.interfaces

import z3c.form.interfaces
import z3c.form.widget

from zope.i18n import translate
from z3c.form.browser.select import SelectWidget
from z3c.form.interfaces import ISelectWidget

class ITaxonomyWidget(ISelectWidget):
    pass


class TaxonomyWidget(SelectWidget):
    zope.interface.implementsOnly(ITaxonomyWidget)

    klass = u'taxonomy-widget'
    value = u''

    def isChecked(self, term):
        return term.token in self.value

    def update(self):
        """See z3c.form.interfaces.IWidget."""
        super(TaxonomyWidget, self).update()
        widget.addFieldClass(self)

        self.items = {}

        for count, term in enumerate(self.terms):
            checked = self.isChecked(term)
            id = '%s-%i' % (self.id, count)
            label = term.token

            if zope.schema.interfaces.ITitledTokenizedTerm.providedBy(term):
                label = translate(term.title, context=self.request,
                                  default=term.title)

            # generate items


@zope.component.adapter(zope.schema.interfaces.IField,
                        z3c.form.interfaces.IFormLayer)
@zope.interface.implementer(z3c.form.interfaces.IFieldWidget)
def TaxonomyFieldWidget(field, request):
    """IFieldWidget factory for WysiwygWidget."""
    return z3c.form.widget.FieldWidget(field, TaxonomyWidget(request))

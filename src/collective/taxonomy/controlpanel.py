from Products.Five.browser import BrowserView

from z3c.form import form, field

from interfaces import ITaxonomy, ITaxonomyForm

class AddTaxonomyForm(form.AddForm):
    fields = field.Fields(ITaxonomyForm)

class ControlPanelView(BrowserView):
    """ """

    @property
    def taxonomies(self):
        results = []
        sm = self.context.getSiteManager()
        utilities = sm.getUtilitiesFor(ITaxonomy)

        for (utility_name, utility) in utilities:
            results.append({'name': utility.name,
                            'title': utility.title})

        return results

    def getAddForm(self):
        add_form = AddTaxonomyForm(self.context, self.context.REQUEST)
        add_form.update()
        return add_form.render()


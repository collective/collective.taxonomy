import generated

from persistent import Persistent

from plone.directives import form
from plone.behavior.interfaces import IBehavior
from plone.memoize import ram
from plone.supermodel.model import SchemaClass, Schema

from zope import schema
from zope.interface import implements, alsoProvides

from .i18n import MessageFactory as _


class TaxonomyBehavior(Persistent):
    implements(IBehavior)

    def __init__(self, title, description, field_name,
                 field_title, field_description, is_required,
                 multi_select):
        self.title = _(title)
        self.description = _(description)
        self.factory = None
        self.field_name = field_name
        self.field_title = field_title
        self.field_description = field_description
        self.is_required = is_required
        self.multi_select = multi_select

    @property
    def short_name(self):
        return str(self.title.split('.')[-1])

    @property
    @ram.cache(lambda method, self: str(self.__dict__))
    def interface(self):

        single_select_field = schema.Choice(
            title=_(unicode(self.field_title)),
            description=_(unicode(self.field_description)),
            required=self.is_required,
            vocabulary='collective.taxonomy.' +
            self.short_name)

        multi_select_field = schema.List(
            title=_(unicode(self.field_title)),
            description=_(unicode(self.field_description)),
            value_type=schema.Choice(
                required=self.is_required,
                vocabulary='collective.taxonomy.' +
                self.short_name))

        schemaclass = SchemaClass(
            self.short_name, (Schema, ),
            __module__='collective.taxonomy.generated',
            attrs={str(self.field_name):
                   self.multi_select
                   and multi_select_field
                   or single_select_field }
        )

        alsoProvides(schemaclass, form.IFormFieldProvider)

        return schemaclass

    @property
    def marker(self):
        return self.interface

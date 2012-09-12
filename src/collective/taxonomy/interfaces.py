from z3c.form import interfaces

from zope import schema
from zope.interface import Interface

from i18n import MessageFactory as _

class ITaxonomy(Interface):
    """ Browser layer """

class ITaxonomyRegistry(Interface):
    """ Registry storage """

    taxonomies = schema.Dict(title=_(u"Taxonomies"),
                                  description=_(u"taxonomies",
                                                default=u"Here is the available taxonomies on the site"),
                                  required=False,
                                  key_type=schema.ASCII(title=_(u"Vocabulary name")),
                                  value_type=schema.Dict(
                                     title=_(u"Taxonomi"),
                                     key_type=schema.ASCII(title=_(u"UID")),
                                     value_type=schema.TextLine(title=_(u"Written value"))
                                 )
                             )

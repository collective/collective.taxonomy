from zExceptions import BadRequest, NotFound

from zope.interface import implements
from zope.component import adapts
from zope.traversing.interfaces import ITraversable
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.publisher.interfaces.browser import IBrowserRequest

class TaxonomyTraverser(object):
    implements(ITraversable)
    adapts(IAttributeAnnotatable, IBrowserRequest)

    def __init__(self, context, request=None):
        self.context = context
        self.request = request

    def traverse(self, name, ignore):
        return name



# generated interfaces.

import sys

from zope.component.hooks import getSite

from plone.supermodel.model import SchemaClass
from plone.behavior.interfaces import IBehavior
from plone.directives import form


class Wrapper(object):

    def __init__(self, wrapped):
        self.__dict__['wrapped'] = wrapped

    def __setattr__(self, name, value):
        setattr(self.__dict__['wrapped'], name, value)

    def __getattr__(self, name):
        try:
            return getattr(self.__dict__['wrapped'], name)
        except AttributeError as attrError:
            sm = getSite().getSiteManager()

            utility = sm.queryUtility(
                IBehavior,
                name='collective.taxonomy.generated.' + name
            )

            if not utility:
                setattr(self.__dict__['wrapped'], name, SchemaClass(
                    name, (form.Schema, ),
                    __module__='collective.taxonomy.generated',
                    attrs={}))
                return getattr(self.__dict__['wrapped'], name)
            else:
                raise attrError
        except Exception as exception:
            raise exception

sys.modules[__name__] = Wrapper(sys.modules[__name__])

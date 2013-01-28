# generated interfaces.

import sys

from zope.component.hooks import getSite

from plone.supermodel.model import SchemaClass
from plone.behavior.interfaces import IBehavior
from plone.directives import form


class Wrapper(object):
    __name__ = __name__

    def __init__(self, wrapped):
        self.__dict__['wrapped'] = wrapped

    def __delattr__(self, name):
        if hasattr(self.__dict__['wrapped'], name):
            delattr(self.__dict__['wrapped'], name)

    def __setattr__(self, name, value):
        raise NotImplementedError(u"Taxonomy: __setattr__ for generated should"
                                  u"not be called!")

    def __getattr__(self, name):
        if name.startswith('__'):
            return getattr(self.__dict__['wrapped'], name)

        if not hasattr(self.__dict__['wrapped'], name):
            sm = getSite().getSiteManager()

            utility = sm.queryUtility(
                IBehavior,
                name='collective.taxonomy.generated.' + name
            )

            if utility:
                setattr(
                    self.__dict__['wrapped'],
                    name,
                    utility.generateInterface()
                )
            else:
                setattr(
                    self.__dict__['wrapped'],
                    name,
                    SchemaClass(
                        name,
                        (form.Schema, ),
                        __module__='collective.taxonomy.generated',
                        attrs={}
                    )
                )

        return getattr(self.__dict__['wrapped'], name)

if type(sys.modules[__name__]) is not Wrapper:
    sys.modules[__name__] = Wrapper(sys.modules[__name__])

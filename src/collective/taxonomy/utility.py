# -*- coding: utf-8 -*-

from BTrees.OIBTree import OIBTree

class Taxonomy(OIBTree):
    def __init__(self, title):
        super(Taxonomy, self).__init__(self)
        self.title = title

    def add(self, identifier, path):
        self[path] = identifier

    def translate(msgid, mapping=None, context=None, target_language=None, default=None):
        import pdb; pdb.set_trace()

    def __call__(self, context):
        language = context.get_the_default_plone_language()

        #return self.get_a_simple_vocabulary_with_this_æangu_as_the_titles_but_its_translatable_through_the_msgid ... amybe.
        return []





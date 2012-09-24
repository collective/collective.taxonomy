
from interfaces import ITaxonomy

from zope.i18nmessageid import MessageFactory
from zope.interface import implements
from zope.schema.interfaces import IVocabulary, IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary


class TaxonomyVocabulary(object):
    """ Vocabulary for generating a list of existing taxonomies """
    implements(IVocabularyFactory)

    def __call__(self, adapter):
        results = []
        context = adapter.context
        sm = context.getSiteManager()
        utilities = sm.getUtilitiesFor(ITaxonomy)

        for (utility_name, utility) in utilities:
            results.append(SimpleTerm(value=utility.name,
                                      title=utility.title))

        return SimpleVocabulary(results)


class Vocabulary(object):
    """ Vocabulary object, when the utilitity is used as a
    vocabulary object """
    implements(IVocabulary)

    def __init__(self, name, data, inv_data):
        self.data = data
        self.inv_data = inv_data
        self.message = MessageFactory(name)

    def __iter__(self):
        for term in self.getTerms():
            yield term

    def __len__(self):
        return len(self.getTerms())

    def __contains__(self, identifier):
        return self.getTerm(identifier) is not None

    def getTermByToken(self, input_identifier):
        return SimpleTerm(value=int(input_identifier),
                          title=self.message(int(input_identifier),
                                             self.inv_data[
                                                 int(input_identifier)]))

    def getTerm(self, input_identifier):
        return self.getTermByToken(input_identifier)

    def getTerms(self):
        results = []

        for (path, identifier) in self.data.items():
            term = SimpleTerm(value=identifier,
                              title=self.message(identifier, path))
            results.append(term)

        return results

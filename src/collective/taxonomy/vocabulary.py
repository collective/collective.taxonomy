
from zope.i18nmessageid import MessageFactory
from zope.interface import implements
from zope.schema.interfaces import IVocabulary
from zope.schema.vocabulary import SimpleTerm


class Vocabulary(object):
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

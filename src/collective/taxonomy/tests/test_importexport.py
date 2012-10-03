import os.path
import unittest2 as unittest

from zope import schema
from zope.component import queryUtility, createObject
from zope.component.interfaces import IFactory

from ..testing import INTEGRATION_TESTING
from ..interfaces import ITaxonomy

from plone.behavior.interfaces import IBehavior
from plone.directives import form
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.fti import DexterityFTI
from plone.dexterity.factory import DexterityFactory
from z3c.form import field

from ..i18n import MessageFactory as _


class TestContent(form.Schema):
    test = schema.TextLine(
        title=_(u"Hest"),
        description=_(u""),
        required=False,
    )


class TestImportExport(unittest.TestCase):
    layer = INTEGRATION_TESTING

    vdex_file_contents = open(os.path.dirname(__file__) +
                              "/examples/nihms.xml").read()

    @property
    def adapter(self):
        from collective.taxonomy.exportimport \
            import TaxonomyImportExportAdapter

        portal = self.layer['portal']
        return TaxonomyImportExportAdapter(portal)

    def test_import_example(self):
        """ Tests, that we can import and get an adequate result """
        utility_name = self.adapter.importDocument(self.vdex_file_contents)
        utility = queryUtility(ITaxonomy, name=utility_name)
        self.assertTrue(utility)
        self.assertTrue(utility.keys() == ['ru', 'de', 'en', 'da'])
        self.assertTrue([key for key in utility['en'].keys()] ==
                        ['/Information Science',
                         '/Information Science/Book Collecting',
                         '/Information Science/Chronology'])

    def test_import_export_example(self):
        """ Tests, that we can import and export getting the same result """
        utility_name = self.adapter.importDocument(self.vdex_file_contents)
        body = self.adapter.exportDocument(utility_name)
        self.assertTrue(body == self.vdex_file_contents, body)

    def test_vocabulary(self):
        """ Testing that the vocabulary contains the correct contents """
        utility_name = self.adapter.importDocument(self.vdex_file_contents)
        utility = queryUtility(ITaxonomy, name=utility_name)
        vocab = utility(self.layer['portal'])
        self.assertTrue([term.value for term in vocab.getTerms()] ==
                        ['/Information Science',
                         '/Information Science/Book Collecting',
                         '/Information Science/Chronology'])

    def test_translate(self):
        utility_name = self.adapter.importDocument(self.vdex_file_contents)
        utility = queryUtility(ITaxonomy, name=utility_name)
        self.assertTrue(utility.translate(1) == '/Information Science')

    def test_behaviour_registration(self):
        utility_name = self.adapter.importDocument(self.vdex_file_contents)
        sm = self.layer['portal'].getSiteManager()
        behavior = sm.queryUtility(IBehavior, name=utility_name)
        self.assertTrue(behavior is not None, behavior)

    def test_behaviour_has_choice_field(self):
        utility_name = self.adapter.importDocument(self.vdex_file_contents)
        sm = self.layer['portal'].getSiteManager()
        behavior = sm.queryUtility(IBehavior, name=utility_name)
        fields = field.Fields(behavior.interface)
        self.assertTrue("TestField" in fields)
        #fields = give_me_the_fields(behavior)
        #self.assertTrue(one of them i IChoice)

    # def test_create_content_type(self):
    #     fti = DexterityFTI("TestContent")
    #     fti.schema = "collective.taxonomy.tests.test_importexport.TestContent"
    #     fti.klass = "plone.dexterity.content.Item"
    #     fti.behaviors = ('collective.taxonomy.generated.testVocabulary')
    #     fti.allow_discussion = False
    #     fti.global_allow = True
    #     sm = self.layer['portal'].getSiteManager()
    #     sm.registerUtility(fti, IDexterityFTI, name='TestContent')
    #     sm.registerUtility(DexterityFactory('TestContent'),
    #                        IFactory, name='TestContent')
    #     test_object = createObject('TestContent')
    #     import pdb; pdb.set_trace()

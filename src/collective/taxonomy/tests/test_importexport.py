import os.path
import unittest2 as unittest

from plone.app.testing import PLONE_INTEGRATION_TESTING
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login

from ..testing import INTEGRATION_TESTING


class TestImportExport(unittest.TestCase):
    layer = INTEGRATION_TESTING

    vdex_file_contents = open(os.path.dirname(__file__) + "/examples/nihms.xml").read()

    class test_environ:
        @staticmethod
        def shouldPurge():
            return True

        @staticmethod
        def getLogger(name):
            import logging
            return logging.getLogger(name)

    @property
    def adapter(self):
        from collective.taxonomy.exportimport import TaxonomyImportExportAdapter
        portal = self.layer['portal']
        return TaxonomyImportExportAdapter(portal, self.test_environ)

    def test_import_export_example(self):
        un = self.adapter.importDocument(self.vdex_file_contents)
        body = self.adapter.exportDocument(un)
        self.assertTrue(body == self.vdex_file_contents, body)


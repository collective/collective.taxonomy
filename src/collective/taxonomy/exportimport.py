from collective.taxonomy.factory import registerTaxonomy
from collective.taxonomy.interfaces import ITaxonomy
from collective.taxonomy.vdex import ExportVdex
from collective.taxonomy.vdex import ImportVdex
from io import StringIO
from lxml.etree import fromstring
from plone.base.utils import safe_text
from plone.behavior.interfaces import IBehavior

import configparser


def parseConfigFile(data):
    try:
        config = configparser.RawConfigParser(allow_no_value=True)
    except Exception as exception:
        raise exception

    config.read_file(StringIO(data.decode("utf-8")))
    return config


def importTaxonomy(context):
    directory = context.listDirectory("taxonomies/")

    if not directory:
        return

    for filename in directory:
        if filename.endswith(".xml"):
            continue

        if filename.endswith(".cfg"):
            data = context.readDataFile("taxonomies/" + filename)
            config = parseConfigFile(data)

            filename = "taxonomies/" + filename.replace(".cfg", ".xml")
            body = context.readDataFile(filename)
            if body is not None:
                result = {}
                for name in ["name", "title", "description", "default_language"]:
                    try:
                        result[name] = config.get("taxonomy", name)
                    except configparser.NoOptionError:
                        pass

                taxonomy = registerTaxonomy(context, **result)
                importer = TaxonomyImportExportAdapter(context)
                importer.importDocument(taxonomy, body)

                result = {}
                for name in [
                    "field_title",
                    "field_description",
                    "default_language",
                    "write_permission",
                    "taxonomy_fieldset",
                    "field_prefix",
                ]:
                    try:
                        result[name] = config.get("taxonomy", name)
                    except configparser.NoOptionError:
                        pass

                for name in ["is_single_select", "is_required"]:
                    try:
                        result[name] = (
                            config.get("taxonomy", name) == "true" and True
                        )  # noqa: E501
                    except configparser.NoOptionError:
                        pass

                taxonomy.registerBehavior(**result)


def exportTaxonomy(context):
    site = context.getSite()
    sm = site.getSiteManager()
    for name, taxonomy in sm.getUtilitiesFor(ITaxonomy):
        behavior = sm.queryUtility(IBehavior, name=taxonomy.getGeneratedName())

        short_name = name.split(".")[-1]
        exporter = TaxonomyImportExportAdapter(context)
        body = exporter.exportDocument(taxonomy)

        if body is not None:
            config = configparser.RawConfigParser()

            config.add_section("taxonomy")
            name = name.replace("collective.taxonomy.", "")
            config.set("taxonomy", "name", name)

            for name in ["title", "description", "default_language"]:
                value = getattr(taxonomy, name, None)
                if value:
                    config.set("taxonomy", name, safe_text(value))

            for name in [
                "field_title",
                "field_description",
                "write_permission",
                "taxonomy_fieldset",
                "field_prefix",
            ]:
                value = getattr(behavior, name, None)
                if value is not None:
                    config.set("taxonomy", name, safe_text(value))

            for name in ["is_single_select", "is_required"]:
                value = getattr(behavior, name, None)
                if value:
                    config.set("taxonomy", name, str(value).lower())

            filehandle = StringIO()
            config.write(filehandle)
            context.writeDataFile(
                "taxonomies/" + short_name + ".cfg", filehandle.getvalue(), "text/plain"
            )
            context.writeDataFile("taxonomies/" + short_name + ".xml", body, "text/xml")


class TaxonomyImportExportAdapter:
    IMSVDEX_NS = "http://www.imsglobal.org/xsd/imsvdex_v1p0"

    def __init__(self, context):
        self.context = context

    def importDocument(self, taxonomy, document, clear=False):
        tree = fromstring(document)
        results = ImportVdex(tree, self.IMSVDEX_NS)()

        for language, items in results.items():
            taxonomy.update(language, items, clear)

    def exportDocument(self, taxonomy):
        treestring = ExportVdex(taxonomy)(as_string=True)
        return treestring

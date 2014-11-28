import ConfigParser

from plone.behavior.interfaces import IBehavior

from io import BytesIO
from elementtree import ElementTree

from .interfaces import ITaxonomy
from .factory import registerTaxonomy
from .vdex import ImportVdex, ExportVdex


def parseConfigFile(data):
    try:
        config = ConfigParser.RawConfigParser(allow_no_value=True)
    except TypeError:
        # We are probably on Python < 2.7 that does not support
        # allow_no_value, so we are just forced to do ConfigParsing
        # without allowing empty arguments :(
        config = ConfigParser.RawConfigParser()
    except Exception as exception:
        raise exception

    config.readfp(BytesIO(data))
    return config


def importTaxonomy(context):
    directory = context.listDirectory('taxonomies/')

    if not directory:
        return

    for filename in directory:
        if filename.endswith('.xml'):
            continue

        if filename.endswith('.cfg'):
            data = context.readDataFile('taxonomies/' + filename)
            config = parseConfigFile(data)

            filename = 'taxonomies/' + filename.replace('.cfg', '.xml')
            body = context.readDataFile(filename)
            if body is not None:
                result = {}
                for name in ['name', 'title',
                             'description', 'default_language']:
                    try:
                        result[name] = unicode(config.get('taxonomy', name), 'utf-8')
                    except ConfigParser.NoOptionError:
                        pass

                taxonomy = registerTaxonomy(
                    context,
                    **result
                )
                importer = TaxonomyImportExportAdapter(context)
                importer.importDocument(taxonomy, body)

                result = {}
                for name in ['field_title', 'field_description',
                             'default_language', 'write_permission']:
                    try:
                        result[name] = unicode(config.get('taxonomy', name), 'utf-8')
                    except ConfigParser.NoOptionError:
                        pass

                for name in ['is_single_select', 'is_required']:
                    try:
                        result[name] = config.get('taxonomy', name) == 'true' and True
                    except ConfigParser.NoOptionError:
                        pass

                taxonomy.registerBehavior(**result)


def exportTaxonomy(context):
    site = context.getSite()
    for (name, taxonomy) in site.getSiteManager().getUtilitiesFor(ITaxonomy):
        behavior = site.getSiteManager().queryUtility(
            IBehavior, name=taxonomy.getGeneratedName()
        )

        short_name = name.split('.')[-1]
        exporter = TaxonomyImportExportAdapter(context)
        body = exporter.exportDocument(taxonomy)

        if body is not None:
            config = ConfigParser.RawConfigParser()

            config.add_section('taxonomy')
            name = name.replace('collective.taxonomy.', '')
            config.set('taxonomy', 'name', name)

            for name in ['title', 'description', 'default_language']:
                value = getattr(taxonomy, name, None)
                if value:
                    if type(value) == unicode:
                        config.set('taxonomy', name, value.encode('utf-8'))
                    else:
                        config.set('taxonomy', name, value)

            for name in ['field_title', 'field_description',
                         'write_permission']:
                value = getattr(behavior, name, None)
                if value:
                    if type(value) == unicode:
                        config.set('taxonomy', name, value.encode('utf-8'))
                    else:
                        config.set('taxonomy', name, value)

            for name in ['is_single_select', 'is_required']:
                value = getattr(behavior, name, None)
                if value:
                    config.set('taxonomy', name, str(value).lower())

            filehandle = BytesIO()
            config.write(filehandle)
            context.writeDataFile('taxonomies/' + short_name + '.cfg',
                                  filehandle.getvalue(), 'text/plain')
            context.writeDataFile('taxonomies/' + short_name + '.xml',
                                  body, 'text/xml')


class TaxonomyImportExportAdapter(object):
    IMSVDEX_NS = 'http://www.imsglobal.org/xsd/imsvdex_v1p0'

    def __init__(self, context):
        self.context = context

    def importDocument(self, taxonomy, document):
        # XXX: we should change this

        tree = ElementTree.fromstring(document)
        # taxonomy.clean()

        results = ImportVdex(tree, self.IMSVDEX_NS)()

        for (language, elements) in results.items():
            for (path, identifier) in elements.items():
                taxonomy.add(language, identifier, path)

    def exportDocument(self, taxonomy):
        treestring = ExportVdex(taxonomy)(as_string=True)
        return treestring

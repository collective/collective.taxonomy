from BTrees.IOBTree import IOBTree
from BTrees.OOBTree import OOBTree
from collective.taxonomy import generated
from collective.taxonomy import LEGACY_PATH_SEPARATOR
from collective.taxonomy import NODE
from collective.taxonomy import PATH_SEPARATOR
from collective.taxonomy import PRETTY_PATH_SEPARATOR
from collective.taxonomy.behavior import TaxonomyBehavior
from collective.taxonomy.interfaces import ITaxonomy
from collective.taxonomy.vocabulary import Vocabulary
from copy import copy
from OFS.SimpleItem import SimpleItem
from persistent.dict import PersistentDict
from plone import api
from plone.behavior.interfaces import IBehavior
from plone.dexterity.fti import DexterityFTIModificationDescription
from plone.dexterity.interfaces import IDexterityFTI
from plone.memoize import ram
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.lifecycleevent import modified

import logging


try:
    from plone.protect.auto import safeWrite
except ImportError:
    # plone.protect < 3.x compatibility
    def safeWrite(obj, request):
        pass


logger = logging.getLogger("collective.taxonomy")


def pop_value(d, compare_value, default=None):
    for key, value in d.items():
        if compare_value == value:
            break
    else:
        return default

    return d.pop(key)


@implementer(ITaxonomy)
class Taxonomy(SimpleItem):
    order = None
    count = None
    version = None

    def __init__(self, name, title, default_language):
        self.data = PersistentDict()
        self.order = PersistentDict()
        self.count = PersistentDict()
        self.version = PersistentDict()

        self.name = name
        self.title = title
        self.default_language = default_language

    @property
    def sm(self):
        return api.portal.get().getSiteManager()

    def __call__(self, context):
        if not self.data:
            return Vocabulary(self.name, {}, {}, {}, 2)

        request = getattr(context, "REQUEST", None)
        language = self.getCurrentLanguage(request)
        return self.makeVocabulary(language)

    @property
    @ram.cache(lambda method, self: (self.name, self.data._p_mtime))
    def inverted_data(self):
        inv_data = {}
        for language, elements in self.data.items():
            inv_data[language] = {}
            for path, identifier in elements.items():
                inv_data[language][identifier] = path
        return inv_data

    def getShortName(self):
        return self.name.split(".")[-1]

    def getGeneratedName(self):
        return "collective.taxonomy.generated." + self.getShortName()

    def getVocabularyName(self):
        return "collective.taxonomy." + self.getShortName()

    def makeVocabulary(self, language):
        self._fixup()
        data = self.data.get(language, {})
        order = self.order.get(language)
        version = self.version.get(language, 1)
        inverted_data = self.inverted_data.get(language, {})
        return Vocabulary(self.name, data, inverted_data, order, version)

    def getCurrentLanguage(self, request):
        language = api.portal.get_current_language()
        if language in self.data:
            return language
        elif self.default_language in self.data:
            return self.default_language
        else:
            # our best guess!
            return self.data.keys()[0]

    def getLanguages(self):
        return tuple(self.data)

    def iterLanguage(self, language=None):
        if language is None:
            language = self.default_language

        vocabulary = self.makeVocabulary(language)

        for path, identifier in vocabulary.iterEntries():
            parent_path = path.rsplit(PATH_SEPARATOR, 1)[0]
            if parent_path:
                parent = vocabulary.getTermByValue(parent_path)
            else:
                parent = None
            yield path, identifier, parent

    def registerBehavior(self, **kwargs):
        new_args = copy(kwargs)

        new_args["name"] = self.getGeneratedName()
        new_args["title"] = self.title
        new_args["description"] = kwargs.get("field_description", "")
        new_args["field_description"] = new_args["description"]

        behavior = TaxonomyBehavior(**new_args)
        self.sm.registerUtility(behavior, IBehavior, name=self.getGeneratedName())

        behavior.addIndex()
        behavior.addMetadata()
        behavior.activateSearchable()

    def cleanupFTI(self):
        """Cleanup the FTIs"""
        generated_name = self.getGeneratedName()
        for name, fti in self.sm.getUtilitiesFor(IDexterityFTI):
            if generated_name in fti.behaviors:
                fti.behaviors = [
                    behavior for behavior in fti.behaviors if behavior != generated_name
                ]
            modified(fti, DexterityFTIModificationDescription("behaviors", ""))

    def updateBehavior(self, **kwargs):
        behavior_name = self.getGeneratedName()
        short_name = self.getShortName()

        utility = self.sm.queryUtility(IBehavior, name=behavior_name)
        if utility:
            utility.deactivateSearchable()
            utility.activateSearchable()
            if "field_title" in kwargs:
                utility.title = kwargs.pop("field_title")

            for k, v in kwargs.items():
                setattr(utility, k, v)

        delattr(generated, short_name)

        for name, fti in self.sm.getUtilitiesFor(IDexterityFTI):
            if behavior_name in fti.behaviors:
                modified(fti, DexterityFTIModificationDescription("behaviors", ""))

    def unregisterBehavior(self):
        behavior_name = self.getGeneratedName()
        utility = self.sm.queryUtility(IBehavior, name=behavior_name)

        if utility is None:
            return

        self.cleanupFTI()

        utility.removeIndex()
        utility.deactivateSearchable()
        utility.unregisterInterface()

        self.sm.unregisterUtility(utility, IBehavior, name=behavior_name)

    def clean(self):
        self.data.clear()

    def add(self, language, value, key):
        self._fixup()
        tree = self.data.get(language)
        if tree is None:
            tree = self.data[language] = OOBTree()
        else:
            # Make sure we update the modification time.
            self.data[language] = tree

        update = key in tree
        tree[key] = value

        order = self.order.get(language)
        if order is None:
            order = self.order[language] = IOBTree()
            count = self.count[language] = 0
        else:
            if update:
                pop_value(tree, key)

            count = self.count[language] + 1

        self.count[language] = count
        order[count] = key

    def update(self, language, items, clear=False):
        self._fixup()

        tree = self.data.setdefault(language, OOBTree())
        if clear:
            tree.clear()

        # A new tree always uses the newest version.
        if not tree:
            version = self.version[language] = 2
        else:
            version = self.version.get(language, 1)

        order = self.order.setdefault(language, IOBTree())
        count = self.count.get(language, 0)

        if clear:
            order.clear()
            count = 0

        # Always migrate to newest version.
        if version == 1:

            def fix(path):
                return path.replace(LEGACY_PATH_SEPARATOR, PATH_SEPARATOR)

            for i in list(order):
                path = order[i]
                order[i] = fix(path)

            for path in list(tree):
                value = tree.pop(path)
                tree[fix(path)] = value

            version = self.version[language] = 2
            logger.info(
                "Taxonomy '%s' upgraded to version %d for language '%s'."
                % (self.name, version, language)
            )

        # Make sure we update the modification time.
        self.data[language] = tree

        # The following structure is used to expunge updated entries.
        inv = {}
        if not clear:
            for i, key in order.items():
                inv[key] = i

        seen = set()
        for key, value in items:
            if key in seen:
                logger.warning(f"Duplicate key entry: {key!r}")

            seen.add(key)
            update = key in tree
            tree[key] = value
            order[count] = key
            count += 1

            # If we're updating, then we have to pop out the old ordering
            # information in order to maintain relative ordering of new items.
            if update:
                i = inv.get(key)
                if i is not None:
                    del order[i]

        self.count[language] = count

    def translate(
        self,
        msgid,
        mapping=None,
        context=None,
        target_language=None,
        default=None,
        msgid_plural=None,
        default_plural=None,
        number=None,
    ):
        if target_language is None or target_language not in self.inverted_data:
            target_language = str(api.portal.get_current_language())

            if target_language not in self.inverted_data:
                # might be a non standard language or the portal has
                # switched standard language after creating the taxonomy
                lngs = list(self.inverted_data.keys())
                if not len(lngs):
                    # empty taxonomy
                    return ""
                target_language = lngs[0]

        if msgid not in self.inverted_data[target_language]:
            return ""

        if self.version is not None and self.version.get(target_language) != 2:
            path_sep = LEGACY_PATH_SEPARATOR
        else:
            path_sep = PATH_SEPARATOR

        path = self.inverted_data[target_language][msgid]
        pretty_path = path[1:].replace(path_sep, PRETTY_PATH_SEPARATOR)

        if mapping is not None and mapping.get(NODE):
            pretty_path = pretty_path.rsplit(PRETTY_PATH_SEPARATOR, 1)[-1]

        return pretty_path

    def _fixup(self):
        # due to compatibility reasons this method fixes data structure
        # for old Taxonomy instances.
        # XXX: remove this in version 2.0 to prevent write on read
        if self.order is None:
            safeWrite(self, getRequest())
            self.order = PersistentDict()
            self.count = PersistentDict()

        if self.version is None:
            safeWrite(self, getRequest())
            self.version = PersistentDict()

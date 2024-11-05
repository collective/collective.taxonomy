Changes
=======

3.1.5 (2024-11-05)
------------------

- Add fake former_dotted_names attribute to do not broke versioning when there are some taxonomies behaviors.
  [cekk]


3.1.4 (2024-10-24)
------------------

- Fix collectionfilter modifier when index names ended with the same string.
  [petschki]


3.1.3 (2024-10-17)
------------------

- Fix wrong rendered boolean attribute "multiple" in orderedselect widget
  [1letter]

- refactor JS resources and update README for better developer experience
  [petschki]

3.1.2 (2024-07-21)
------------------

- Fix keywords comparison
  [mamico]

- Added Italian translation
  [mamico]

3.1.1 (2024-05-22)
------------------

- Fix missing plone.app.contentmenu zcml dependency for plone_displayviews menu
  [laulaz]

- Update JS dependencies.
  [petschki]

- config with ``plone/meta``.
  [petschki]

3.1 (2023-05-26)
----------------

- Integrate taxonomies into Collection tabular view, display values are now resolved
  [MrTango]
- Restapi endpoints support [cekk, nileshgulia1]


3.0.1 (2023-02-02)
------------------

- check for the field presence in `TaxonomyIndexerWrapper` more consistent.
  [mamico]

- export/import of field_prefix value.
  [eikichi18]


3.0.0 (2022-12-13)
------------------

- Fix deprecated `collections.Iterable` in `TaxonomyIndexerWrapper`. This got
  removed since python 3.10. Importing `collections.abc.Iterable` now.
  [petschki]

- Add missing `fetch_vocabulary` record for IQueryField
  This was introduced in plone.app.querystring 1.5.0
  [laulaz]

- more markup updates to Bootstrap 5.
  [petschki]

3.0.0a1 (2022-07-13)
--------------------

- Fix configlet icon for Plone 6 (#135)
  [laulaz]

- update markup in `edittaxonomydata.js` to Bootstrap 5
  [petschki]

2.2.2 (2022-07-12)
------------------

- Use new 'Manage taxonomies' permission for taxonomies configlet (#134)
  Permission is by default assigned to Manager and Site Administrator roles.
  [laulaz]

- Fixed 'Required' and 'Single select' option being compulsory [JeffersonBledsoe] (#131)


2.2.1 (2022-03-30)
------------------

- Fix taxonomy data edition when using Gunicorn WSGI (#123)
  [laulaz]
- Implemented possibility to change the IDs. [Petchesi-Iulian] (#113)
- Added constraints to not allow duplicate IDs. [Petchesi-Iulian] (#113)
- Improved the editing interface. [Petchesi-Iulian] (#113)
- Updated the documentation and tutorial. [Petchesi-Iulian] (#113)

2.2.0 (2021-12-13)
------------------

- Refactor import of synchronized decorator [1letter] (#120)


2.1.1 (2021-11-23)
------------------

- Wrap strings in list while indexing to correctly index single-select taxonomies. [adrianschulz] (#108)
- Plone 6 / pip install ready [avoinea] (#114)


2.1.0 (2021-05-27)
------------------

- Fix GenericSetup export in python2
  [gotcha]

- Integrate taxonomies into collective.collectionfilter
  [MrTango]


2.0.1 (2020-07-04)
------------------

- Add a tutorial
  [rodfersou]

- Add Cypress test
  [rodfersou]

- Fix translating msgid when portal language is not found in taxonomy
  [petschki, rodfersou]

- Fix JavaScript in ``input_widget.pt`` which had python comments
  [petschki]

- Add Transifex.net service integration to manage the translation process
  [macagua]

- Added Spanish translation
  [macagua]

- Updated the i18n support
  [macagua]

- Added license documentation of package
  [macagua]


2.0.0 (2019-11-25)
------------------

- add uninstall handler to cleanup persistent utilities and generated behaviors
  [petschki]

- Fix GenericSetup import/export in python3
  [erral]

- Use taxonomy default language for indexing if current language is not available
  [agitator]

- Make generated behaviors language independent
  [agitator]

- export selected taxonomies as zipped folder with XML files
  [petschki]

- Python 3 compatibility
  [petschki, agitator]


1.5.1 (2018-10-25)
------------------

- Fix bug in cachekey generator
  [petschki]


1.5.0 (2018-10-18)
------------------

- Fix controlpanel to show settings navigation
  [petschki]

- Memoize vocabulary lookup
  [tomgross, petschki]

- Fix #53 when editing taxonomy data the first time
  [petschki]

- Update german translations
  [petschki]

- Add uninstall profile
  [petschki]

- When using "delete" option on import, clear any previous ordering.
  [malthe]

- Add support for specifying behavior field prefix.
  [malthe]

- The `getTermByToken` method now accepts an optional argument
  `tail_only` which if set, returns a message object where the title
  translates to the last path segment (the "tail" node).
  [malthe]

- Added new method `makeTree` on taxonomy vocabulary class which
  returns a term tree.
  [malthe]

- Support "slash" character in term title (issue #34).
  [malthe]

- When uploading a taxonomy there is now an option to purge the
  existing entries prior to processing.
  [malthe]

- Taxonomies are now assigned a persistent order. Taxonomies imported
  from VDEX now preserve the ordering of the input document.
  [malthe]

- Add new method `iterEntries` on taxonomy vocabulary class that
  provides a safe way to iterate over the path to identifier mapping
  (in order).
  [malthe]

- Vocabulary is a IVocabularyTokenized implementer.
  [cedricmessiant]

- updateBehavior method can now modify other attributes (and not only `field_title`).
  [cedricmessiant]

- Add explicit dependency on plone.api >= 1.5 which
  the api.portal.get_current_language api was introduced.
  [vincentfretin]

- Add german translation
  [tomgross]

- Mention Plone 5.0 and 5.1 compatibility
  [tkimnguyen]

- Enable choosing what fieldset to use for the behavior fields. Fallback to categorization,
  keeping backwards compatibility.
  [sunew]

- Change to no longer register example *Test*-taxonomy on install
  [datakurre]

- Fix issue where taxonomy indexer adapter was not properly unregistered from
  the persistent local registry on taxonomy removal
  [datakurre]

- Fix issue where public ++taxonomy++short_name -traverser for returning
  generator of (key, label) tuples for given taxonomy was broken
  [datakurre]


1.4.4 (2016-11-29)
------------------

- Fix taxonomy export that was broken since 1.4.0.
  [vincentfretin]


1.4.3 (2016-11-29)
------------------

- Fix save action to work on Plone 5 (by reading portal url from
  body[data-portal-url] and adding X-CSRF-TOKEN for post requests
  [datakurre]

- Fix BehaviorRegistrationNotFound error with Plone 5.0.6
  [tomgross]

- Use lxml instead of elementtree
  [tomgross]

- Rename fontello font to taxonomy to avoid clash with Plone 5 theme
  [vincentfretin]


1.4.2 (2016-11-08)
------------------

- Fix save action in edit-taxonomy-data. This was a regression in 1.4.0, the
  get parameter should be taxonomy, not form.widgets.taxonomy.
  [cedricmessiant]


1.4.1 (2016-11-03)
------------------

- Remove Save and Cancel buttons in controlpanel introduced 1.4.0.
  [vincentfretin]

- Add missing upgrade step to create records in registry.
  [vincentfretin]


1.4.0 (2016-11-03)
------------------

- Getting language by acquisition, indeed some Dexterity content has no language or empty language.
  [bsuttor]

- Fix empty context.REQUEST.get('form.widgets.taxonomy'). It add it into POST form.
  [bsuttor]

- Plone 5 compatibility
  [tomgross]

- Use context language to find index.
  [bsuttor]


1.3.0 (2016-07-07)
------------------

- Fix index when taxonomy is added as field.
  [bsuttor]

- Now uses a React/Redux app to edit taxonomy data. It is now possible to edit
  the data in multiple languages and to compare between languages.
  [cedricmessiant]

- Fix index when taxonomy is added as field.
  [bsuttor]

- Now uses a React/Redux app to edit taxonomy data. It is now possible to edit
  the data in multiple languages and to compare between languages.
  [cedricmessiant]

- Add PATH_SEPARATOR constant to be able to use '/' character in terms.
  [cedricmessiant]

- Add ++taxonomy++[shortname] -traverser to be usable with PloneFormGen
  dynamic field vocabulary overrides
  [datakurre]

- prevent taxonomy reset on reinstall if you've defined a vdex xml file
  in your profile
  [petschki]

- Plone 5 compatibility
  [tomgross]

1.2.3 (2014-02-07)
------------------

- ConfigParser supports allow_no_value on Python 2.6, so we cannot allow empty values,
  only on 2.7 or newer.
  [bosim]

1.2.2 (2014-01-03)
------------------

Bugfix release

- Fixed problem with registration of search criteria in collections, the previous
  registration broke export feature of plone.app.registry. Upgrade step has been
  added so please upgrade.
  [bosim]

1.2.1 (2013-11-12)
------------------

Bugfix release, please upgrade

- Using Schema from plone.supermodel. Fixes issue #6
  [bosim]

- Rewrote behavior creation routine. Fixes issue #5
  [bosim]

1.2 (2013-11-12)
----------------

- Add collective.js.jqueryui as dependency.  Install it automatically.
  [maurits]

- i18n fixes,
  messages extraction script,
  french translation.
  [thomasdesvenain]

- Fixed error in vdex import.
  [thomasdesvenain]

- Avoid failure at export when no default language was selected.
  [thomasdesvenain]

- Remove dependency form plone.directives
  [thomasdesvenain]

- Added elementtree in dependencies
  [thomasdesvenain]

1.1 (2013-07-16)
----------------

- Taxonomies can now be added without uploading a VDEX file.
  [bosim]

- Taxonomies can be exported/imported via GenericSetup again.
  [bosim]

- Single select fields are now possible again.
  [bosim]

1.0 (2013-05-07)
----------------

- Initial release
  [bosim]

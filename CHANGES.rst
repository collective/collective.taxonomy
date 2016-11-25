Changes
=======


1.4.3 (unreleased)
------------------

- Fix save action to work on Plone 5 (by reading portal url from
  body[data-portal-url] and adding X-CSRF-TOKEN for post requets
  [datakurre]


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

- Use lxml instead of elementtree
  [tomgross]


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

- Fixed problem with registration of search citeria in collections, the previous
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

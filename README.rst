Taxonomy Vocabularies
=====================

Create, edit and use hierarchical taxonomies in `Plone`_.

This add-on provides support for hierarchical taxonomies in multiple
languages, letting users easily associate existing content with terms
from one or more taxonomies.

    `Taxonomy <https://en.wikipedia.org/wiki/Taxonomy>`_ is the
    "discipline of defining groups [...] on the basis of shared
    characteristics and giving names to those groups. Each group is
    given a rank and groups of a given rank can be aggregated to form
    a super group of higher rank and thus create a hierarchical
    classification".

Here's an example of the "taxonomic kingdoms of life"::

    Living Organisms
    Living Organisms -> Eukaryotic
    Living Organisms -> Eukaryotic -> Simple multicells or unicells
    Living Organisms -> Eukaryotic -> Multicellular
    Living Organisms -> Eukaryotic -> Multicellular -> Autotrophic
    Living Organisms -> Eukaryotic -> Multicellular -> ...
    Living Organisms -> Prokaryotic
    Living Organisms -> Prokaryotic -> Archaebacteria
    Living Organisms -> Prokaryotic -> Eubacteria
    Living Organisms -> Prokaryotic -> Eubacteria -> ...

Taxonomies can be quite large, sometimes in the tens of thousands
(10,000+). And in sites with multiple languages, each title – or
*caption* – must appear in translation.

Note that the selection of a term in the hierarchy implies the
selection of all its parents. In the example above this means that if
"Eubacteria" is selected, then also "Prokaryotic" and "Living
Organisms" will be.


Overview
========

The implementation tries to meet the following requirements:

#. Support many (10,000+) terms.

#. Terms can be organized in a hierarchical classification.

#. Easily import and export in a common format (VDEX).

#. Taxonomies will provide vocabularies that are translatable.

#. Use behaviors to provide a choice field for each taxonomy.

#. Manage taxonomies and assign to content types "through-the-web".

In the description below, we touch on each of these requirements.


Data structure
--------------

In order to limit both the memory and computation requirements, the
term data is contained in exactly one persistent index per language, a
mapping from the *materialized term path* to its *term identifier*.

The term::

    Living Organisms -> Eukaryotic -> Simple multicells or unicells

will be indexed under this path::

    "Living Organisms/Eukaryotic/Simple multicells or unicells"

The index allows us to provide an iterator over the sorted vocabulary
terms, virtually without cost (as well as containment queries).

At the same time, while the hierarchy is encoded, we can quickly look
up terms in a subtree.

Note: As ``collective.taxonomy`` uses slash as separator, you have to
monkey patch the ``PATH_SEPARATOR`` constant if you want to use '/' in
your terms.


Data exchange
-------------

While ``collective.taxonomy`` (this package) does make it possible to
create, manage and edit taxonomies from a browser-based interface, the
primary focus is to support the exchange of terms in the VDEX format:

    The `IMS Vocabulary Definition Exchange
    <http://www.imsglobal.org/vdex/>`_ (VDEX) specification defines a
    grammar for the exchange of value lists of various classes:
    collections often denoted "vocabulary".

This exchange is integrated with `GenericSetup
<https://pypi.org/project/Products.GenericSetup/>`_ which manages
imports and exports using setup profiles. It is also possible to
use the control panel for importing and exporting VDEX files.

The package comes with integration for the `Dexterity
<https://pypi.org/project/plone.app.dexterity/>`_ content type framework:
for each taxonomy, a *behavior* is available that adds a choice field
which pulls its vocabulary from the taxonomy. The behavior is
configurable in terms of field name, title and whether it allows the
selection of one or more multiple terms.  You should *first* install
dexterity and then ``collective.taxonomy``, otherwise the behaviors
for the existing taxonomies will be missing.


How does it work?
-----------------

The main objective during this project has been to get a high rate
of through-the-Web administration. Therefore the use of the product
will not require any Python programming nor ``configure.zcml`` directives.

In the control panel (``/@@taxonomy-settings``), the user can:

#. Import taxonomies from VDEX files.

#. Export taxonomies existing to VDEX files.

#. Delete taxonomies

#. Add and delete behaviors for taxonomies

When a new behavior is created for a taxonomy, it can easily be added
to the desired content types using the content type control panel, provided
by Dexterity. After this is done, the taxonomy is available on add and edit
forms, and it is also available for collections, if ``plone.app.collection``
is used on the site. An index is also created, so the taxonomies can easily
be used for catalog queries.

Please read the detailed `Getting Started Tutorial <https://github.com/collective/collective.taxonomy/blob/master/docs/tutorial.md>`_


React/Redux app to edit taxonomies
----------------------------------

The view ``@@taxonomy-edit-data`` that allow users to edit the taxonomy data
is a React/Redux app (the source code is in the ``javascripts`` directory.

Here's a preview of this view:

.. image:: https://raw.githubusercontent.com/collective/collective.taxonomy/master/images/edit_taxonomy_data.gif
    :alt: Edit taxonomy data preview

The languages allowed for the taxonomies are the languages defined in ``portal_languages``.


Development
===========

Run the app, run ``npm start`` in the ``javascripts`` directory.
To make Plone use the development code, you need the ``NODE_ENV`` environment
variable to be set to ``development``:

::

    NODE_ENV=development bin/instance fg


i18n
----

The app uses `react-intl <https://github.com/yahoo/react-intl>`_ to handle i18n.
To translate the app, add a new language in the translations directory. For example,
create a ``es`` file in the translations directory that contains:

::

    const es = {
        submitLabel: 'Enviar',
    }

    export default es

Then, edit ``translations/index.js`` to add the language to the translations object:

::

    import es from './es'

    const translations = {
        es,
        fr
    }

You'll have to rebuild the js bundle: ``npm run build``

That's it!


Translations
------------

This product has been translated into

- Danish.

- German.

- French.

- Spanish.

You can contribute for any message missing or other new languages, join us at
`Plone Collective Team <https://www.transifex.com/plone/plone-collective/>`_
into *Transifex.net* service with all world Plone translators community.


Plone Version Compatibility
===========================

collective.taxonomy version `2.x`

* Plone 5.2 (py2/py3)
* Plone 5.1
* Plone 5.0

collective.taxonomy version `1.x`

* Plone 4.3
* or an older version using a recent version of `plone.dexterity <https://pypi.org/project/plone.dexterity/>`_/`plone.app.dexterity <https://pypi.org/project/plone.app.dexterity/>`_


Frequently Asked Questions
==========================

How can I import an existing ``ATVocabularyManager`` vocabulary?

  Use the script provided in this `gist <https://gist.github.com/3826155>`_. Just
  remember to edit the vocabIdentifier and vocabName.


Tests status
============

This add-on is tested using Travis CI. The current status of the add-on is:

.. image:: https://img.shields.io/travis/collective/collective.taxonomy/master.svg
    :alt: Travis CI badge
    :target: https://travis-ci.org/collective/collective.taxonomy

.. image:: https://coveralls.io/repos/collective/collective.taxonomy/badge.png?branch=master
    :alt: Coveralls badge
    :target: https://coveralls.io/r/collective/collective.taxonomy

.. image:: http://img.shields.io/pypi/v/collective.taxonomy.svg
    :target: https://pypi.org/project/collective.taxonomy


Contribute
==========

Have an idea? Found a bug? Let us know by `opening a ticket`_.

- Issue Tracker: https://github.com/collective/collective.taxonomy/issues
- Source Code: https://github.com/collective/collective.taxonomy


Contributors
============

Author
------

- Bo Simonsen <bo@headnet.dk>


Contributors
------------

- Malthe Borch <mborch@gmail.com>

- Thomas Clement Mogensen <thomas@headnet.dk>

- Thomas Desvenain <thomas.desvenain@gmail.com>

- Maurits van Rees <maurits@vanrees.org>

- Cédric Messiant <cedric.messiant@gmail.com>

- Leonardo J. Caballero G. <leonardocaballero@gmail.com>


Existing work
=============

In 2010, Rok Garbas <rok@garbas.si> reimplemented and extended prior
work by `Seantis <http://www.seantis.ch/>`_ and released
`collective.vdexvocabulary
<https://pypi.org/project/collective.vdexvocabulary>`_. This
package allows you to configure and populate vocabulary components
from a VDEX-specification. The package supports flat vocabularies
only, and support for multiple languages takes a different approach
(vocabularies are returned in an already translated form). Note that
vocabularies are loaded in a read-only mode, although it's been
proposed that vocabularies might be edited through-the-web.

In 2005, Jens Klein <jens.klein@bluedynamics.com> released
`ATVocabularyManager
<https://pypi.org/project/Products.ATVocabularyManager/>`_. This package makes
it possible to create taxonomies using Plone's content management
interface with terms existing as regular site content. It's integrated
with the `Archetypes <https://pypi.org/project/Products.Archetypes/>`_ content
type framework (now deprecated).


.. [#] Term relationships are currently not supported.


License
=======

The project is licensed under the GPL v2 or later (GPLv2+).

.. _Plone: https://plone.org/
.. _`opening a ticket`: https://github.com/collective/collective.taxonomy/issues

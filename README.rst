This add-on provides support for hierarchical taxonomies in multiple
languages, letting users easily associate existing content with terms
from one or more taxonomies.

    `Taxonomy <http://en.wikipedia.org/wiki/Taxonomy>`_ is the
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

The package includes an ajax-based form widget (for the `z3c.form
<http://packages.python.org/z3c.form/README.html>`_ library) that
allows the selection of multiple terms at various levels.

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

#. Taxonomies provide the ``IVocabularyFactory`` interface.

#. Taxonomies provide the ``ITranslationDomain`` interface.

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
<http://packages.python.org/Products.GenericSetup/>`_ which manages
imports and exports using setup profiles.

The package comes with integration for the `Dexterity
<http://plone.org/products/dexterity/>`_ content type framework: for
each taxonomy, a *behavior* is available that adds a choice field
which pulls its vocabulary from the taxonomy. The behavior is
configurable in terms of field name, title and whether it allows the
selection of one or more multiple terms.


Components
----------

The standard `zope.schema <http://pypi.python.org/pypi/zope.schema>`_
and `zope.i18n <http://pypi.python.org/pypi/zope.i18n>`_ components
are supported::

  class MySchema(Interface):
      classification = zope.schema.Choice(
          title=_(u"Classification"),
          vocabulary=u"my-classification"
          )

This definition requires a named vocabulary utility
``"my-classification"`` to be registered. Expressed in VDEX, this corresponds to the following XML fragment::

    <vdex xmlns="http://www.imsglobal.org/xsd/imsvdex_v1p0">
        <vocabIdentifier>my-classification</vocabIdentifier>
    </vdex>

The vocabulary terms returned by the utility are translation
messages. The term identifier is encoded into the message id while the
default text is the term caption in the default language.

Existing work
=============

In 2010, Rok Garbas <rok@garbas.si> reimplemented and extended prior
work by `Seantis <http://www.seantis.ch/>`_ and released
`collective.vdexvocabulary
<http://pypi.python.org/pypi/collective.vdexvocabulary>`_. This
package allows you to configure and populate vocabulary components
from a VDEX-specification. The package supports flat vocabularies
only, and support for multiple languages takes a different approach
(vocabularies are returned in an already translated form). Note that
vocabularies are loaded in a read-only mode, although it's been
proposed that vocabularies might be edited through-the-web.

In 2005, Jens Klein <jens.klein@bluedynamics.com> released
`ATVocabularyManager
<http://plone.org/products/atvocabularymanager>`_. This package makes
it possible to create taxonomies using Plone's content management
interface with terms existing as regular site content. It's integrated
with the `Archetypes <http://plone.org/products/archetypes>`_ content
type framework (now deprecated).


.. [#] Term relationships are currently not supported.

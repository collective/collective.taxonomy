This add-on provides support for hierarchical taxonomies in multiple
languages, letting users easily associate existing content with terms
from one or more taxonomies.

    `Taxonomy <http://en.wikipedia.org/wiki/Taxonomy>`_ is the
    "discipline of defining groups [...] on the basis of shared
    characteristics and giving names to those groups. Each group is
    given a rank and groups of a given rank can be aggregated to form
    a super group of higher rank and thus create a hierarchical
    classification". The `IMS Vocabulary Definition Exchange
    <http://www.imsglobal.org/vdex/>`_ (VDEX) specification defines a
    grammar for the exchange of value lists of various classes:
    collections often denoted "vocabulary".

Taxonomies can be created and are edited through a
user interface in Plone's control panel, and can be imported or
exported in VDEX-format.

The package comes with integration for the `Dexterity
<http://plone.org/products/dexterity/>`_ content type framework: for
each taxonomy, a *behavior* is available that adds a choice field
which pulls its vocabulary from the taxonomy. The behavior is
configurable in terms of field name, title and whether it allows the
selection of one or more multiple terms.


Overview
========

This add-on tries to meet the following requirements:

#. Many (10,000+) terms.

#. Terms can be organized in a hierarchical classification.

#. Easily import and export in a common format.

#. Expose vocabularies as persistent ``IVocabularyFactory``
   components.

#. Expose translations as persistent ``ITranslationDomain``
   components.


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

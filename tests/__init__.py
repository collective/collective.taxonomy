"""Tests for collective.taxonomy."""

from collective.taxonomy import PATH_SEPARATOR


#: The taxonomy registered by the ``collective.taxonomy:examples`` profile,
#: which the test layer applies.
TAXONOMY_NAME = "collective.taxonomy.test"

#: Title of :data:`TAXONOMY_NAME`.
TAXONOMY_TITLE = "Test vocabulary"

#: Number of terms per language in :data:`TAXONOMY_NAME`.
TAXONOMY_COUNT = {"da": 4, "de": 1, "en": 6, "ru": 1}

#: Behavior generated for :data:`TAXONOMY_NAME`.
TAXONOMY_BEHAVIOR = "collective.taxonomy.generated.test"

#: Catalog index (and field name) generated for :data:`TAXONOMY_NAME`.
TAXONOMY_INDEX = "taxonomy_test"


def path(*titles: str) -> str:
    """Materialized term path, as the taxonomy stores it."""
    return "".join(f"{PATH_SEPARATOR}{title}" for title in titles)

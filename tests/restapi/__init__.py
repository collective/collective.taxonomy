"""Tests for the @taxonomy and @taxonomySchema services."""

#: Name of the taxonomy the maintenance tests create.
SPACE_NAME = "collective.taxonomy.space"

#: Behavior generated for :data:`SPACE_NAME`.
SPACE_BEHAVIOR = "collective.taxonomy.generated.space"

#: Registry record of the querystring criterion for a taxonomy field.
CRITERION = "plone.app.querystring.field.{}.title"

#: The tree volto-taxonomy sends for :data:`SPACE_NAME`.
SPACE_TREE = [
    {
        "key": "mars",
        "title": "Mars",
        "children": [
            {"key": "mission", "title": "Mission", "children": []},
        ],
    },
    {"key": "venus", "title": "Venus", "children": []},
]

#: Payload creating a taxonomy through ``POST /@taxonomy``.
NEW_TAXONOMY = {
    "taxonomy": "new-taxonomy",
    "field_title": "new taxonomy",
    "default_language": "en",
    "is_required": False,
    "is_single_select": True,
}

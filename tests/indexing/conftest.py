from plone import api
from plone.schemaeditor.utils import FieldAddedEvent
from plone.schemaeditor.utils import FieldRemovedEvent
from plone.schemaeditor.utils import IEditableSchema
from tests import TAXONOMY_INDEX
from zope import schema
from zope.event import notify
from zope.lifecycleevent import ObjectAddedEvent
from zope.lifecycleevent import ObjectRemovedEvent

import pytest


def _taxonomy_field() -> schema.Set:
    return schema.Set(
        title=TAXONOMY_INDEX,
        description="taxonomy description schema",
        required=False,
        value_type=schema.Choice(vocabulary="collective.taxonomy.taxonomies"),
    )


@pytest.fixture
def notify_field_added():
    """Notify that a new taxonomy field was added to the Document schema."""

    def func() -> None:
        field = _taxonomy_field()
        fti = api.portal.get_tool("portal_types").get("Document")
        notify(ObjectAddedEvent(field, fti.lookupSchema()))
        notify(FieldAddedEvent(fti, field))

    return func


@pytest.fixture
def portal(portal):
    """The portal, with a taxonomy field on the Document schema."""
    field = _taxonomy_field()
    fti = api.portal.get_tool("portal_types").get("Document")
    document_schema = fti.lookupSchema()
    editor = IEditableSchema(document_schema)
    editor.addField(field, name=TAXONOMY_INDEX)
    notify(ObjectAddedEvent(field, document_schema))
    notify(FieldAddedEvent(fti, field))
    yield portal
    editor.removeField(TAXONOMY_INDEX)
    notify(ObjectRemovedEvent(field, document_schema))
    notify(FieldRemovedEvent(fti, field))


@pytest.fixture
def document(portal):
    with api.env.adopt_roles(["Manager"]):
        return api.content.create(
            portal, type="Document", id="doc1", title="Doc", language="en"
        )


@pytest.fixture
def folder(portal):
    with api.env.adopt_roles(["Manager"]):
        return api.content.create(
            portal, type="Folder", id="fold1", title="Fold", language="en"
        )


@pytest.fixture
def catalog(portal):
    return api.portal.get_tool("portal_catalog")

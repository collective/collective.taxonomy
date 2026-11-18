import pytest
import transaction


@pytest.fixture
def portal(functional_portal):
    """The functional portal, with its state committed for HTTP requests."""
    transaction.commit()
    return functional_portal

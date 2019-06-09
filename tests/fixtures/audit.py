

import pytest

from tests.base import fake

from api.models import Audit


@pytest.fixture(scope='module')
def audit(app):
    params = {
        "resource_id": 1,
        "resource_type": "Category",
        "action": "Added",
        "activity": "Added from Activo"
    }
    audit = Audit(**params)
    return audit.save()
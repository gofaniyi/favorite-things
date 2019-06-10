

import pytest

from tests.base import fake

from api.models import Audit


@pytest.fixture(scope='module')
def audit(app):
    params = {
        "resource_id": 1,
        "resource_type": "CATEGORY",
        "action": "Added",
        "activity": "Added from App"
    }
    audit = Audit(**params)
    return audit.save()


@pytest.fixture(scope='module')
def categories_audits(app):
    audits = []
    for each in range(1, 4):
        params = {
            "resource_id": each,
            "resource_type": "CATEGORY",
            "action": "Added",
            "activity": "Added from App"
        }
        audit = Audit(**params)
        audits.append(audit.save())
    return audits


@pytest.fixture(scope='module')
def favorites_audits(app):
    audits = []
    for each in range(1, 4):
        params = {
            "resource_id": each,
            "resource_type": "FAVORITE",
            "action": "Added",
            "activity": "Added from App"
        }
        audit = Audit(**params)
        audits.append(audit.save())
    return audits
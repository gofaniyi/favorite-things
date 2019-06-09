

import pytest

from tests.base import fake

from api.models import Category


@pytest.fixture(scope='module')
def category(app):
    params = {
        'name': fake.alphanumeric(),
    }
    category = Category(**params)
    return category.save()


@pytest.fixture(scope='module')
def category1(app):
    params = {
        'name': fake.alphanumeric(),
    }
    category = Category(**params)
    return category.save()

@pytest.fixture(scope='module')
def category2(app):
    params = {
        'name': fake.alphanumeric(),
    }
    category = Category(**params)
    return category.save()

@pytest.fixture(scope='module')
def category3(app):
    params = {
        'name': fake.alphanumeric(),
    }
    category = Category(**params)
    return category.save()

@pytest.fixture(scope='module')
def category4(app):
    params = {
        'name': fake.alphanumeric(),
    }
    category = Category(**params)
    return category.save()

@pytest.fixture(scope='module')
def categories(app):
    categories = []
    for each in range(3):
        params = {
            'name': fake.alphanumeric()
        }
        category = Category(**params)
        categories.append(category.save())
    return categories

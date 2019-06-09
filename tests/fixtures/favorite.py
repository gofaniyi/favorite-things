import pytest

from tests.base import fake

from api.models import Favorite


@pytest.fixture(scope='module')
def favorite(app, category3):
    params = {
        'title' : fake.alphanumeric(15),
        'description' : fake.alphanumeric(200),
        'ranking' : 1,
        'meta_data' : {
            'color' : 'red',
            'quantity' : 2,
            'date_purchased' : '2019-02-05',
            'condition' : 'bad'
        },
        'category_id' : category3.id
    }
    favorite = Favorite(**params)
    return favorite.save()


@pytest.fixture(scope='module')
def favorite1(app, category1):
    params = {
        'title' : fake.alphanumeric(15),
        'description' : fake.alphanumeric(200),
        'ranking' : 2,
        'meta_data' : {
            'color' : 'red',
            'quantity' : 2,
            'date_purchased' : '2019-02-05',
            'condition' : 'bad'
        },
        'category_id' : category1.id
    }
    favorite = Favorite(**params)
    return favorite.save()


@pytest.fixture(scope='module')
def favorites(app, category4):
    favorites = []
    for each in range(3):
        params = {
            'title' : fake.alphanumeric(15),
            'description' : fake.alphanumeric(200),
            'ranking' : 1,
            'meta_data' : {
                'color' : 'red',
                'quantity' : 2,
                'date_purchased' : '2019-02-05',
                'condition' : 'bad'
            },
            'category_id' : category4.id
        }
        favorite = Favorite(**params)
        favorites.append(favorite.save())
    return favorites


@pytest.fixture(scope='module')
def category_with_favorites(app, category2):
    favorites = []
    for each in range(3):
        params = {
            'title' : fake.alphanumeric(15),
            'description' : fake.alphanumeric(200),
            'ranking' : 1,
            'meta_data' : {
                'color' : 'red',
                'quantity' : 2,
                'date_purchased' : '2019-02-05',
                'condition' : 'bad'
            },
            'category_id' : category2.id
        }
        favorite = Favorite(**params)
        favorites.append(favorite.save())
    return category2
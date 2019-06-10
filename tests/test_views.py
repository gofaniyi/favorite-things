"""
Module of tests for company endpoints
"""
from flask import json

# app config
from config import AppConfig

from tests.base import fake

from api.messages import (ERROR_MESSAGES, SUCCESS_MESSAGES)

BASE_URL = AppConfig.API_BASE_URL_V1


class TestCategoryResource:

    def test_get_all_categories_succeeds(
            self, client, init_db, categories):
        """
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            categories (Category): Fixture to create new categories
        """

        response = client.get(
            f'{BASE_URL}/categories')
            
        data = json.loads(response.data.decode())
        assert response.status_code == 200
        assert data['status'] == 'success'
        assert data['message'] == SUCCESS_MESSAGES['FETCHED'].format('Categories')
        assert len(data['data']) > 0


    def test_create_category_with_valid_data_succeeds(
            self, client, init_db):
        """
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
        """
        payload = {
            'name' : fake.alphanumeric(14)
        }

        response = client.post(
            f'{BASE_URL}/categories', 
            data=json.dumps(payload),
            content_type='application/json')
            
        response_json = json.loads(response.data.decode())
        assert response.status_code == 201
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES['CREATED'].format('Category')

        data = response_json['data']
        assert data['name'] == payload['name']


    def test_create_category_with_existing_name_fails(
            self, client, init_db, category):
        """
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            category (Category): Fixture to create a new category
        """

        payload = {
            'name' : category.name
        }

        response = client.post(
            f'{BASE_URL}/categories', 
            data=json.dumps(payload),
            content_type='application/json')

        data = json.loads(response.data.decode())
        assert response.status_code == 409
        assert data['status'] == 'error'
        assert data['message'] == ERROR_MESSAGES['EXISTS'].format('Category')


    def test_create_category_with_missing_name_fails(
            self, client, init_db):
        """
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
        """

        payload = {}

        response = client.post(
            f'{BASE_URL}/categories', 
            data=json.dumps(payload),
            content_type='application/json')

        data = json.loads(response.data.decode())
        assert response.status_code == 400
        assert data['status'] == 'error'
        assert data['message'] == 'An error occurred'
        assert data['errors']['name'] == ['Missing data for required field.']


    def test_create_category_with_empty_name_fails(
            self, client, init_db):
        """
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
        """

        payload = {
            'name' : ''
        }

        response = client.post(
            f'{BASE_URL}/categories', 
            data=json.dumps(payload),
            content_type='application/json')

        data = json.loads(response.data.decode())
        assert response.status_code == 400
        assert data['status'] == 'error'
        assert data['message'] == ERROR_MESSAGES['NOT_FOUND'].format('Name')


    def test_get_all_favorites_under_a_category_succeeds(
            self, client, init_db, category_with_favorites):
        """
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            category_with_favorites (Category): Fixture to create a new category with favorites
        """

        response = client.get(
            f'{BASE_URL}/categories/{category_with_favorites.id}/favorites')

        data = json.loads(response.data.decode())
        
        assert response.status_code == 200
        assert data['status'] == 'success'
        assert data['message'] == SUCCESS_MESSAGES['FETCHED'].format('Favorites')
        assert len(data['data']) > 0
 

class TestSingleCategoryResource:

    def test_update_a_category_with_valid_data_succeeds(
            self, client, init_db, category):
        """
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            category (Category): Fixture to create a new category
        """
        params = {
            'name' : fake.alphanumeric(20),
        }

        response = client.put(
            f'{BASE_URL}/categories/{category.id}', 
            data=json.dumps(params),
            content_type='application/json')

        response_json = json.loads(response.data.decode())
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES['UPDATED'].format('Category')

        data = response_json['data']
        assert data['name'] == params['name']

    def test_update_category_with_existing_name_fails(
            self, client, init_db, category, category1):
        """
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            category (Category): Fixture to create a new category
        """

        payload = {
            'name' : category1.name
        }

        response = client.put(
            f'{BASE_URL}/categories/{category.id}', 
            data=json.dumps(payload),
            content_type='application/json')

        data = json.loads(response.data.decode())
        assert response.status_code == 409
        assert data['status'] == 'error'
        assert data['message'] == ERROR_MESSAGES['EXISTS'].format('Category')


    def test_update_category_without_changes_succeeds(
            self, client, init_db, category):
        """
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            category (Category): Fixture to create a new category
        """

        payload = {
            'name' : category.name
        }

        response = client.put(
            f'{BASE_URL}/categories/{category.id}', 
            data=json.dumps(payload),
            content_type='application/json')
            
        response_json = json.loads(response.data.decode())
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES['UPDATED'].format('Category')

        data = response_json['data']
        assert data['name'] == payload['name']

    def test_delete_a_category_succeeds(
            self, client, init_db, category):
        """
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            category (Favorite): Fixture to create a new category
        """

        response = client.delete(
            f'{BASE_URL}/categories/{category.id}')

        response_json = json.loads(response.data.decode())
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES['DELETED'].format('Category')


    def test_delete_an_invalid_category_succeeds(
            self, client, init_db):
        """
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
        """

        response = client.delete(
            f'{BASE_URL}/categories/1232')
            
        data = json.loads(response.data.decode())
        assert response.status_code == 404
        assert data['status'] == 'error'
        assert data['message'] == ERROR_MESSAGES['NOT_FOUND'].format('Category')


    def test_delete_a_category_with_favorites_fails(
            self, client, init_db, category_with_favorites):
        """
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            category_with_favorites (Category): Fixture to create a new category with favorites
        """

        response = client.delete(
            f'{BASE_URL}/categories/{category_with_favorites.id}')
        
        response_json = json.loads(response.data.decode())
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == ERROR_MESSAGES['DELETING_RELATED_OBJECTS'].format('Category', 'Favorites')

class TestFavoriteResource:

    def test_create_favorite_with_valid_data_succeeds(
            self, client, init_db, category4):
        """
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            category (Category): Fixture to create a new category
        """
        payload = {
            'title' : fake.alphanumeric(10),
            'description' : fake.alphanumeric(200),
            'metaData' : {
                'color' : 'red',
                'quantity': 100,
                'condition' : 'good'
            },
            'ranking' : 3,
            'categoryId' : category4.id
        }

        response = client.post(
            f'{BASE_URL}/favorites', 
            data=json.dumps(payload),
            content_type='application/json')
            
        data = json.loads(response.data.decode())

        assert response.status_code == 201
        assert data['status'] == 'success'
        assert data['message'] == SUCCESS_MESSAGES['CREATED'].format('Favorite')
        assert data['data']['title'] == payload['title']
        assert data['data']['description'] == payload['description']



    def test_create_favorite_with_empty_description_succeeds(
            self, client, init_db, category4):
        """
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            category (Category): Fixture to create a new category
        """

        payload = {
            'title' : fake.alphanumeric(10),
            'metaData' : {
                'quantity': 100,
                'condition' : 'good'
            },
            'ranking' : 2,
            'categoryId' : category4.id
        }

        response = client.post(
            f'{BASE_URL}/favorites', 
            data=json.dumps(payload),
            content_type='application/json')

        data = json.loads(response.data.decode())

        assert response.status_code == 201
        assert data['status'] == 'success'
        assert data['message'] == SUCCESS_MESSAGES['CREATED'].format('Favorite')
        assert data['data']['title'] == payload['title']
        assert data['data']['description'] == None
        assert data['data']['ranking'] == payload['ranking']
        assert data['data']['metaData'] == payload['metaData']


    def test_create_favorite_with_missing_title_fails(
            self, client, init_db, category):
        """
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            category (Category): Fixture to create a new category
        """

        payload = {
            'description' : fake.alphanumeric(20),
            'ranking' :  3,
            'metaData' : {
                'color' : 'black',
                'quantity' : 20
            },
            'categoryId' : category.id
        }

        response = client.post(
            f'{BASE_URL}/favorites', 
            data=json.dumps(payload),
            content_type='application/json')

        data = json.loads(response.data.decode())
        assert response.status_code == 400
        assert data['status'] == 'error'
        assert data['message'] == 'An error occurred'
        assert data['errors']['title'] == ['Missing data for required field.']


    def test_create_favorite_with_missing_ranking_fails(
            self, client, init_db, category):
        """
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            category (Category): Fixture to create a new category
        """

        payload = {
            'title' : fake.alphanumeric(10),
            'description' : fake.alphanumeric(20),
            'metaData' : {
                'color' : 'black',
                'quantity' : 20
            },
            'categoryId' : category.id
        }

        response = client.post(
            f'{BASE_URL}/favorites', 
            data=json.dumps(payload),
            content_type='application/json')

        data = json.loads(response.data.decode())
        assert response.status_code == 400
        assert data['status'] == 'error'
        assert data['message'] == 'An error occurred'
        assert data['errors']['ranking'] == ['Missing data for required field.']


    def test_create_favorite_with_missing_category_fails(
            self, client, init_db):
        """
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
        """

        payload = {
            'title' : fake.alphanumeric(10),
            'description' : fake.alphanumeric(20),
            'metaData' : {
                'color' : 'black',
                'quantity' : 20
            },
            'ranking' : 2
        }

        response = client.post(
            f'{BASE_URL}/favorites', 
            data=json.dumps(payload),
            content_type='application/json')

        data = json.loads(response.data.decode())
        assert response.status_code == 400
        assert data['status'] == 'error'
        assert data['message'] == 'An error occurred'
        assert data['errors']['categoryId'] == ['Missing data for required field.']


    def test_create_favorite_with_invalid_category_fails(
            self, client, init_db):
        """
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
        """

        payload = {
            'title' : fake.alphanumeric(10),
            'description' : fake.alphanumeric(20),
            'metaData' : {
                'color' : 'black',
                'quantity' : 20
            },
            'ranking' : 2,
            'categoryId' : 2121
        }

        response = client.post(
            f'{BASE_URL}/favorites', 
            data=json.dumps(payload),
            content_type='application/json')

        data = json.loads(response.data.decode())

        assert response.status_code == 400
        assert data['status'] == 'error'
        assert data['message'] == 'An error occurred'
        assert data['errors']['categoryId'] == [ERROR_MESSAGES['NOT_FOUND_IDENTIFIER'].format('category')]

    def test_create_favorite_with_incomplete_description_fails(
            self, client, init_db, category):
        """
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            category (Category): Fixture to create a new category
        """

        payload = {
            'title' : fake.alphanumeric(10),
            'description' : fake.alphanumeric(4), #Description is less than 10
            'ranking' :  3,
            'metaData' : {
                'color' : 'black',
                'quantity' : 20
            },
            'categoryId' : category.id
        }

        response = client.post(
            f'{BASE_URL}/favorites', 
            data=json.dumps(payload),
            content_type='application/json')

        data = json.loads(response.data.decode())

        assert response.status_code == 400
        assert data['status'] == 'error'
        assert data['message'] == 'An error occurred'
        assert data['errors']['description'][0] == ERROR_MESSAGES['STRING_LENGTH'].format(10)


    def test_get_all_favorites_succeeds(
            self, client, init_db, favorites):
        """
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            favorites (Favorite): Fixture to create a new favorites
        """

        response = client.get(
            f'{BASE_URL}/favorites')

        data = json.loads(response.data.decode())
        assert response.status_code == 200
        assert data['status'] == 'success'
        assert data['message'] == SUCCESS_MESSAGES['FETCHED'].format('Favorites')
        assert len(data['data']) > 0


class TestSingleFavoriteResource:

    def test_get_a_favorite_invalid_id_fails(
            self, client, init_db):
        """
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
        """

        response = client.get(
            f'{BASE_URL}/favorites/2212910')

        data = json.loads(response.data.decode())
        assert response.status_code == 404
        assert data['status'] == 'error'
        assert data['message'] == ERROR_MESSAGES['NOT_FOUND'].format('Favorite')


    def test_get_a_favorite_succeeds(
            self, client, init_db, favorite):
        """
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            favorite (Favorite): Fixture to create a new favorite
        """

        response = client.get(
            f'{BASE_URL}/favorites/{favorite.id}')
            
        response_json = json.loads(response.data.decode())
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES['FETCHED'].format('Favorite')
        data = response_json['data']
        assert data['title'] == favorite.title
        assert data['id'] == favorite.id
        assert data['description'] == favorite.description


    def test_update_a_favorite_with_valid_data_succeeds(
            self, client, init_db, favorite):
        """
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            favorite (Favorite): Fixture to create a new favorite
        """
        params = {
            'ranking' : 2,
            'metaData' : {
                'color' : 'green',
                'quantity' : 2,
                'date_purchased' : '2019-02-05',
                'condition' : 'bad'
            },
        }

        response = client.put(
            f'{BASE_URL}/favorites/{favorite.id}', 
            data=json.dumps(params),
            content_type='application/json')

        response_json = json.loads(response.data.decode())
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES['UPDATED'].format('Favorite')

        data = response_json['data']
        assert data['title'] == favorite.title
        assert data['ranking'] == params['ranking']
        assert data['metaData']['color'] == params['metaData']['color']


    def test_delete_a_favorite_succeeds(
            self, client, init_db, favorite):
        """
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            favorite (Favorite): Fixture to create a new favorite
        """

        response = client.delete(
            f'{BASE_URL}/favorites/{favorite.id}')
            
        response_json = json.loads(response.data.decode())
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES['DELETED'].format('Favorite')


    def test_delete_an_invalid_favorite_succeeds(
            self, client, init_db):
        """
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
        """

        response = client.delete(
            f'{BASE_URL}/favorites/1232')
            
        data = json.loads(response.data.decode())
        assert response.status_code == 404
        assert data['status'] == 'error'
        assert data['message'] == ERROR_MESSAGES['NOT_FOUND'].format('Favorite')


class TestAuditCategoryResource:

    def test_get_all_categories_audits_succeeds(
            self, client, init_db, categories_audits):
        """
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            categories_audits (Audit): Fixture to create new categories' audits
        """

        response = client.get(
            f'{BASE_URL}/categories/audits')
            
        data = json.loads(response.data.decode())
        assert response.status_code == 200
        assert data['status'] == 'success'
        assert data['message'] == SUCCESS_MESSAGES['FETCHED'].format('Audits')
        assert len(data['data']) > 0


class TestAuditFavoriteResource:

    def test_get_all_favorites_audits_succeeds(
            self, client, init_db, favorites_audits):
        """
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            favorites_audits (Audit): Fixture to create new favorites' audits
        """

        response = client.get(
            f'{BASE_URL}/favorites/audits')
            
        data = json.loads(response.data.decode())
        assert response.status_code == 200
        assert data['status'] == 'success'
        assert data['message'] == SUCCESS_MESSAGES['FETCHED'].format('Audits')
        assert len(data['data']) > 0
"""Module with application entry point."""

# Third party Imports
import sys, click
import requests
from os import environ

import click
from flask import jsonify, render_template, g, request
from sqlalchemy import text

# Local Imports
from main import create_app
from config import config, AppConfig
from api.database import db

# create application object
app = create_app(AppConfig)



@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def redirect_all(path):
    if AppConfig.DEBUG:
        return requests.get('http://localhost:8081/{}'.format(path)).text
    return render_template("index.html")

@app.route('/health')
def health_check():
    """Checks the health of application and returns 'Health App Server' as json."""
    return jsonify(dict(message='Healthy App Server')), 200

@app.cli.command(context_settings=dict(token_normalize_func=str.lower))
def seed():
    """
    Seeds the database with sample data

    Return:
        func: call the function if successful or the click help option if unsuccesful
    """
    print('Seeding data')

    categories_data = [
        {'name' : 'Food', 'favorites' : [
            {
                'title' : 'Rice',
                'description' : 'This is a local food for us all to eat',
                'ranking': 1,
                'meta_data' : {
                    'origin' : 'Lagos',
                    'quantity' : 20
                }
            },
            {
                'title' : 'Beans',
                'description' : 'This is a internation food for us all to eat',
                'ranking': 2,
                'meta_data' : {
                    'origin' : 'Abuja',
                    'quantity' : 2
                }
            },
        ]},
        {'name' : 'Dress', 'favorites' : [
            {
                'title' : 'Nike',
                'description' : 'This is a designers clothes',
                'ranking': 1,
                'meta_data' : {
                    'origin' : 'New York',
                    'quantity' : 2
                }
            },
            {
                'title' : 'Dolce',
                'description' : 'This is a brand for all',
                'ranking': 2,
                'meta_data' : {
                    'origin' : 'Los Angeles',
                    'quantity' : 4
                }
            },
            {
                'title' : 'Fardd',
                'description' : 'This is a brand for single people',
                'ranking': 3,
                'meta_data' : {
                    'origin' : 'Malawi',
                    'quantity' : 40
                }
            },
        ]}
    ]

    for category_data in categories_data:
        create_entry(category_data)

    print('Seeded data')


def create_entry(category_data):
    from api.models import Category, Favorite
    
    try:
        category = Category(name=category_data['name'])
        category.save()

        for each in category_data.get('favorites', []):
            favorite = Favorite(**dict(**each, category_id=category.id))
            favorite.save()
    except Exception as e:
        print(e)
        pass

if __name__ == '__main__':
    app.run()

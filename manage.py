"""Module with application entry point."""

# Third party Imports
import sys, click
import requests, flask_s3
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
        {'name' : 'Person', 'favorites' : [
            {
                'title' : 'Shem Michael',
                'description' : 'He is a very good friend that helped me in high school with my project',
                'ranking' : 1,
                'meta_data' : {
                    'race' : 'African',
                    'age' : 29,
                    'residence' : 'Houston, USA'
                }
            }
        ]},
        {'name' : 'Place', 'favorites' : [
            {
                'title' : 'Pentagon House',
                'description' : 'This is a tourist attraction site and a place for everyone to have fun',
                'ranking' : 1,
                'meta_data' : {
                    'country' : 'United States of America',
                    'state' : 'Washington',
                    'floors' : 20
                }
            }
        ]},
        {'name' : 'Food', 'favorites' : [
            {
                'title' : 'Pancake',
                'description' : 'This is a lovely dessert you can enjoy for breakfast',
                'ranking' : 1,
                'meta_data' : {
                    'flavors' : ['chocolate', 'vanilla'],
                    'cooking' : 2
                }
            }
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

@app.cli.command(context_settings=dict(token_normalize_func=str.lower))
def upload():
    """
    upload static files to s3

    Return:
        func: call the function if successful or the click help option if unsuccesful
    """
    print('Uploading static files to S3....')

    flask_s3.create_all(app)

    print('Uploaded static files to S3.....')

if __name__ == '__main__':
    app.run()

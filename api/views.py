"""Module for users resource"""
# Third-party libraries
from flask_restplus import Resource
from flask import request, jsonify

# Middlewares
from main import api
# Models
from .models import Category, Favorite, Audit
from .schemas import CategorySchema, FavoriteSchema, AuditSchema

from .messages import SUCCESS_MESSAGES


@api.route('/categories')
class CategoryResource(Resource):
    """Resource class for category"""

    def get(self):
        """
        Gets categories list
        """
        categories = Category.query

        category_schema = CategorySchema(many=True)

        return (
            {
                "data": category_schema.dump(categories).data,
                "message": SUCCESS_MESSAGES["FETCHED"].format("Categories"),
                "status": "success",
            },
            200,
        )

    def post(self):
        """
        POST method for creating categories.

        """
        request_data = request.get_json()

        category_schema = CategorySchema()
        category_data = category_schema.load_object_into_schema(
            request_data)

        category = Category(**category_data)

        category = category.save()

        return {
            'status': 'success',
            'message': SUCCESS_MESSAGES['CREATED'].format('Category'),
            'data' : category_schema.dump(category).data
        }, 201


@api.route('/categories/audits')
class AuditCategoryResource(Resource):
    """Resource class for category"""

    def get(self):
        """
        Gets audits list for all categories
        """

        audits = Audit.filter(resource_type='CATEGORY')

        audit_schema = AuditSchema(many=True)

        return (
            {
                "data": audit_schema.dump(audits).data,
                "message": SUCCESS_MESSAGES["FETCHED"].format("Audits"),
                "status": "success",
            },
            200,
        )

@api.route('/categories/<int:category_id>')
class SingleFavoriteResource(Resource):
    """Resource class for carrying out operations on a single category"""


    def put(self, category_id):
        """
        Updates category
        """

        category = Category.get_or_404(category_id)

        request_data = request.get_json()
        
        request_data['id'] = category.id

        category_schema = CategorySchema()
        category_data = category_schema.load_object_into_schema(
            request_data, partial=True)

        category.update(**category_data)

        response = jsonify({
            "status": 'success',
            "message": SUCCESS_MESSAGES['UPDATED'].format('Category'),
            "data": category_schema.dump(category).data
        })

        response.status_code = 200
        return response

    def delete(self, category_id):
        """
        Delete a single category
        """
        category = Category.get_or_404(category_id)

        category.delete()

        return (
            {
                "message": SUCCESS_MESSAGES["DELETED"].format("Category"),
                "status": "success",
            },
            200,
        )


@api.route('/categories/<int:category_id>/favorites')
class SingleCategoryFavoritesResource(Resource):
    """Resource class for carrying out operations on a single category"""

    def get(self, category_id):
        """
        Get a single category favorites
        """
        category = Category.get_or_404(category_id)

        favorites = category.favorites.all()

        favorite_schema = FavoriteSchema(many=True)

        return (
            {
                "data": favorite_schema.dump(favorites).data,
                "message": SUCCESS_MESSAGES["FETCHED"].format("Favorites"),
                "status": "success",
            },
            200,
        )

@api.route("/favorites")
class FavoriteResource(Resource):
    """
    Resource class for creating and getting favorites
    """

    def post(self):
        """
        POST method for creating favorites.

        Payload should have the following parameters:
            name(str): name of the risk-type
        """
        request_data = request.get_json()

        favorite_schema = FavoriteSchema()

        favorite_data = favorite_schema.load_object_into_schema(
            request_data)

        favorite = Favorite(**favorite_data)

        favorite = favorite.save()

        return {
            'status': 'success',
            'message': SUCCESS_MESSAGES['CREATED'].format('Favorite'),
            'data' : favorite_schema.dump(favorite).data
        }, 201

    def get(self):
        """
        Gets list of favorites
        """
        favorites = Favorite.query

        favorite_schema = FavoriteSchema(many=True)

        return (
            {
                "data": favorite_schema.dump(favorites).data,
                "message": SUCCESS_MESSAGES["FETCHED"].format("Favorites"),
                "status": "success",
            },
            200,
        )


@api.route('/favorites/audits')
class AuditCategoryResource(Resource):
    """Resource class for category"""

    def get(self):
        """
        Gets audits list for all favorites
        """
        
        audits = Audit.filter(resource_type='FAVORITE')

        audit_schema = AuditSchema(many=True)

        return (
            {
                "data": audit_schema.dump(audits).data,
                "message": SUCCESS_MESSAGES["FETCHED"].format("Audits"),
                "status": "success",
            },
            200,
        )



@api.route('/favorites/<int:favorite_id>')
class SingleFavoriteResource(Resource):
    """Resource class for carrying out operations on a single favorite"""

    def get(self, favorite_id):
        """
        Get a single favorite
        """
        favorite = Favorite.get_or_404(favorite_id)

        return (
            {
                "data": FavoriteSchema().dump(favorite).data,
                "message": SUCCESS_MESSAGES["FETCHED"].format("Favorite"),
                "status": "success",
            },
            200,
        )

    def delete(self, favorite_id):
        """
        Delete a single favorite
        """
        risk_type = Favorite.get_or_404(favorite_id)

        risk_type.delete()

        return (
            {
                "message": SUCCESS_MESSAGES["DELETED"].format("Favorite"),
                "status": "success",
            },
            200,
        )

    def put(self, favorite_id):
        """
        Updates favorite
        """
        favorite = Favorite.get_or_404(favorite_id)

        request_data = request.get_json()
        
        request_data['id'] = favorite.id

        favorite_schema = FavoriteSchema()
        favorite_data = favorite_schema.load_object_into_schema(
            request_data, partial=True)

        favorite.update(**favorite_data)

        response = jsonify({
            "status": 'success',
            "message": SUCCESS_MESSAGES['UPDATED'].format('Favorite'),
            "data": favorite_schema.dump(favorite).data
        })

        response.status_code = 200
        return response
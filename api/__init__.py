from flask import Blueprint
from .models import Category
from .schemas import CategorySchema

api_blueprint = Blueprint('api_blueprint', __name__, url_prefix='/api/v1')

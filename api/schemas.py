""" Module with user model schemas. """

# Third Party
from marshmallow import (Schema, fields, post_load)
from marshmallow import ValidationError as MarshValidationError

from exception.validation import ValidationError

from .messages import ERROR_MESSAGES

from api.models import Category, Favorite


class BaseSchema(Schema):
    """Base marshmallow schema with common attributes."""
    
    id = fields.Integer(dump_only=True)

    created_date = fields.DateTime(dump_only=True, dump_to='createdDate')
    modified_date = fields.DateTime(dump_only=True, dump_to='modifiedDate')


    def load_object_into_schema(self, data, partial=False):
        """Helper function to load python objects into schema"""

        data, errors = self.load(data, partial=partial)

        BaseSchema.raise_errors(errors)

        return data

    @staticmethod
    def raise_errors(errors):
        if errors:
            raise ValidationError(
                dict(errors=errors, message=ERROR_MESSAGES['DEFAULT']), 400)


def common_args(**kwargs):
    """ Returns the common arguments used in marshmallow fields.
    Args:
        kwargs: key word arguments use in fields
        ie validate=some_function

    Returns:
        dict: Resultant fields to be passed to a schema

    """

    return {
        "required": True,
        "validate": kwargs.get('validate'),
        "error_messages": {
            'required': ERROR_MESSAGES['REQUIRED_FIELD'],
        }
    }


def validate_duplicate(model, error_key, obj, **kwargs):
    validate(model, error_key, obj, 409, **kwargs)


def validate_category_exist(value):
    category = Category.get(value)
    raise_error('NOT_FOUND_IDENTIFIER', 'category', fields=['categoryId']) if not category else None

def validate(model, *args, **kwargs):
    error_key, obj, status_code = args
    instance = model.filter(**kwargs).first()
    if instance:
        raise ValidationError(
        {
            'message': ERROR_MESSAGES[error_key].format(obj)
        }, status_code)

def raise_error(error_key, *args, **kwargs):
    """Raises a Marshmallow validation error

    Args:
        error_key (str): The key for accessing the correct error message
        *args: Arguments taken by the serialization error message
        **kwargs:
            fields (list): The fields where the error will appear

    Raises:
        ValidationError: Marshmallow validation error
    """
    raise MarshValidationError(ERROR_MESSAGES[error_key].format(*args),
                           kwargs.get('fields'))



def description_validator(value):
    if value and len(value) < 10:
        raise_error('STRING_LENGTH', 10, fields=value)

class CategorySchema(BaseSchema):
    """ Category model schema. """

    id = fields.Integer()

    name = fields.String(required=True)

    favorites_count = fields.Integer(dump_to='favoritesCount', dump_only=True)

    rankings = fields.Dict(dump_to='rankings', dump_only=True)

    @post_load
    def is_valid(self, data):
        """
        Ensure id fields reference existing resource
        and name supplied is not owned by an exising category

        Arguments:
            data (dict): request body

        Raises:
            ValidationError: Used to raise exception if request body is empty
        """
        if not data.get('name'):
            raise ValidationError(
            {
                'message': ERROR_MESSAGES['NOT_FOUND'].format('Name')
            }, 400)
        if data.get('id'):
            category = Category.get(data.get('id'))
            if category.name == data.get('name'):
                return

        validate_duplicate(Category, 'EXISTS', 'Category', name=data.get('name'))
    

class FavoriteSchema(BaseSchema):
    """Favorite model schema"""

    title = fields.String(required=True)

    description = fields.String(validate=[description_validator])

    ranking = fields.Integer(required=True)

    meta_data = fields.Dict(
        load_from="metaData", dump_to="metaData")

    category_id = fields.Integer(
        load_only=True,
        load_from="categoryId",
        **common_args(validate=[validate_category_exist]))

    category = fields.Nested(
        CategorySchema,
        only=[
            'id', 'name',
        ],
        dump_only=True,
        dump_to="category")


class AuditSchema(BaseSchema):
    """ Audit model schema. """

    resource_id = fields.Integer(dump_only=True)
    resource_type = fields.String(dump_only=True)
    action = fields.String(dump_only=True)
    activity = fields.String(dump_only=True)
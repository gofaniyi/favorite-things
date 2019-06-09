"""Test model user module"""
from pytest import raises

# Local Modules
from api.models import Category, Audit, Favorite

from tests.base import fake

class TestCategoryModel:
    """Test category model
    """

    def test_save(self, init_db):
        """Test for creating a new company
        
            Args:
                init_db(SQLAlchemy): fixture to initialize the test database
        """
        params = {
            'name': fake.alphanumeric(15)
        }
        category = Category(**params)
        assert category == category.save()

    def test_get(self, init_db, category):
        """Test for get method
        
            Args:
                init_db(SQLAlchemy): fixture to initialize the test database
                category (Category): Fixture to create a new category
        """
        assert Category.get(category.id) == category

    def test_update(self, init_db, category):
        """Test for update method
        
            Args:
                init_db(SQLAlchemy): fixture to initialize the test database
                category (Category): Fixture to create a new category
        """
        category_name = fake.alphanumeric()
        category.update(name=category_name)
        assert category.name == category_name

    def test_delete(self, init_db, category):
        """Test for delete method
        
            Args:
                init_db(SQLAlchemy): fixture to initialize the test database
                category (Category): Fixture to create a new category
        """
        category.delete()
        assert Category.get(category.id) == None

    def test_model_string_representation(self, init_db, category):
        """ Should compute the string representation of a category

            Args:
                init_db(SQLAlchemy): fixture to initialize the test database
                category (Category): Fixture to create a new category
        """
        assert repr(category) == f'<Category: {category.name}>'


    def test_child_relationships(self, init_db, category_with_favorites):
        """ Test child relationships of audit

            Args:
                init_db(SQLAlchemy): fixture to initialize the test database
                category_with_favorites (Category): Fixture to create a new category with favorites
        """

        category = Category.get(id=category_with_favorites.id)
        assert category.get_child_relationships() is not None
        assert len(category.favorites.all()) > 0

class TestAuditModel:
    """Test audit model
    """

    def test_save(self, init_db):
        """Test creating new audit

        Args:
            init_db (SQLAlchemy): fixture to initialize the test database
        """
        params = {
                "resource_id": 1,
                "resource_type": "Category",
                "action": "Added",
                "activity": "Added from Activo"
            }

        audit = Audit(**params)
        assert audit == audit.save()

    def test_get(self, init_db, audit):
        """Test for get method
        
            Args:
                init_db(SQLAlchemy): fixture to initialize the test database
                audit (Audit): Fixture to create a new audit
        """
        assert Audit.get(audit.id) == audit

    def test_update(self, init_db, audit):
        """Test for update method
        
            Args:
                init_db(SQLAlchemy): fixture to initialize the test database
                audit (Audit): Fixture to create a new audit
        """
        params = {
            "resource_type": "Category",
            "action": "Updated",
            "activity": "changed name"
        }
        audit.update(**params)
        assert audit.resource_type == params['resource_type']
        assert audit.action == params['action']
        assert audit.activity == params['activity']


    def test_delete(self, init_db, audit):
        """Test for delete method
        
            Args:
                init_db(SQLAlchemy): fixture to initialize the test database
                audit (Audit): Fixture to create a new audit
        """
        audit.delete()
        assert Audit.get(audit.id) == None


    def test_model_string_representation(self, init_db, audit):
        """ Should compute the string representation of a audit

            Args:
                init_db(SQLAlchemy): fixture to initialize the test database
                audit (Audit): Fixture to create a new audit
        """
        assert repr(audit) == f'<Audit on {audit.resource_type}>'

    def test_child_relationships(self, init_db, audit):
        """ Test child relationships of audit

            Args:
                init_db(SQLAlchemy): fixture to initialize the test database
                audit (Audit): Fixture to create a new audit
        """
        audit = Audit.query.first()
        assert audit.get_child_relationships() is None


    


class TestFavoriteModel:
    """Test favorite model
    """

    def test_save(self, init_db, category1):
        """Test creating new favorite

        Args:
            init_db (SQLAlchemy): fixture to initialize the test database
            category (Category): Fixture to create a new category
        """
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
            'category_id' : category1.id
        }

        favorite = Favorite(**params)
        assert favorite == favorite.save()

    def test_get(self, init_db, favorite):
        """Test for get method
        
            Args:
                init_db(SQLAlchemy): fixture to initialize the test database
                favorite (Favorite): Fixture to create a new favorite
        """
        assert Favorite.get(favorite.id) == favorite

    def test_update(self, init_db, favorite):
        """Test for update method
        
            Args:
                init_db(SQLAlchemy): fixture to initialize the test database
                favorite (Favorite): Fixture to create a new favorite
        """
        params = {
            "title": "Category",
            "description": fake.alphanumeric(100),
        }
        favorite.update(**params)
        assert favorite.title == params['title']
        assert favorite.description == params['description']


    def test_delete(self, init_db, favorite):
        """Test for delete method
        
            Args:
                init_db(SQLAlchemy): fixture to initialize the test database
                favorite (Favorite): Fixture to create a new favorite
        """
        favorite.delete()
        assert Favorite.get(favorite.id) == None


    def test_model_string_representation(self, init_db, favorite):
        """ Should compute the string representation of a favorite

            Args:
                init_db(SQLAlchemy): fixture to initialize the test database
                favorite (Favorite): Fixture to create a new favorite
        """
        assert repr(favorite) == f'<Favorite: {favorite.title}>'


    def test_child_relationships(self, init_db, favorite1):
        """ Test unimplemented child relationships of favorite

            Args:
                init_db(SQLAlchemy): fixture to initialize the test database
                favorite (Favorite): Fixture to create a new favorite
        """

        favorite = Favorite.get(id=favorite1.id)

        with raises(NotImplementedError) as error:
            favorite.get_child_relationships()
        
        assert  str(error.value) == "The get_relationships method must be overridden in all child model classes"
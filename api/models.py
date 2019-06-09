"""Module for Company model."""

# Database
from sqlalchemy import text
from api.database import db
from datetime import datetime as dt
from sqlalchemy.dialects.mysql import JSON
import re
from exception.validation import ValidationError
from .messages import ERROR_MESSAGES


class BaseModel(db.Model):
    """Mixin class with generic model operations."""

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_date = db.Column(db.DateTime, default=dt.utcnow)
    modified_date = db.Column(db.DateTime, onupdate=dt.utcnow)

    def save(self):
        """
        Save a model instance
        """
        db.session.add(self)
        db.session.commit()
        return self

    def update(self, **kwargs):
        """
        update entries
        """
        for field, value in kwargs.items():
            setattr(self, field, value)

        db.session.commit()
        return self


    @classmethod
    def get(cls, id):
        """
        return entries by id
        """
        return cls.query.filter_by(id=id).first()


    @classmethod
    def filter(cls, **kwargs):
        """
        return entries 
        """
        return cls.query.filter_by(**kwargs)


    @classmethod
    def get_or_404(cls, id):
        """
        return entries by id
        """

        record = cls.get(id)

        if not record:
            raise ValidationError(
                {
                    'message':
                    f'{re.sub(r"(?<=[a-z])[A-Z]+",lambda x: f" {x.group(0).lower()}" , (cls.__name__))} not found'
                },
                404)

        return record

    def get_child_relationships(self):
        """
        Method to get all child relationships a model has.
        This is used to ascertain if a model has relationship(s) or
        not when validating delete operation.
        It must be overridden in subclasses and takes no argument.
        :return None if there are no child relationships.
        A tuple of all child relationships eg (self.relationship_field1,
        self.relationship_field2)
        """
        raise NotImplementedError(
            "The get_relationships method must be overridden in all child model classes"
        )  #noqa


    def delete(self):
        """
        Delete a model instance.
        """
        db.session.delete(self)
        db.session.commit()
        return True

class Category(BaseModel):
    """Class for categories db table."""

    __tablename__ = 'categories'

    name = db.Column(db.String(255), unique=True, nullable=False)

    favorites = db.relationship(
        'Favorite',
        backref='category',
        cascade='save-update, delete',
        lazy='dynamic')

    @property
    def favorites_count(self):
        return self.favorites.count()

    
    @property
    def rankings(self):
        next_rank = self.favorites_count + 2
        rankings = list(range(1, next_rank))
        ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])
        return [dict(id=each, name=ordinal(each))for each in rankings]

    def get_child_relationships(self):
        return (self.favorites, )

    def __repr__(self):
        return f'<Category: {self.name}>'


    def delete(self):
        """ Delete a Category """
        
        if self.favorites.count() > 0:
            raise ValidationError(
            {
                'message': ERROR_MESSAGES['DELETING_RELATED_OBJECTS'].format('Category', 'Favorites'),
            }, 400)
            
        return super(Category, self).delete()


class Audit(BaseModel):
    """ Model for audit logs.
        Tracks all changes on different resources.
    """
    resource_id = db.Column(db.String(60), index=True, nullable=False)
    resource_type = db.Column(db.String(60), index=True, nullable=False)
    action = db.Column(db.String(60), index=True, nullable=False)
    activity = db.Column(db.Text(), nullable=False)

    def get_child_relationships(self):
        """Method to get all child relationships of this model

        Returns:
            None
        """
        return None

    def __repr__(self):
        return f'<Audit on {self.resource_type}>'


class Favorite(BaseModel):
    """Class for favorites db table."""

    __tablename__ = 'favorites'

    title = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    ranking = db.Column(db.Integer, nullable=False)
    category_id = db.Column(
        db.Integer, db.ForeignKey('categories.id'), nullable=False)
    meta_data = db.Column(JSON, nullable=True)



    def __repr__(self):
        return f'<Favorite: {self.title}>'

    
    def save(self):
        """
        """
        instance = super(Favorite, self).save()
        Favorite.reorder_ranks(instance.id, instance.category_id)
        return instance

    def update(self, **kwargs):
        """
        """
        instance = super(Favorite, self).update(**kwargs)
        Favorite.reorder_ranks(instance.id, instance.category_id)
        return instance

    
    def delete(self):
        """
        """
        status = super(Favorite, self).delete()
        Favorite.reorder_ranks(None, self.category_id)
        return status

    @staticmethod
    def reorder_ranks(pk, category_id):
        query = \
        """
        UPDATE favorites f
        JOIN (
            SELECT t.id, count(*) AS rank_below
            FROM favorites t
            JOIN favorites tr ON tr.ranking <= t.ranking
            WHERE tr.category_id = {0}
            GROUP BY t.id
        ) c ON c.id=f.id
        SET f.ranking = c.rank_below
        """
        if pk:
            query += \
                """
                WHERE (f.id < {1} or f.id > {1})
                AND f.category_id = {0}
                """
            query = query.format(category_id,pk)
        else:
            query += \
                """
                WHERE f.category_id = {0}
                """
            query = query.format(category_id)
        output = db.engine.execute(text(query))

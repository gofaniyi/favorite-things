"""empty message

Revision ID: 1b215551edf9
Revises: 
Create Date: 2019-06-10 11:52:26.997614

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1b215551edf9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('audit',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('modified_date', sa.DateTime(), nullable=True),
    sa.Column('resource_id', sa.Integer(), nullable=False),
    sa.Column('resource_type', sa.String(length=60), nullable=False),
    sa.Column('action', sa.String(length=60), nullable=False),
    sa.Column('activity', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_audit'))
    )
    op.create_index(op.f('ix_audit_action'), 'audit', ['action'], unique=False)
    op.create_index(op.f('ix_audit_resource_id'), 'audit', ['resource_id'], unique=False)
    op.create_index(op.f('ix_audit_resource_type'), 'audit', ['resource_type'], unique=False)
    op.create_table('categories',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('modified_date', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_categories')),
    sa.UniqueConstraint('name', name=op.f('uq_categories_name'))
    )
    op.create_table('favorites',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('modified_date', sa.DateTime(), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('ranking', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('meta_data', mysql.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], name=op.f('favorites_category_id_fkey')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_favorites')),
    sa.UniqueConstraint('title', name=op.f('uq_favorites_title'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favorites')
    op.drop_table('categories')
    op.drop_index(op.f('ix_audit_resource_type'), table_name='audit')
    op.drop_index(op.f('ix_audit_resource_id'), table_name='audit')
    op.drop_index(op.f('ix_audit_action'), table_name='audit')
    op.drop_table('audit')
    # ### end Alembic commands ###

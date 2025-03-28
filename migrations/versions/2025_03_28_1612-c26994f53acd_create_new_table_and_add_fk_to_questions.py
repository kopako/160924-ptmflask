"""create new table and add fk to questions

Revision ID: c26994f53acd
Revises: 85d119cb56b5
Create Date: 2025-03-28 16:12:50.608828

"""
from alembic import op
import sqlalchemy as sa


revision = 'c26994f53acd'
down_revision = '85d119cb56b5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('categories',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    if_not_exists=True
    )
    with op.batch_alter_table('questions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'categories', ['category_id'], ['id'])


def downgrade():
    with op.batch_alter_table('questions', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('category_id')

    op.drop_table('categories')

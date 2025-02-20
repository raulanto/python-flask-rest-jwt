"""Initial migration

Revision ID: 59adf8ad2439
Revises: 
Create Date: 2025-02-20 00:54:58.402952

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59adf8ad2439'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ship',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('affiliation', sa.String(length=80), nullable=False),
    sa.Column('category', sa.String(length=80), nullable=False),
    sa.Column('crew', sa.Integer(), nullable=False),
    sa.Column('length', sa.Integer(), nullable=False),
    sa.Column('manufacturer', sa.String(length=120), nullable=False),
    sa.Column('model', sa.String(length=120), nullable=False),
    sa.Column('ship_class', sa.String(length=120), nullable=False),
    sa.Column('roles', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('roles', sa.Text(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('ship')
    # ### end Alembic commands ###

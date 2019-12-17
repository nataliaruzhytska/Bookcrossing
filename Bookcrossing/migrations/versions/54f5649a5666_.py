"""empty message

Revision ID: 54f5649a5666
Revises: 
Create Date: 2019-11-20 15:02:03.821520

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54f5649a5666'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('users_library_id_fkey', 'users', type_='foreignkey')
    op.drop_column('users', 'library_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('library_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('users_library_id_fkey', 'users', 'library', ['library_id'], ['lib_id'])
    # ### end Alembic commands ###
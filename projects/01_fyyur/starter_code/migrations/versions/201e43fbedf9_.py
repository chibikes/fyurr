"""empty message

Revision ID: 201e43fbedf9
Revises: b5ce9a0ded57
Create Date: 2022-08-24 23:27:43.545573

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '201e43fbedf9'
down_revision = 'b5ce9a0ded57'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'artists', ['name'])
    op.create_unique_constraint(None, 'venues', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'venues', type_='unique')
    op.drop_constraint(None, 'artists', type_='unique')
    # ### end Alembic commands ###

"""empty message

Revision ID: 1372251bbc98
Revises: 1d86b6f980ef
Create Date: 2022-08-22 18:35:04.947112

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1372251bbc98'
down_revision = '1d86b6f980ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('genres', sa.ARRAY(sa.String()), nullable=False))
    op.add_column('venues', sa.Column('genres', sa.ARRAY(sa.String()), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venues', 'genres')
    op.drop_column('artists', 'genres')
    # ### end Alembic commands ###
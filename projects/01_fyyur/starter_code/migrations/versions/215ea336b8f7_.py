"""empty message

Revision ID: 215ea336b8f7
Revises: 7c3566f32a58
Create Date: 2022-08-21 18:21:42.156508

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '215ea336b8f7'
down_revision = '7c3566f32a58'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('genres', sa.String(), nullable=True))
    op.add_column('venues', sa.Column('genres', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venues', 'genres')
    op.drop_column('artists', 'genres')
    # ### end Alembic commands ###

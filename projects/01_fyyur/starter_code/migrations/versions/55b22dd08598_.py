"""empty message

Revision ID: 55b22dd08598
Revises: d8c9becd2066
Create Date: 2022-08-20 15:08:49.688873

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55b22dd08598'
down_revision = 'd8c9becd2066'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('shows_artist_id_fkey', 'shows', type_='foreignkey')
    op.drop_column('shows', 'artist_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shows', sa.Column('artist_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('shows_artist_id_fkey', 'shows', 'artists', ['artist_id'], ['id'])
    # ### end Alembic commands ###

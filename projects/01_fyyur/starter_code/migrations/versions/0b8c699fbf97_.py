"""empty message

Revision ID: 0b8c699fbf97
Revises: 57dbc8386438
Create Date: 2022-08-20 11:17:30.718847

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b8c699fbf97'
down_revision = '57dbc8386438'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('artists', 'seeking_venue')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('seeking_venue', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###

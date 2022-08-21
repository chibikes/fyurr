"""empty message

Revision ID: 1ee2ea7deb5a
Revises: 5aabd96938d3
Create Date: 2022-08-20 11:09:14.256790

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ee2ea7deb5a'
down_revision = '5aabd96938d3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('seeking_venue', sa.String(), nullable=True))
    op.add_column('artists', sa.Column('seeking_description', sa.String(), nullable=True))
    op.add_column('artists', sa.Column('website_link', sa.String(length=120), nullable=True))
    op.drop_column('artists', 'genres')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('genres', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.drop_column('artists', 'website_link')
    op.drop_column('artists', 'seeking_description')
    op.drop_column('artists', 'seeking_venue')
    # ### end Alembic commands ###
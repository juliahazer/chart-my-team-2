"""add primarykeyconstraint rosters

Revision ID: fa6012c09c5a
Revises: 9b6d65313fa6
Create Date: 2017-05-31 20:43:22.727212

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa6012c09c5a'
down_revision = '9b6d65313fa6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('rosters', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rosters', sa.Column('id', sa.INTEGER(), nullable=False))
    # ### end Alembic commands ###

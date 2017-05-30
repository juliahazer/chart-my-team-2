"""added org_id to teams

Revision ID: a3ac553cc397
Revises: 38b9bd95362d
Create Date: 2017-05-30 15:35:16.970510

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3ac553cc397'
down_revision = '38b9bd95362d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('teams', sa.Column('org_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('teams', 'org_id')
    # ### end Alembic commands ###

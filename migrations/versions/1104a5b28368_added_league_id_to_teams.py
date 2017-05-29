"""added league_id to teams

Revision ID: 1104a5b28368
Revises: af3d48257a46
Create Date: 2017-05-29 11:15:58.385130

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1104a5b28368'
down_revision = 'af3d48257a46'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('teams', sa.Column('league_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('teams', 'league_id')
    # ### end Alembic commands ###

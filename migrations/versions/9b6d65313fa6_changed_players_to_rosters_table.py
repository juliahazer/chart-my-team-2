"""changed players to rosters table

Revision ID: 9b6d65313fa6
Revises: 95a83417b00e
Create Date: 2017-05-31 20:10:17.599082

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b6d65313fa6'
down_revision = '95a83417b00e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rosters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('player_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('city', sa.Text(), nullable=True),
    sa.Column('gender', sa.Text(), nullable=True),
    sa.Column('rating', sa.Text(), nullable=True),
    sa.Column('np_sw', sa.Text(), nullable=True),
    sa.Column('expiration', sa.Text(), nullable=True),
    sa.Column('won', sa.Integer(), nullable=True),
    sa.Column('lost', sa.Integer(), nullable=True),
    sa.Column('matches', sa.Integer(), nullable=True),
    sa.Column('defaults', sa.Integer(), nullable=True),
    sa.Column('win_percent', sa.Integer(), nullable=True),
    sa.Column('singles', sa.Integer(), nullable=True),
    sa.Column('doubles', sa.Integer(), nullable=True),
    sa.Column('team_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['team_id'], ['teams.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('players')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('players',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('player_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('name', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('city', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('gender', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('rating', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('np_sw', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('expiration', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('won', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('lost', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('matches', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('defaults', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('win_percent', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('singles', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('doubles', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('team_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['team_id'], ['teams.id'], name='players_team_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='players_pkey')
    )
    op.drop_table('rosters')
    # ### end Alembic commands ###

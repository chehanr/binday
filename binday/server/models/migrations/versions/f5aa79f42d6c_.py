"""empty message

Revision ID: f5aa79f42d6c
Revises: 7a998316135c
Create Date: 2020-05-21 19:10:18.431397

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5aa79f42d6c'
down_revision = '7a998316135c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bin_reading',
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.Column('date_updated', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sonar_reading', sa.Integer(), nullable=False),
    sa.Column('led_status', sa.Boolean(), nullable=False),
    sa.Column('my_bin_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['my_bin_id'], ['my_bin.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bin_reading')
    # ### end Alembic commands ###

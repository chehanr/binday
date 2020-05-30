"""empty message

Revision ID: 47688dd1ec92
Revises: f5aa79f42d6c
Create Date: 2020-05-30 18:43:29.725876

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47688dd1ec92'
down_revision = 'f5aa79f42d6c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_config',
    sa.Column('pushbullet_api_key', sa.String(length=128), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_config')
    # ### end Alembic commands ###
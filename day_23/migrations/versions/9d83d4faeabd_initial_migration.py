"""initial migration

Revision ID: 9d83d4faeabd
Revises: 
Create Date: 2020-04-24 12:56:05.160179

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d83d4faeabd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('tel', sa.String(length=100), nullable=True),
    sa.Column('password', sa.String(length=100), nullable=True),
    sa.Column('transactionPin', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('wallet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.Column('transactionLogs', sa.PickleType(), nullable=True),
    sa.Column('User_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['User_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('wallet')
    op.drop_table('user')
    # ### end Alembic commands ###

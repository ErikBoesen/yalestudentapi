"""birth_day and birth_month

Revision ID: ee481e23e0bd
Revises: 210c909216c2
Create Date: 2021-05-19 20:38:09.363250

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee481e23e0bd'
down_revision = '210c909216c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('person', schema=None) as batch_op:
        batch_op.add_column(sa.Column('birth_day', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('birth_month', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('person', schema=None) as batch_op:
        batch_op.drop_column('birth_month')
        batch_op.drop_column('birth_day')

    # ### end Alembic commands ###

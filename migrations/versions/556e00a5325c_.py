"""empty message

Revision ID: 556e00a5325c
Revises: af2a33ad2456
Create Date: 2023-02-14 20:34:56.296132

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '556e00a5325c'
down_revision = 'af2a33ad2456'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['phone'])
        batch_op.create_unique_constraint(None, ['email'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###

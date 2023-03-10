"""empty message

Revision ID: b8bd4d4170fa
Revises: 556e00a5325c
Create Date: 2023-02-14 21:37:13.958825

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b8bd4d4170fa'
down_revision = '556e00a5325c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.drop_constraint('employees_company_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'companies', ['company_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('employees_company_id_fkey', 'companies', ['company_id'], ['id'])

    # ### end Alembic commands ###

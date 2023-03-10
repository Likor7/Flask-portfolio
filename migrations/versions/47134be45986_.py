"""empty message

Revision ID: 47134be45986
Revises: 577b02e188aa
Create Date: 2023-02-14 18:04:21.445355

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47134be45986'
down_revision = '577b02e188aa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('company_employee',
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.Column('employee_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.ForeignKeyConstraint(['employee_id'], ['employees.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('company_employee')
    # ### end Alembic commands ###

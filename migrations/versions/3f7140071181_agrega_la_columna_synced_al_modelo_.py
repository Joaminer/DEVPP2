"""Agrega la columna 'synced' al modelo Material

Revision ID: 3f7140071181
Revises: 
Create Date: 2024-05-17 16:23:41.214981

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f7140071181'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('material', schema=None) as batch_op:
        batch_op.add_column(sa.Column('synced', sa.Boolean(), nullable=True))
        batch_op.alter_column('codigo_barras',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=50),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('material', schema=None) as batch_op:
        batch_op.alter_column('codigo_barras',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)
        batch_op.drop_column('synced')

    # ### end Alembic commands ###

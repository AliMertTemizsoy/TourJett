"""Add tur_sefer_id to rezervasyon

Revision ID: c25c918555db
Revises: 21c36bda6c79
Create Date: 2025-04-25 14:04:09.736809

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c25c918555db'
down_revision = '21c36bda6c79'
branch_labels = None
depends_on = None


def upgrade():
    # Use batch_alter_table to safely add the column to an existing table
    with op.batch_alter_table('rezervasyonlar', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tur_sefer_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_rezervasyon_tur_seferi', 'tur_seferi', ['tur_sefer_id'], ['id'])


def downgrade():
    # Remove the column if we need to roll back
    with op.batch_alter_table('rezervasyonlar', schema=None) as batch_op:
        batch_op.drop_constraint('fk_rezervasyon_tur_seferi', type_='foreignkey')
        batch_op.drop_column('tur_sefer_id')

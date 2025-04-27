"""merge multiple heads

Revision ID: 2294d293dde3
Revises: 628c36810a3a, 9e39c34c082d
Create Date: 2025-04-27 18:23:41.619302

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2294d293dde3'
down_revision = ('628c36810a3a', '9e39c34c082d')
branch_labels = None
depends_on = None


def upgrade():
    # Tur paketleri tablosuna destinasyon_id sütunu ekleme
    op.add_column('tur_paketleri', sa.Column('destinasyon_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'fk_tur_paketleri_destinasyonlar', 
        'tur_paketleri', 
        'destinasyonlar', 
        ['destinasyon_id'], 
        ['id']
    )


def downgrade():
    # Eklenen sütunu kaldırma
    op.drop_constraint('fk_tur_paketleri_destinasyonlar', 'tur_paketleri', type_='foreignkey')
    op.drop_column('tur_paketleri', 'destinasyon_id')

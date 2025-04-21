"""Simple fix

Revision ID: simple_fix
Revises: 486c97c4930b
Create Date: 2025-04-21 13:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'simple_fix'
down_revision = '486c97c4930b'
branch_labels = None
depends_on = None

def upgrade():
    # sure sütunu zaten değiştirildi, başka değişiklik yapmıyoruz
    pass

def downgrade():
    # Geri dönüş gerekmiyor
    pass

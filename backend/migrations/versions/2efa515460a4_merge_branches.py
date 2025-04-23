"""merge branches

Revision ID: 2efa515460a4
Revises: 8a626b39bb2e, simple_fix
Create Date: 2025-04-23 18:40:07.492313

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2efa515460a4'
down_revision = ('8a626b39bb2e', 'simple_fix')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass

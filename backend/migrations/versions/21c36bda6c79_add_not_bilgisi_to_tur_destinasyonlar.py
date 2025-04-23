from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21c36bda6c79'
down_revision = '2efa515460a4'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('tur_destinasyonlar', schema=None) as batch_op:
        batch_op.add_column(sa.Column('not_bilgisi', sa.Text(), nullable=True))

def downgrade():
    with op.batch_alter_table('tur_destinasyonlar', schema=None) as batch_op:
        batch_op.drop_column('not_bilgisi')

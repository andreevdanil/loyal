"""Create pgcrypto extension.

Revision ID: 1d67447b8eae
Revises:
Create Date: 2020-12-01 19:54:07.215308

"""

from alembic import op

revision = "1d67447b8eae"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE EXTENSION pgcrypto;")


def downgrade():
    op.execute("DROP EXTENSION pgcrypto;")

"""Create passwords table.

Revision ID: 1b81f93b9c27
Revises: 1d67447b8eae
Create Date: 2020-12-01 19:55:04.450828

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP, BYTEA

revision = "1b81f93b9c27"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "passwords",

        sa.Column("id", UUID, primary_key=True),
        sa.Column("salt", BYTEA, nullable=False),
        sa.Column("password", BYTEA, nullable=False),
        sa.Column("created_at", TIMESTAMP, nullable=False),
    )


def downgrade():
    op.drop_table("passwords")

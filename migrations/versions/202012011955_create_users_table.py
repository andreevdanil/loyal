"""Create users table.

Revision ID: a07ccb9c10a6
Revises: 1b81f93b9c27
Create Date: 2020-12-01 19:55:37.319233

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID, TEXT, TIMESTAMP

revision = "a07ccb9c10a6"
down_revision = "1b81f93b9c27"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",

        sa.Column("id", UUID, primary_key=True),
        sa.Column("first_name", TEXT, nullable=False),
        sa.Column("last_name", TEXT, nullable=False),
        sa.Column("email", TEXT, nullable=False),
        sa.Column("password_id", UUID, nullable=False),
        sa.Column("eth_address", TEXT, nullable=False),
        sa.Column("created_at", TIMESTAMP, nullable=False),

        sa.ForeignKeyConstraint(
            ("password_id", ),
            ("passwords.id", ),
        ),

        sa.Index(
            "email_users_idx",
            sa.Column("email"),
        ),
    )


def downgrade():
    op.drop_table("users")

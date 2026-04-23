"""cascade import_logs on account delete

Revision ID: 032
Revises: 031
Create Date: 2026-04-23
"""

from alembic import op

revision = "032"
down_revision = "031"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_constraint(
        "import_logs_account_id_fkey", "import_logs", type_="foreignkey"
    )
    op.create_foreign_key(
        "import_logs_account_id_fkey",
        "import_logs",
        "accounts",
        ["account_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint(
        "import_logs_account_id_fkey", "import_logs", type_="foreignkey"
    )
    op.create_foreign_key(
        "import_logs_account_id_fkey",
        "import_logs",
        "accounts",
        ["account_id"],
        ["id"],
    )

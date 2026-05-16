from alembic import op


revision = "20260515_0002"
down_revision = "20260515_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE INDEX ix_machiyotl_evidence_owner_status
        ON machiyotl.evidence_items (owner_user_id, status);
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DROP INDEX IF EXISTS machiyotl.ix_machiyotl_evidence_owner_status;
        """
    )

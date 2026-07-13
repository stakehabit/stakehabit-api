"""Create pool, pool_participants, and pool_checkins tables."""

from alembic import op
import sqlalchemy as sa

revision = "0002_create_pools"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "pools",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(length=1024), nullable=True),
        sa.Column("duration", sa.Integer(), nullable=False),
        sa.Column("stake_amount", sa.Numeric(20, 7), nullable=False),
        sa.Column("currency", sa.String(length=10), nullable=False),
        sa.Column("max_participants", sa.Integer(), nullable=False),
        sa.Column("winner_split", sa.Integer(), nullable=False),
        sa.Column("charity", sa.String(length=50), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="active"),
        sa.Column("contract_address", sa.String(length=56), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("creator_address", sa.String(length=56), nullable=False),
        sa.Column("creator_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["creator_id"], ["users.id"], ondelete="SET NULL"),
    )
    op.create_index(op.f("ix_pools_id"), "pools", ["id"], unique=False)

    op.create_table(
        "pool_participants",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("pool_id", sa.Integer(), nullable=False),
        sa.Column("wallet_address", sa.String(length=56), nullable=False),
        sa.Column("joined_at", sa.DateTime(), nullable=False),
        sa.Column("days_completed", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("current_streak", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="active"),
        sa.ForeignKeyConstraint(["pool_id"], ["pools.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("pool_id", "wallet_address", name="uq_pool_wallet"),
    )
    op.create_index(op.f("ix_pool_participants_id"), "pool_participants", ["id"], unique=False)

    op.create_table(
        "pool_checkins",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("participant_id", sa.Integer(), nullable=False),
        sa.Column("pool_id", sa.Integer(), nullable=False),
        sa.Column("check_in_date", sa.Date(), nullable=False),
        sa.Column("tx_hash", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["participant_id"], ["pool_participants.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["pool_id"], ["pools.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("participant_id", "check_in_date", name="uq_participant_checkin"),
    )
    op.create_index(op.f("ix_pool_checkins_id"), "pool_checkins", ["id"], unique=False)


def downgrade() -> None:
    op.drop_table("pool_checkins")
    op.drop_table("pool_participants")
    op.drop_table("pools")

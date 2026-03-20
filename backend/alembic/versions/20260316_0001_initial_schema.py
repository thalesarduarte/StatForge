"""initial schema

Revision ID: 20260316_0001
Revises:
Create Date: 2026-03-16 00:00:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260316_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("username", sa.String(length=50), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("is_admin", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_username", "users", ["username"], unique=True)

    op.create_table(
        "profiles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False, unique=True),
        sa.Column("display_name", sa.String(length=100), nullable=False),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("avatar_url", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "comments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("author_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("profile_id", sa.Integer(), sa.ForeignKey("profiles.id"), nullable=True),
        sa.Column("target_type", sa.String(length=50), nullable=False),
        sa.Column("target_id", sa.Integer(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "comment_likes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("comment_id", sa.Integer(), sa.ForeignKey("comments.id"), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("comment_id", "user_id", name="uq_comment_likes_comment_user"),
    )

    op.create_table(
        "favorites",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("target_type", sa.String(length=50), nullable=False),
        sa.Column("target_id", sa.Integer(), nullable=False),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "follows",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("follower_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("following_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("follower_id", "following_id", name="uq_follows_pair"),
    )

    op.create_table(
        "activity_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("actor_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("verb", sa.String(length=50), nullable=False),
        sa.Column("entity_type", sa.String(length=50), nullable=False),
        sa.Column("entity_id", sa.Integer(), nullable=True),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("metadata_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "teams",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=False, unique=True),
        sa.Column("slug", sa.String(length=120), nullable=False, unique=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "tournaments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("game_slug", sa.String(length=50), nullable=False),
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "badges",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False, unique=True),
        sa.Column("slug", sa.String(length=100), nullable=False, unique=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "game_profiles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("game_slug", sa.String(length=50), nullable=False),
        sa.Column("handle", sa.String(length=120), nullable=False),
        sa.Column("region", sa.String(length=30), nullable=True),
        sa.Column("external_player_id", sa.String(length=120), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "game_stats",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("game_profile_id", sa.Integer(), sa.ForeignKey("game_profiles.id"), nullable=False),
        sa.Column("game_slug", sa.String(length=50), nullable=False),
        sa.Column("stat_scope", sa.String(length=50), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "game_matches",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("game_profile_id", sa.Integer(), sa.ForeignKey("game_profiles.id"), nullable=False),
        sa.Column("game_slug", sa.String(length=50), nullable=False),
        sa.Column("external_match_id", sa.String(length=120), nullable=False),
        sa.Column("played_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "overwatch_profiles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("game_profile_id", sa.Integer(), sa.ForeignKey("game_profiles.id"), nullable=False, unique=True),
        sa.Column("current_rank", sa.String(length=50), nullable=False),
        sa.Column("main_hero", sa.String(length=80), nullable=False),
        sa.Column("role_stats", sa.JSON(), nullable=False),
        sa.Column("hero_stats", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "valorant_profiles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("game_profile_id", sa.Integer(), sa.ForeignKey("game_profiles.id"), nullable=False, unique=True),
        sa.Column("current_rank", sa.String(length=50), nullable=False),
        sa.Column("favorite_agents", sa.JSON(), nullable=False),
        sa.Column("core_stats", sa.JSON(), nullable=False),
        sa.Column("weapon_stats", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "cs2_profiles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("game_profile_id", sa.Integer(), sa.ForeignKey("game_profiles.id"), nullable=False, unique=True),
        sa.Column("current_rank", sa.String(length=50), nullable=False),
        sa.Column("kd", sa.Float(), nullable=False),
        sa.Column("hs_percentage", sa.Float(), nullable=False),
        sa.Column("weapon_stats", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "lol_profiles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("game_profile_id", sa.Integer(), sa.ForeignKey("game_profiles.id"), nullable=False, unique=True),
        sa.Column("current_elo", sa.String(length=60), nullable=False),
        sa.Column("primary_role", sa.String(length=40), nullable=False),
        sa.Column("champion_pool", sa.JSON(), nullable=False),
        sa.Column("core_stats", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "fortnite_profiles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("game_profile_id", sa.Integer(), sa.ForeignKey("game_profiles.id"), nullable=False, unique=True),
        sa.Column("platform", sa.String(length=40), nullable=False),
        sa.Column("victories", sa.Integer(), nullable=False),
        sa.Column("kills", sa.Integer(), nullable=False),
        sa.Column("kd", sa.Float(), nullable=False),
        sa.Column("mode_breakdown", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    for table_name in [
        "fortnite_profiles",
        "lol_profiles",
        "cs2_profiles",
        "valorant_profiles",
        "overwatch_profiles",
        "game_matches",
        "game_stats",
        "game_profiles",
        "activity_events",
        "badges",
        "tournaments",
        "teams",
        "follows",
        "favorites",
        "comment_likes",
        "comments",
        "profiles",
        "users",
    ]:
        op.drop_table(table_name)

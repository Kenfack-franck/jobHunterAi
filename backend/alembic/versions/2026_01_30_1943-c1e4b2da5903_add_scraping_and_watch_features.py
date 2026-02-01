"""add_scraping_and_watch_features

Revision ID: c1e4b2da5903
Revises: 9f3e15511125
Create Date: 2026-01-30 19:43:26.513272

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c1e4b2da5903'
down_revision = '9f3e15511125'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Ajouter champs à job_offers (seulement ceux qui manquent)
    # source_url existe déjà
    # job_type existe déjà
    # source_platform existe (on va l'utiliser comme 'source')
    
    # Ajouter les champs manquants
    op.add_column('job_offers', sa.Column('scraped_at', sa.DateTime(), nullable=True))
    op.add_column('job_offers', sa.Column('work_mode', sa.String(20), nullable=True))
    
    # 2. Table watched_companies (entreprises surveillées, mutualisée)
    op.create_table(
        'watched_companies',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('company_name', sa.String(200), nullable=False),
        sa.Column('company_slug', sa.String(200), unique=True, nullable=False),
        sa.Column('linkedin_url', sa.String(500), nullable=True),
        sa.Column('careers_url', sa.String(500), nullable=True),
        sa.Column('indeed_url', sa.String(500), nullable=True),
        sa.Column('wttj_url', sa.String(500), nullable=True),
        sa.Column('last_scraped_at', sa.DateTime(), nullable=True),
        sa.Column('scraping_frequency', sa.Integer(), server_default='24', nullable=False),
        sa.Column('total_watchers', sa.Integer(), server_default='0', nullable=False),
        sa.Column('total_offers_found', sa.Integer(), server_default='0', nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False)
    )
    op.create_index('idx_watched_companies_slug', 'watched_companies', ['company_slug'])
    
    # 3. Table user_company_watches (relation user ↔ entreprise)
    op.create_table(
        'user_company_watches',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('watched_company_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('watched_companies.id', ondelete='CASCADE'), nullable=False),
        sa.Column('alert_threshold', sa.Integer(), server_default='70', nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False)
    )
    op.create_index('idx_user_company_watches_user', 'user_company_watches', ['user_id'])
    op.create_index('idx_user_company_watches_company', 'user_company_watches', ['watched_company_id'])
    op.create_unique_constraint('uq_user_company_watch', 'user_company_watches', ['user_id', 'watched_company_id'])
    
    # 4. Table user_feed_cache (cache pré-calculé nocturne)
    # Utiliser 'profiles' au lieu de 'candidate_profiles'
    op.create_table(
        'user_feed_cache',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('profile_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('profiles.id', ondelete='CASCADE'), nullable=False),
        sa.Column('job_offer_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('job_offers.id', ondelete='CASCADE'), nullable=False),
        sa.Column('compatibility_score', sa.Float(), nullable=False),
        sa.Column('calculated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False)
    )
    op.create_index('idx_user_feed_cache_user_profile', 'user_feed_cache', ['user_id', 'profile_id'])
    op.create_index('idx_user_feed_cache_expires', 'user_feed_cache', ['expires_at'])
    op.create_unique_constraint('uq_user_profile_offer_cache', 'user_feed_cache', ['user_id', 'profile_id', 'job_offer_id'])
    
    # 5. Table custom_sources (sources custom ajoutées par users)
    op.create_table(
        'custom_sources',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('url', sa.String(500), nullable=False),
        sa.Column('platform', sa.String(50), nullable=True),
        sa.Column('status', sa.String(20), server_default='pending', nullable=False),
        sa.Column('last_scraped_at', sa.DateTime(), nullable=True),
        sa.Column('offers_found', sa.Integer(), server_default='0', nullable=False),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False)
    )
    op.create_index('idx_custom_sources_user', 'custom_sources', ['user_id'])
    op.create_index('idx_custom_sources_status', 'custom_sources', ['status'])


def downgrade() -> None:
    # Supprimer dans l'ordre inverse
    op.drop_table('custom_sources')
    op.drop_table('user_feed_cache')
    op.drop_table('user_company_watches')
    op.drop_table('watched_companies')
    
    # Supprimer colonnes job_offers (seulement celles qu'on a ajoutées)
    op.drop_column('job_offers', 'work_mode')
    op.drop_column('job_offers', 'scraped_at')

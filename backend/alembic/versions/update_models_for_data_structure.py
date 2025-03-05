"""update_models_for_data_structure

Revision ID: update_models_structure
Revises: add_health_notes_field
Create Date: 2025-03-05 15:20:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'update_models_structure'
down_revision = 'add_health_notes_field'
branch_labels = None
depends_on = None


def upgrade():
    # ### команды для обновления схемы БД ###
    
    # 1. Обновляем таблицу players
    op.add_column('players', sa.Column('first_name', sa.String(length=255), nullable=True))
    op.add_column('players', sa.Column('last_name', sa.String(length=255), nullable=True))
    op.add_column('players', sa.Column('middle_name', sa.String(length=255), nullable=True))
    
    # 2. Обновляем таблицу player_nicknames
    op.add_column('player_nicknames', sa.Column('room', sa.String(length=255), nullable=True))
    op.add_column('player_nicknames', sa.Column('discipline', sa.String(length=255), nullable=True))
    op.drop_column('player_nicknames', 'source')
    
    # 3. Создаем таблицу player_payment_methods
    op.create_table('player_payment_methods',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('player_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('type', sa.String(length=50), nullable=False),
        sa.Column('value', sa.String(length=255), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['player_id'], ['players.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 4. Создаем таблицу player_social_media
    op.create_table('player_social_media',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('player_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('type', sa.String(length=50), nullable=False),
        sa.Column('value', sa.String(length=255), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['player_id'], ['players.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 5. Обновляем таблицу cases
    op.add_column('cases', sa.Column('arbitrage_type', sa.String(length=255), nullable=True))
    op.add_column('cases', sa.Column('arbitrage_amount', sa.Float(), nullable=True))
    op.add_column('cases', sa.Column('arbitrage_currency', sa.String(length=10), nullable=True, server_default='USD'))
    
    # 6. Добавляем description к case_evidences
    op.add_column('case_evidences', sa.Column('description', sa.Text(), nullable=True))
    
    # 7. Создаем таблицу case_comments
    op.create_table('case_comments',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('case_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('comment', sa.Text(), nullable=False),
        sa.Column('created_by_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, default=sa.text('now()')),
        sa.ForeignKeyConstraint(['case_id'], ['cases.id'], ),
        sa.ForeignKeyConstraint(['created_by_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # ### конец команд обновления ###


def downgrade():
    # ### команды для отката схемы БД ###
    
    # 7. Удаляем таблицу case_comments
    op.drop_table('case_comments')
    
    # 6. Удаляем description из case_evidences
    op.drop_column('case_evidences', 'description')
    
    # 5. Откатываем изменения в таблице cases
    op.drop_column('cases', 'arbitrage_currency')
    op.drop_column('cases', 'arbitrage_amount')
    op.drop_column('cases', 'arbitrage_type')
    
    # 4. Удаляем таблицу player_social_media
    op.drop_table('player_social_media')
    
    # 3. Удаляем таблицу player_payment_methods
    op.drop_table('player_payment_methods')
    
    # 2. Откатываем изменения в таблице player_nicknames
    op.add_column('player_nicknames', sa.Column('source', sa.String(length=255), nullable=True))
    op.drop_column('player_nicknames', 'discipline')
    op.drop_column('player_nicknames', 'room')
    
    # 1. Откатываем изменения в таблице players
    op.drop_column('players', 'middle_name')
    op.drop_column('players', 'last_name')
    op.drop_column('players', 'first_name')
    
    # ### конец команд отката ### 
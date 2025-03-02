"""initial

Revision ID: 001
Revises: 
Create Date: 2024-02-28 15:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Создаем таблицу пользователей
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=False),
        sa.Column('organization', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('is_superuser', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint('email')
    )
    op.create_index('ix_users_email', 'users', ['email'])

    # Создаем справочные таблицы
    op.create_table(
        'poker_rooms',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint('name')
    )

    op.create_table(
        'disciplines',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint('name')
    )

    # Создаем основные таблицы
    op.create_table(
        'arbitrage_cases',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('author_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('status', sa.String(50), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['author_id'], ['users.id'])
    )

    op.create_table(
        'persons',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('case_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('first_name', sa.String(100), nullable=False),
        sa.Column('last_name', sa.String(100)),
        sa.Column('middle_name', sa.String(100)),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['case_id'], ['arbitrage_cases.id'], ondelete='CASCADE')
    )

    op.create_table(
        'addresses',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('case_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('country', sa.String(100)),
        sa.Column('region', sa.String(100)),
        sa.Column('city', sa.String(100)),
        sa.Column('street', sa.String(200)),
        sa.Column('building', sa.String(50)),
        sa.Column('apartment', sa.String(50)),
        sa.Column('postal_code', sa.String(20)),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['case_id'], ['arbitrage_cases.id'], ondelete='CASCADE')
    )

    op.create_table(
        'nicknames',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('case_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('room_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('discipline_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('nickname', sa.String(100), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['case_id'], ['arbitrage_cases.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['room_id'], ['poker_rooms.id']),
        sa.ForeignKeyConstraint(['discipline_id'], ['disciplines.id'])
    )

    op.create_table(
        'contacts',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('case_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('type', sa.String(50), nullable=False),
        sa.Column('value', sa.Text, nullable=False),
        sa.Column('verified', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['case_id'], ['arbitrage_cases.id'], ondelete='CASCADE')
    )

    op.create_table(
        'incidents',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('case_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('type', sa.String(50), nullable=False),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('amount', sa.Numeric(15, 2)),
        sa.Column('currency', sa.String(3), default='USD'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['case_id'], ['arbitrage_cases.id'], ondelete='CASCADE')
    )

    op.create_table(
        'evidence',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('incident_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('type', sa.String(50), nullable=False),
        sa.Column('url', sa.Text, nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['incident_id'], ['incidents.id'], ondelete='CASCADE')
    )

    # Создаем индексы для поиска
    op.create_index('ix_persons_names', 'persons',
                    ['first_name', 'last_name', 'middle_name'],
                    postgresql_using='gin',
                    postgresql_ops={
                        'first_name': 'gin_trgm_ops',
                        'last_name': 'gin_trgm_ops',
                        'middle_name': 'gin_trgm_ops'
                    })
    op.create_index('ix_nicknames_nickname', 'nicknames', ['nickname'],
                    postgresql_using='gin',
                    postgresql_ops={'nickname': 'gin_trgm_ops'})
    op.create_index('ix_contacts_value', 'contacts', ['value'],
                    postgresql_using='gin',
                    postgresql_ops={'value': 'gin_trgm_ops'})

def downgrade():
    op.drop_index('ix_contacts_value')
    op.drop_index('ix_nicknames_nickname')
    op.drop_index('ix_persons_names')
    op.drop_index('ix_users_email')

    op.drop_table('evidence')
    op.drop_table('incidents')
    op.drop_table('contacts')
    op.drop_table('nicknames')
    op.drop_table('addresses')
    op.drop_table('persons')
    op.drop_table('arbitrage_cases')
    op.drop_table('disciplines')
    op.drop_table('poker_rooms')
    op.drop_table('users') 
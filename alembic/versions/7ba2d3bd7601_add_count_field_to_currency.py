"""add count field to Currency

Revision ID: 7ba2d3bd7601
Revises: f05e47cd1acb
Create Date: 2025-02-13 22:43:26.982807

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7ba2d3bd7601'
down_revision: Union[str, None] = 'f05e47cd1acb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_currency_requests')
    op.drop_table('currencies')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('currencies',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('currencies_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('code', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='currencies_pkey'),
    sa.UniqueConstraint('code', name='currencies_code_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('user_currency_requests',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('currency_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('timestamp', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['currency_id'], ['currencies.id'], name='user_currency_requests_currency_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], name='user_currency_requests_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='user_currency_requests_pkey')
    )
    # ### end Alembic commands ###

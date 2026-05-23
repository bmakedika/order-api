"""add customers table and stock to products

Revision ID: cd32cbf8fbee
Revises: c61a95690531
Create Date: 2026-05-19 23:14:06.965949

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd32cbf8fbee'
down_revision: Union[str, Sequence[str], None] = 'c61a95690531'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'customers',
        sa.Column('id',               sa.UUID(),                  nullable=False),
        sa.Column('email',            sa.String(),                nullable=False),
        sa.Column('full_name',        sa.String(),                nullable=True),
        sa.Column('phone',            sa.String(),                nullable=True),
        sa.Column('address',          sa.String(),                nullable=True),
        sa.Column('birthdate',        sa.Date(),                  nullable=True),
        sa.Column('marketing_optin',  sa.Boolean(),               nullable=True, default=False),
        sa.Column('kyc_level',        sa.String(),                nullable=True),
        sa.Column('gdpr_consent_at',  sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at',       sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
    )

    op.add_column('products',
        sa.Column('stock_quantity',    sa.Integer(), nullable=False, server_default='0'))
    op.add_column('products',
        sa.Column('reserved_quantity', sa.Integer(), nullable=False, server_default='0'))


def downgrade() -> None:
    op.drop_column('products', 'reserved_quantity')
    op.drop_column('products', 'stock_quantity')
    op.drop_table('customers')

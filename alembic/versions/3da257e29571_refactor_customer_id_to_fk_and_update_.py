"""refactor customer_id to fk and update invoices

Revision ID: 3da257e29571
Revises: cd32cbf8fbee
Create Date: 2026-05-20 17:56:14.696168

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3da257e29571'
down_revision: Union[str, Sequence[str], None] = 'cd32cbf8fbee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ORDERS 
    op.drop_index('ix_orders_customer_id', table_name='orders')
    op.drop_column('orders', 'customer_id')
    op.add_column('orders',
        sa.Column('customer_id', sa.UUID(), nullable=True))
    
    op.create_foreign_key(
        'fk_orders_customer_id',
        'orders',             
        'customers',                
        ['customer_id'],            
        ['id'],                     
    )
    op.create_index('ix_orders_customer_id', 'orders', ['customer_id'])

    # INVOICES 
    op.drop_column('invoices', 'id_customer')
    op.add_column('invoices',
        sa.Column('customer_id', sa.UUID(), nullable=True))
    
    op.create_foreign_key(
        'fk_invoices_customer_id',
        'invoices',
        'customers',
        ['customer_id'],
        ['id'],
    )
    op.add_column('invoices',
        sa.Column('created_by', sa.UUID(), nullable=True))

    op.create_foreign_key(
        'fk_invoices_created_by',
        'invoices',
        'users',
        ['created_by'],
        ['id'],
    )
    op.add_column('invoices',
        sa.Column('validated_by', sa.UUID(), nullable=True))

    op.create_foreign_key(
        'fk_invoices_validated_by',
        'invoices',
        'users',
        ['validated_by'],
        ['id'],
    )
    op.add_column('invoices',
        sa.Column('validated_at', sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    # invoices
    op.drop_column('invoices', 'validated_at')
    op.drop_constraint('fk_invoices_validated_by', 'invoices', type_='foreignkey')
    op.drop_column('invoices', 'validated_by')
    op.drop_constraint('fk_invoices_created_by', 'invoices', type_='foreignkey')
    op.drop_column('invoices', 'created_by')
    op.drop_constraint('fk_invoices_customer_id', 'invoices', type_='foreignkey')
    op.drop_column('invoices', 'customer_id')

    op.add_column('invoices',
        sa.Column('id_customer', sa.String(), nullable=True))
    
    # orders
    op.drop_index('ix_orders_customer_id', table_name='orders')
    op.drop_constraint('fk_orders_customer_id', 'orders', type_='foreignkey')
    op.drop_column('orders', 'customer_id')

    op.add_column('orders',
        sa.Column('customer_id', sa.String(), nullable=True))
    op.create_index('ix_orders_customer_id', 'orders', ['customer_id'])

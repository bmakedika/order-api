from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID, uuid4
from datetime import datetime, timezone
from app.models.invoice import InvoiceModel, InvoiceItemModel


async def create_invoice(db: AsyncSession, order, id_payment: UUID, created_by: UUID = None):
    invoice_number = f"INV-{uuid4()}"
    tax = int(order.total_cents * 0.2)

    invoice = InvoiceModel(
        id=uuid4(),
        invoice_number=invoice_number,
        id_order=order.id,
        id_payment=id_payment,
        customer_id=order.customer_id,
        total_cents=order.total_cents,
        tax=tax,
        created_by=created_by,
        created_at=datetime.now(timezone.utc),
    )
    db.add(invoice)

    for item in order.items:
        invoice_item = InvoiceItemModel(
            id=uuid4(),
            invoice_id=invoice.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price_cents=item.unit_price_cents,
            line_total_cents=item.quantity * item.unit_price_cents,
        )
        db.add(invoice_item)

    await db.commit()
    await db.refresh(invoice)
    return invoice
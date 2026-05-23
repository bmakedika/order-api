from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID
from app.core.auth import require_user
from app.core.database import get_db
from app.models.invoice import InvoiceModel
from app.repos.user_repo import get_by_email
from app.schemas.invoice import InvoiceResponse
from app.services import order_service

router = APIRouter()


@router.get('/orders/{order_id}/invoices', response_model=List[InvoiceResponse])
async def get_invoices_by_order(
    order_id: UUID,
    payload=Depends(require_user),
    db: AsyncSession = Depends(get_db),
):
    user  = await get_by_email(db, email=payload['sub'])
    order = await order_service.get_order(db, order_id)

    if payload.get('role') != 'admin' and order.user_id != user.id:
        raise HTTPException(status_code=403, detail='Forbidden')

    result = await db.execute(
        select(InvoiceModel).where(InvoiceModel.id_order == order_id)
    )
    return result.scalars().all()


@router.get('/invoices/{invoice_id}', response_model=InvoiceResponse)
async def get_invoice(
    invoice_id: UUID,
    payload=Depends(require_user),
    db: AsyncSession = Depends(get_db),
):
    user   = await get_by_email(db, email=payload['sub'])
    result = await db.execute(
        select(InvoiceModel).where(InvoiceModel.id == invoice_id)
    )
    invoice = result.scalar_one_or_none()
    if not invoice:
        raise HTTPException(status_code=404, detail='Invoice not found')

    if payload.get('role') != 'admin' and invoice.order.user_id != user.id:
        raise HTTPException(status_code=403, detail='Forbidden')

    return invoice
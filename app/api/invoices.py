from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.core.auth import require_user
from app.core.database import get_db
from app.models.invoice import InvoiceModel as Invoice
from app.repos.user_repo import get_by_email
from app.schemas.invoice import InvoiceResponse
from app.services import order_service

router = APIRouter()


@router.get('/invoices/{invoice_id}', response_model=InvoiceResponse)
def get_invoice(
    invoice_id: UUID, 
    payload = Depends(require_user),
    db: Session = Depends(get_db)
    ):
    user = get_by_email(db, email=payload['sub'])
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail='Invoice not found')
    if invoice.order.user_id != user.id:
        raise HTTPException(status_code=403, detail='Forbidden')
    return invoice


@router.get('/orders/{order_id}/invoices', response_model=List[InvoiceResponse])
def get_invoices_by_order(
    order_id: UUID, 
    payload = Depends(require_user),
    db: Session = Depends(get_db)
    ):
    user = get_by_email(db, email=payload['sub'])
    order = order_service.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail='Order not found')
    if order.user_id != user.id:
        raise HTTPException(status_code=403, detail='Forbidden')
    invoices = db.query(Invoice).filter(Invoice.id_order == order_id).all()
    return invoices
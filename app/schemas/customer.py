from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime, date
from typing import Optional


class CustomerCreate(BaseModel):
    email:           str
    full_name:       Optional[str] = None
    phone:           Optional[str] = None
    address:         Optional[str] = None
    birthdate:       Optional[date] = None
    marketing_optin: Optional[bool] = False
    kyc_level:       Optional[str] = None
    gdpr_consent_at: Optional[datetime] = None


class CustomerUpdate(BaseModel):
    email:           Optional[str] = None
    full_name:       Optional[str] = None
    phone:           Optional[str] = None
    address:         Optional[str] = None
    birthdate:       Optional[date] = None
    marketing_optin: Optional[bool] = None
    kyc_level:       Optional[str] = None
    gdpr_consent_at: Optional[datetime] = None


class CustomerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:              UUID
    email:           str
    full_name:       Optional[str] = None
    phone:           Optional[str] = None
    address:         Optional[str] = None
    birthdate:       Optional[date] = None
    marketing_optin: Optional[bool] = None
    kyc_level:       Optional[str] = None
    gdpr_consent_at: Optional[datetime] = None
    created_at:      datetime
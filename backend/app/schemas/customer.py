"""Customer schemas."""

from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

EmploymentType = Literal[
    "Salaried", "Self-Employed", "Business Owner", "MSME", "Corporate", "Agriculture"
]
Gender = Literal["Male", "Female", "Other"]


class CustomerBase(BaseModel):
    customer_name: str = Field(min_length=1, max_length=200)
    gender: Gender | None = None
    date_of_birth: date | None = None
    occupation: str | None = None
    employment_type: EmploymentType | None = None
    annual_income: Decimal | None = Field(default=None, ge=0)
    credit_score: int | None = Field(default=None, ge=300, le=900)
    marital_status: str | None = None
    address: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    region: str | None = None
    branch_id: uuid.UUID | None = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    """All fields optional for partial update."""

    customer_name: str | None = Field(default=None, min_length=1, max_length=200)
    gender: Gender | None = None
    date_of_birth: date | None = None
    occupation: str | None = None
    employment_type: EmploymentType | None = None
    annual_income: Decimal | None = Field(default=None, ge=0)
    credit_score: int | None = Field(default=None, ge=300, le=900)
    marital_status: str | None = None
    address: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    region: str | None = None
    branch_id: uuid.UUID | None = None


class CustomerOut(CustomerBase):
    model_config = ConfigDict(from_attributes=True)

    customer_id: uuid.UUID
    created_at: datetime

"""Loan and repayment schemas."""

from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

LoanType = Literal["Personal", "Home", "MSME", "Agriculture", "Education"]
LoanStatus = Literal["Active", "Closed", "Overdue", "Defaulted"]


class LoanBase(BaseModel):
    customer_id: uuid.UUID
    loan_type: LoanType
    loan_amount: Decimal = Field(gt=0)
    interest_rate: Decimal = Field(ge=0)
    tenure_months: int = Field(gt=0)
    emi: Decimal = Field(gt=0)
    outstanding_amount: Decimal = Field(default=0, ge=0)
    loan_status: LoanStatus = "Active"
    disbursement_date: date | None = None


class LoanCreate(LoanBase):
    pass


class LoanUpdate(BaseModel):
    loan_type: LoanType | None = None
    loan_amount: Decimal | None = Field(default=None, gt=0)
    interest_rate: Decimal | None = Field(default=None, ge=0)
    tenure_months: int | None = Field(default=None, gt=0)
    emi: Decimal | None = Field(default=None, gt=0)
    outstanding_amount: Decimal | None = Field(default=None, ge=0)
    loan_status: LoanStatus | None = None
    disbursement_date: date | None = None


class LoanOut(LoanBase):
    model_config = ConfigDict(from_attributes=True)

    loan_id: uuid.UUID
    created_at: datetime


class RepaymentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    repayment_id: uuid.UUID
    loan_id: uuid.UUID
    due_date: date
    payment_date: date | None
    due_amount: Decimal
    payment_amount: Decimal
    delay_days: int
    payment_status: str

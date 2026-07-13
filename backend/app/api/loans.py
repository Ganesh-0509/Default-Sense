"""Loan endpoints (docs/10 §6)."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user, require_roles
from app.database import get_db
from app.models import User
from app.schemas.loan import LoanCreate, LoanOut, LoanUpdate, RepaymentOut
from app.services import loan_service
from app.utils.responses import success

router = APIRouter(prefix="/loans", tags=["Loans"])


@router.get("")
def list_loans(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> dict:
    loans, total = loan_service.list_loans(db, skip, limit)
    return success(
        {
            "items": [LoanOut.model_validate(loan) for loan in loans],
            "total": total,
            "skip": skip,
            "limit": limit,
        },
        message="Loans retrieved.",
    )


@router.get("/{loan_id}")
def get_loan(
    loan_id: uuid.UUID,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> dict:
    loan = loan_service.get_loan(db, loan_id)
    return success(LoanOut.model_validate(loan), message="Loan details.")


@router.get("/{loan_id}/repayments")
def get_repayments(
    loan_id: uuid.UUID,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> dict:
    repayments = loan_service.get_repayments(db, loan_id)
    return success(
        [RepaymentOut.model_validate(r) for r in repayments], message="Repayment history."
    )


@router.post("", status_code=status.HTTP_201_CREATED)
def create_loan(
    payload: LoanCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin", "risk_manager", "loan_officer")),
) -> dict:
    loan = loan_service.create_loan(db, payload)
    return success(LoanOut.model_validate(loan), message="Loan created.")


@router.put("/{loan_id}")
def update_loan(
    loan_id: uuid.UUID,
    payload: LoanUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin", "risk_manager", "loan_officer")),
) -> dict:
    loan = loan_service.update_loan(db, loan_id, payload)
    return success(LoanOut.model_validate(loan), message="Loan updated.")

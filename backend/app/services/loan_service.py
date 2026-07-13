"""Loan business logic."""

from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from app.models import Loan, RepaymentHistory
from app.repositories import customer_repository, loan_repository
from app.schemas.loan import LoanCreate, LoanUpdate
from app.utils.responses import APIException


def list_loans(db: Session, skip: int, limit: int) -> tuple[list[Loan], int]:
    return loan_repository.list_loans(db, skip, limit), loan_repository.count(db)


def get_loan(db: Session, loan_id: uuid.UUID) -> Loan:
    loan = loan_repository.get_by_id(db, loan_id)
    if loan is None:
        raise APIException(404, "Loan not found.")
    return loan


def create_loan(db: Session, payload: LoanCreate) -> Loan:
    # Referential guard: the customer must exist.
    if customer_repository.get_by_id(db, payload.customer_id) is None:
        raise APIException(404, "Cannot create loan: customer not found.")
    loan = Loan(**payload.model_dump(exclude_none=True))
    return loan_repository.save(db, loan)


def update_loan(db: Session, loan_id: uuid.UUID, payload: LoanUpdate) -> Loan:
    loan = get_loan(db, loan_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(loan, field, value)
    return loan_repository.save(db, loan)


def get_repayments(db: Session, loan_id: uuid.UUID) -> list[RepaymentHistory]:
    get_loan(db, loan_id)  # 404 if missing
    return loan_repository.list_repayments(db, loan_id)

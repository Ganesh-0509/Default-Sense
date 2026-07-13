"""Data access for Loan and RepaymentHistory."""

from __future__ import annotations

import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Loan, RepaymentHistory


def list_loans(db: Session, skip: int = 0, limit: int = 50) -> list[Loan]:
    stmt = select(Loan).order_by(Loan.created_at.desc()).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())


def count(db: Session) -> int:
    return db.execute(select(func.count()).select_from(Loan)).scalar_one()


def get_by_id(db: Session, loan_id: uuid.UUID) -> Loan | None:
    return db.get(Loan, loan_id)


def save(db: Session, loan: Loan) -> Loan:
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan


def list_repayments(db: Session, loan_id: uuid.UUID) -> list[RepaymentHistory]:
    stmt = (
        select(RepaymentHistory)
        .where(RepaymentHistory.loan_id == loan_id)
        .order_by(RepaymentHistory.due_date)
    )
    return list(db.execute(stmt).scalars().all())

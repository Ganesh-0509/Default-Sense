"""Data access for Customer."""

from __future__ import annotations

import uuid

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models import Customer


def list_customers(db: Session, skip: int = 0, limit: int = 50) -> list[Customer]:
    stmt = select(Customer).order_by(Customer.created_at.desc()).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())


def count(db: Session) -> int:
    return db.execute(select(func.count()).select_from(Customer)).scalar_one()


def get_by_id(db: Session, customer_id: uuid.UUID) -> Customer | None:
    return db.get(Customer, customer_id)


def get_by_email(db: Session, email: str) -> Customer | None:
    return db.execute(select(Customer).where(Customer.email == email)).scalar_one_or_none()


def get_by_phone(db: Session, phone: str) -> Customer | None:
    return db.execute(select(Customer).where(Customer.phone == phone)).scalar_one_or_none()


def search(db: Session, query: str, limit: int = 50) -> list[Customer]:
    like = f"%{query}%"
    stmt = (
        select(Customer)
        .where(
            or_(
                Customer.customer_name.ilike(like),
                Customer.email.ilike(like),
                Customer.phone.ilike(like),
            )
        )
        .limit(limit)
    )
    return list(db.execute(stmt).scalars().all())


def save(db: Session, customer: Customer) -> Customer:
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def delete(db: Session, customer: Customer) -> None:
    db.delete(customer)
    db.commit()

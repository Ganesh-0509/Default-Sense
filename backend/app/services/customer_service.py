"""Customer business logic."""

from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from app.models import Customer
from app.repositories import customer_repository
from app.schemas.customer import CustomerCreate, CustomerUpdate
from app.utils.responses import APIException


def _ensure_unique_contact(
    db: Session, email: str | None, phone: str | None, exclude_id: uuid.UUID | None = None
) -> None:
    if email:
        existing = customer_repository.get_by_email(db, email)
        if existing and existing.customer_id != exclude_id:
            raise APIException(409, "A customer with this email already exists.")
    if phone:
        existing = customer_repository.get_by_phone(db, phone)
        if existing and existing.customer_id != exclude_id:
            raise APIException(409, "A customer with this phone number already exists.")


def list_customers(db: Session, skip: int, limit: int) -> tuple[list[Customer], int]:
    return customer_repository.list_customers(db, skip, limit), customer_repository.count(db)


def get_customer(db: Session, customer_id: uuid.UUID) -> Customer:
    customer = customer_repository.get_by_id(db, customer_id)
    if customer is None:
        raise APIException(404, "Customer not found.")
    return customer


def search_customers(db: Session, query: str) -> list[Customer]:
    if not query or not query.strip():
        raise APIException(400, "Search query must not be empty.")
    return customer_repository.search(db, query.strip())


def create_customer(db: Session, payload: CustomerCreate) -> Customer:
    _ensure_unique_contact(db, payload.email, payload.phone)
    customer = Customer(**payload.model_dump(exclude_none=True))
    return customer_repository.save(db, customer)


def update_customer(db: Session, customer_id: uuid.UUID, payload: CustomerUpdate) -> Customer:
    customer = get_customer(db, customer_id)
    updates = payload.model_dump(exclude_unset=True)
    _ensure_unique_contact(db, updates.get("email"), updates.get("phone"), exclude_id=customer_id)
    for field, value in updates.items():
        setattr(customer, field, value)
    return customer_repository.save(db, customer)


def delete_customer(db: Session, customer_id: uuid.UUID) -> None:
    customer = get_customer(db, customer_id)
    customer_repository.delete(db, customer)

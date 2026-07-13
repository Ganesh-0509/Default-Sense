"""Customer endpoints (docs/10 §5)."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user, require_roles
from app.database import get_db
from app.models import User
from app.schemas.customer import CustomerCreate, CustomerOut, CustomerUpdate
from app.services import customer_service
from app.utils.responses import success

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("")
def list_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> dict:
    customers, total = customer_service.list_customers(db, skip, limit)
    return success(
        {
            "items": [CustomerOut.model_validate(c) for c in customers],
            "total": total,
            "skip": skip,
            "limit": limit,
        },
        message="Customers retrieved.",
    )


@router.get("/search")
def search_customers(
    q: str = Query(..., min_length=1, description="Name, email, or phone fragment"),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> dict:
    results = customer_service.search_customers(db, q)
    return success([CustomerOut.model_validate(c) for c in results], message="Search results.")


@router.get("/{customer_id}")
def get_customer(
    customer_id: uuid.UUID,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> dict:
    customer = customer_service.get_customer(db, customer_id)
    return success(CustomerOut.model_validate(customer), message="Customer details.")


@router.post("", status_code=status.HTTP_201_CREATED)
def create_customer(
    payload: CustomerCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin", "risk_manager", "loan_officer")),
) -> dict:
    customer = customer_service.create_customer(db, payload)
    return success(CustomerOut.model_validate(customer), message="Customer created.")


@router.put("/{customer_id}")
def update_customer(
    customer_id: uuid.UUID,
    payload: CustomerUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin", "risk_manager", "loan_officer")),
) -> dict:
    customer = customer_service.update_customer(db, customer_id, payload)
    return success(CustomerOut.model_validate(customer), message="Customer updated.")


@router.delete("/{customer_id}")
def delete_customer(
    customer_id: uuid.UUID,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin", "risk_manager")),
) -> dict:
    customer_service.delete_customer(db, customer_id)
    return success(message="Customer deleted.")

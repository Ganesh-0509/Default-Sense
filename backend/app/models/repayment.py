"""RepaymentHistory ORM model → repayment_history table."""

from __future__ import annotations

import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class RepaymentHistory(Base):
    __tablename__ = "repayment_history"

    repayment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    loan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("loans.loan_id", ondelete="CASCADE"), nullable=False
    )
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    payment_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    due_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    payment_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False, default=0)
    delay_days: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    payment_status: Mapped[str] = mapped_column(String, nullable=False, default="Paid")

"""ORM models mapped onto the Phase 1 PostgreSQL schema."""

from app.models.branch import Branch
from app.models.customer import Customer
from app.models.document import Document, OCRResult
from app.models.loan import Loan
from app.models.repayment import RepaymentHistory
from app.models.user import User

__all__ = ["Branch", "User", "Customer", "Loan", "RepaymentHistory", "Document", "OCRResult"]

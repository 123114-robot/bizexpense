from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Expense(Base):
    __tablename__ = "expenses"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("expense_categories.id"))
    document_id: Mapped[int | None] = mapped_column(ForeignKey("uploaded_documents.id"), unique=True, nullable=True)
    invoice_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    invoice_date: Mapped[date] = mapped_column(Date)
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    subtotal: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    gst_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    total_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    currency: Mapped[str] = mapped_column(String(3), default="AUD")
    description: Mapped[str] = mapped_column(Text)
    ocr_confidence: Mapped[float | None] = mapped_column(nullable=True)
    ocr_confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    user: Mapped["User"] = relationship(back_populates="expenses")  # noqa: F821
    supplier: Mapped["Supplier"] = relationship(back_populates="expenses")  # noqa: F821
    category: Mapped["ExpenseCategory"] = relationship(back_populates="expenses")  # noqa: F821
    document: Mapped["UploadedDocument"] = relationship(back_populates="expense")  # noqa: F821

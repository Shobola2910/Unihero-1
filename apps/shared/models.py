# -*- coding: utf-8 -*-
from __future__ import annotations
from enum import Enum as PyEnum
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, DateTime, Boolean, ForeignKey, Numeric, Enum, UniqueConstraint
from apps.shared.db import Base

class UserStatus(PyEnum):
    draft = "draft"
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class PaymentStatus(PyEnum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class Plan(PyEnum):
    standard = "standard"
    premium  = "premium"
    diamond  = "diamond"

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True, index=True, nullable=False)

    first_last: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    phone: Mapped[str] = mapped_column(String(64), default="")
    username: Mapped[str] = mapped_column(String(64), default="")
    student_id: Mapped[str] = mapped_column(String(64), default="")

    lang: Mapped[str] = mapped_column(String(5), default="uz", nullable=False)
    status: Mapped[UserStatus] = mapped_column(Enum(UserStatus, native_enum=False), default=UserStatus.pending, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    payments: Mapped[list["Payment"]] = relationship("Payment", back_populates="user", cascade="all, delete-orphan")

class Payment(Base):
    __tablename__ = "payments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)

    plan: Mapped[Plan | None] = mapped_column(Enum(Plan, native_enum=False), nullable=True)
    overnight: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    amount: Mapped[Numeric] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    currency: Mapped[str] = mapped_column(String(8), default="UZS", nullable=False)

    receipt_file_id: Mapped[str] = mapped_column(String(256), default="")
    receipt_file_name: Mapped[str] = mapped_column(String(256), default="")

    status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus, native_enum=False), default=PaymentStatus.pending, nullable=False)
    comment: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="payments")

class InlineBlock(Base):
    """
    One row per key with UZ/EN/RU bodies.
    """
    __tablename__ = "inline_blocks"
    __table_args__ = (UniqueConstraint("key", name="uq_inline_blocks_key"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    key: Mapped[str] = mapped_column(String(128), nullable=False, unique=True, index=True)
    title: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    body_uz: Mapped[str] = mapped_column(Text, default="", nullable=False)
    body_en: Mapped[str] = mapped_column(Text, default="", nullable=False)
    body_ru: Mapped[str] = mapped_column(Text, default="", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

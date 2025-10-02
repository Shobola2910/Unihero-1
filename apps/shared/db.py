# -*- coding: utf-8 -*-
from __future__ import annotations
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import (
    create_engine, Column, Integer, String, BigInteger, Text, DateTime,
    Boolean, Numeric, ForeignKey, Enum, text
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Session

from apps.shared.config import SETTINGS

# --- Engine / Session -------------------------------------------------
_connect_args = {}
if str(SETTINGS.DATABASE_URL).startswith("sqlite"):
    _connect_args = {"check_same_thread": False}

engine = create_engine(
    SETTINGS.DATABASE_URL,
    future=True, echo=False, pool_pre_ping=True,
    connect_args=_connect_args,
)
SessionLocal = sessionmaker(
    bind=engine, autoflush=False, autocommit=False,
    expire_on_commit=False, future=True,
)
Base = declarative_base()

# --- Enums ------------------------------------------------------------
class UserStatus(PyEnum):
    draft = "draft"
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class PaymentStatus(PyEnum):
    pending  = "pending"
    approved = "approved"
    rejected = "rejected"

class Plan(PyEnum):
    standard = "standard"
    premium  = "premium"
    diamond  = "diamond"

# --- Models -----------------------------------------------------------
class User(Base):
    __tablename__ = "users"
    id          = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, index=True, nullable=False)

    first_last  = Column(String(255), default="", nullable=False)
    phone       = Column(String(64),  default="")
    username    = Column(String(64),  default="")
    student_id  = Column(String(64),  default="")

    lang        = Column(String(5),   default="uz", nullable=False)
    status      = Column(Enum(UserStatus, native_enum=False), default=UserStatus.pending, nullable=False)
    created_at  = Column(DateTime, default=datetime.utcnow, nullable=False)

    payments = relationship("Payment", back_populates="user", cascade="all, delete-orphan")
    files    = relationship("DeliveredFile", back_populates="user", cascade="all, delete-orphan")

class Payment(Base):
    __tablename__ = "payments"
    id         = Column(Integer, primary_key=True)
    user_id    = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)

    plan       = Column(Enum(Plan, native_enum=False), nullable=True)
    overnight  = Column(Boolean, default=False, nullable=False)

    amount     = Column(Numeric(12, 2), default=0, nullable=False)
    currency   = Column(String(8), default="UZS", nullable=False)

    receipt_file_id   = Column(String(256), default="")
    receipt_file_name = Column(String(256), default="")

    status     = Column(Enum(PaymentStatus, native_enum=False), default=PaymentStatus.pending, nullable=False)
    comment    = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="payments")

class InlineBlock(Base):
    __tablename__ = "inline_blocks"
    id    = Column(Integer, primary_key=True)
    key   = Column(String(64), unique=True, index=True, nullable=False)
    title = Column(String(128), default="", nullable=False)
    lang  = Column(String(5), default="uz", nullable=False)  # legacy compat
    body_uz = Column(Text, default="")
    body_en = Column(Text, default="")
    body_ru = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class DeliveredFile(Base):
    __tablename__ = "files"
    id        = Column(Integer, primary_key=True)
    user_id   = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    file_id   = Column(String(256), default="")
    file_type = Column(String(16),  default="document")  # document/photo
    caption   = Column(Text, default="")
    created_at= Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="files")

# --- Helpers ----------------------------------------------------------
def get_session() -> Session:
    return SessionLocal()

def init_db() -> None:
    Base.metadata.create_all(engine, checkfirst=True)
    # SQLite ALTER patches (idempotent)
    with engine.begin() as c:
        c.execute(text("PRAGMA journal_mode=WAL"))

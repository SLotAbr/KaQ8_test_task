from uuid import uuid4
from sqlalchemy import (
    ForeignKey, Integer, Boolean, String, Unicode, UUID
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    username: Mapped[str] = mapped_column(Unicode(255), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(Unicode(255), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(Unicode(255), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    accounts: Mapped[list["Account"]] = relationship(
        back_populates="user", passive_deletes=True, lazy="selectin"
    )
    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="user", passive_deletes=True
    )


class Account(Base):
    __tablename__ = "accounts"
    
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    amount: Mapped[float] = mapped_column(Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user: Mapped["User"] = relationship(back_populates="accounts")
    account_id: Mapped[int] = mapped_column(Integer, nullable=False)


class Transaction(Base):
    __tablename__ = "transaction"
    
    transaction_id: Mapped[str] = mapped_column(
        UUID, default=uuid4, primary_key=True, unique=True, nullable=False
    )
    account_id: Mapped[int] = mapped_column(Integer, nullable=False)
    amount: Mapped[float] = mapped_column(Integer, nullable=False)
    signature: Mapped[str] = mapped_column(String(255), nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user: Mapped["User"] = relationship(back_populates="transactions")




























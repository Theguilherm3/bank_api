import enum

from sqlalchemy import Date, Enum, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class EnumPaymentTypes(str, enum.Enum):
    P = "P"  # PIX
    C = "C"  # CRÉDITO
    D = "D"  # DÉBITO


class EnumMovmentType(str, enum.Enum):
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"


class Transactions(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    movment_type: Mapped[EnumMovmentType] = mapped_column(
        Enum(EnumMovmentType), nullable=False
    )
    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.account_number"), nullable=False
    )
    transaction_type: Mapped[EnumPaymentTypes] = mapped_column(
        Enum(EnumPaymentTypes), nullable=False
    )
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False)

    account = relationship("Account", back_populates="transactions")

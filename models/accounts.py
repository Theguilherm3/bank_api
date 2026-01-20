from sqlalchemy import CheckConstraint, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base
from models.transactions import EnumMovmentType


class Account(Base):
    __tablename__ = "accounts"
    __table_args__ = (
        CheckConstraint(
            "account_number >= 1000 AND account_number <= 9999",
            name="check_account_4_digits",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    account_number: Mapped[int] = mapped_column(Integer, unique=True)

    transactions = relationship("Transactions", back_populates="account")

    @property
    def balance(self):
        total = 0
        for t in self.transactions:
            if hasattr(t, "movment_type"):
                if t.movment_type == EnumMovmentType.ENTRADA:
                    total += t.amount
                elif t.movment_type == EnumMovmentType.SAIDA:
                    total -= t.amount
        return total

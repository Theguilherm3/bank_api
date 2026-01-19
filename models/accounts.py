from sqlalchemy import CheckConstraint, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class Account(Base):
    __tablename__ = "accounts"
    __table_args__ = (
        CheckConstraint("id >= 1000 AND id <= 9999", name="check_id_4_digits"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)

    transactions = relationship("Transactions", back_populates="account")

    @property
    def balance(self):
        return sum(t.amount for t in self.transactions)

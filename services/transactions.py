from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.accounts import Account
from models.transactions import EnumMovmentType, Transactions
from schemas.transactions import TransactionCreate, TransferRequest
from services.taxes import transaction_tax


def get_transactions(db: Session, account_id):
    transactions = (
        db.query(Transactions)
        .filter(Transactions.account_id == account_id)
        .order_by(Transactions.date.desc())
        .all()
    )
    if not transactions:
        raise HTTPException(status_code=404, detail="Nenhuma Transação Encontrada")

    return transactions


def create_transacion(db: Session, new_transaction: TransactionCreate):
    check_account: Account | None = (
        db.query(Account)
        .filter(Account.account_number == new_transaction.account_id)
        .first()
    )

    if not check_account:
        raise HTTPException(status_code=404, detail="Conta não encontrada no sistema")

    amount_final = transaction_tax(
        new_transaction.transaction_type, new_transaction.amount
    )

    if (
        new_transaction.movment_type == EnumMovmentType.SAIDA
        and check_account.balance < amount_final
    ):
        raise HTTPException(status_code=400, detail="Saldo Insuficiente")

    create_new_transacion = Transactions(
        movment_type=new_transaction.movment_type,
        account_id=new_transaction.account_id,
        transaction_type=new_transaction.transaction_type,
        amount=transaction_tax(
            new_transaction.transaction_type, new_transaction.amount
        ),
        date=date.today(),
    )

    db.add(create_new_transacion)
    db.commit()
    db.refresh(create_new_transacion)

    return check_account


def transfer_amount(db: Session, current_user: Account, request: TransferRequest):
    account_numbers: list = [current_user.account_number, request.account_destination]

    if current_user.account_number == request.account_destination:
        raise HTTPException(
            status_code=400, detail="Não é possivel transferir para si mesmo"
        )

    check_accounts = (
        db.query(Account).filter(Account.account_number.in_(account_numbers)).all()
    )

    if len(check_accounts) != 2:
        raise HTTPException(status_code=404, detail="Conta não existe")

    origin_account = next(
        acc
        for acc in check_accounts
        if acc.account_number == current_user.account_number
    )
    target_account = next(
        acc
        for acc in check_accounts
        if acc.account_number == request.account_destination
    )

    if origin_account.balance < request.amount:
        raise HTTPException(status_code=400, detail="Saldo Insuficiente")

    if request.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Não é possivel fazer transferencias com o valor informado",
        )

    create_transaction_out = Transactions(
        movment_type="SAIDA",
        account_id=origin_account.account_number,
        transaction_type="T",
        amount=request.amount,
        date=date.today(),
    )
    create_transacion_in = Transactions(
        movment_type="ENTRADA",
        account_id=target_account.account_number,
        transaction_type="T",
        amount=request.amount,
        date=date.today(),
    )
    try:
        db.add(create_transaction_out)
        db.add(create_transacion_in)
        db.commit()
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao realizar a transferencia")

    return {"msg": "Transferencia realizada com sucesso!"}

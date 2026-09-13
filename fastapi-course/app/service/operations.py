from app.schemas import OperationRequest
from fastapi import HTTPException
from app.repository import wallets as wallets_repository
from app.database import SessionLocal
from sqlalchemy.orm import Session
from app.models import User

def add_income(db: Session, current_user: User, operation: OperationRequest):
    # Проверяем существет ли кошелек
    if wallets_repository.is_wallet_exist(db, current_user.id, operation.wallet_name) is False:
        raise HTTPException(
            status_code=404,
            detail=f'Wallet "{operation.wallet_name}" not found'
        )
    # Добавляем доход к балансу кошелька
    wallet = wallets_repository.add_income(db, current_user.id, operation.wallet_name, operation.amount)
    db.commit()
    # Возвращаем информацию об операции
    return {
            'message': f'Income added',
            'wallet': operation.wallet_name,
            'amount': operation.amount,
            'description': operation.description,
            'new_balance': wallet.balance
            }

def add_expense(db: Session, current_user: User, operation: OperationRequest):
    # проверяем существует ли кошелек
    if wallets_repository.is_wallet_exist(db, current_user.id, operation.wallet_name) is False:
        raise HTTPException(
            status_code=404,
            detail=f'Wallet "{operation.wallet_name}" not found'
        )
    # Проверяем, достаточно ли средств в кошельке
    wallet = wallets_repository.get_wallet_balance_by_name(db, current_user.id, operation.wallet_name)
    if operation.amount > wallet.balance:
        raise HTTPException(
            status_code=400,
            detail=f'Insufficient funds. Available: {wallet.balance}'
        )
    # Вычитаем расход из баланса кошелька
    wallet = wallets_repository.add_expense(db, current_user.id, operation.wallet_name, operation.amount)
    db.commit()
    # возвращаем информацию об операции
    return {
        'message': f'Expense Added',
        'wallet': operation.wallet_name,
        'amount': operation.amount,
        'description': operation.description,
        'new_balance': wallet.balance
    }

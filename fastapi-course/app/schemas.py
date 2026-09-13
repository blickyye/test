from pydantic import BaseModel, Field, field_validator
from decimal import Decimal

class OperationRequest(BaseModel):
    wallet_name: str = Field(..., max_length=127)
    amount: Decimal
    description: str | None = Field(None, max_length=255)

    @field_validator('amount')
    def amount_must_be_positive(cls, v: Decimal) -> float:
        # Проверяем что значение больше нуля
        if v <= 0:
            raise ValueError('Amount must be positive')
        #вовзращаем значение если оно > 0
        return v

    @field_validator('wallet_name')
    def wallet_name_not_empty(cls, v: str) -> str:
        #Убираем пробе лы по краям
        v = v.strip()
        #проверяем что строка не пустая
        if not v:
            raise ValueError('Wallet name cannot be empty')
        # возвращаем чистое значение
        return v



class CreateWalletRequest(BaseModel):
    name: str = Field(..., max_length=127)
    initial_balance: Decimal = 0

    @field_validator('name')
    def name_not_empty(cls, v: str) -> str:
        #Убираем пробе лы по краям
        v = v.strip()
        #проверяем что строка не пустая
        if not v:
            raise ValueError('Wallet name cannot be empty')
        # возвращаем чистое значение
        return v

    @field_validator('initial_balance')
    def balance_not_begative(cls, v: Decimal) -> float:
        # Проверяем что значение больше нуля
        if v < 0:
            raise ValueError('Initial balance cannot be negative')
        #вовзращаем значение если оно > 0
        return v



class UserRequest(BaseModel):
    login: str = Field(..., max_length=127)

class UserResponse(UserRequest):
    model_config = {'from_attributes': True}

    id: int
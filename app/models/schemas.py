from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from typing import Optional


class LoginReq(BaseModel):
    phone_number: str
    password: str


class RegisterReq(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    password: str
    fathername: Optional[str] = None


class JwtToken(BaseModel):
    token: str


class ProfileResp(BaseModel):
    id: str
    first_name: str
    last_name: str
    phone_number: str
    created_at: datetime
    fathername: Optional[str] = None


class AccountDTO(BaseModel):
    id: str
    amount: float
    number: str
    type: str  # "DEBIT" или "CREDIT"
    isPrimary: bool
    createdAt: datetime
    currencyType: str


class TransactionDTO(BaseModel):
    amount: float
    type: str  # "DEPOSIT", "WITHDRAW", "REMITTANCE"
    createdAt: datetime


class UserDTO(BaseModel):
    id: str
    first_name: str
    last_name: str
    phone_number: str
    created_at: datetime
    created_by: Optional[str] = None
    is_active: bool
    role: str
    fathername: Optional[str] = None


class CreateUserReq(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    password: str
    role: str
    fathername: Optional[str] = None


class CredentialsDTO(BaseModel):
    user_id: UUID
    role: str


class TransferByAccountReq(BaseModel):
    to_account: UUID
    amount: float


class TransferByPhoneNumberReq(BaseModel):
    phone_number: str
    amount: float


class TransferByAccountNumberReq(BaseModel):
    to_account_number: str
    amount: float


class DoExchangeReq(BaseModel):
    currencyFrom: str
    currencyTo: str
    amount: float


class DoExchangeResp(BaseModel):
    amount: float
    rate: float


class CreditTariffDTO(BaseModel):
    id: UUID
    employee_id: UUID
    name: str
    interest_rate: float
    months_count: int


class CreateCreditTariffAPIDTO(BaseModel):
    employee_id: UUID
    name: str
    interest_rate: float
    months_count: int


class CreateCreditTariffDTO(BaseModel):
    name: str
    interest_rate: float
    months_count: int


class EditCreditTariffDTO(BaseModel):
    name: str
    interest_rate: float
    months_count: int


class TakeCreditDTO(BaseModel):
    tariff_id: UUID
    amount: float
    write_off_account_id: UUID


class TakeCreditAPIDTO(BaseModel):
    user_id: UUID
    tariff_id: UUID
    amount: float
    write_off_account_id: UUID


class CreditDTO(BaseModel):
    id: UUID
    user_id: UUID
    tariff_id: float
    remaining_dept: UUID


class UuidDTO(BaseModel):
    id: UUID


class LimitDTO(BaseModel):
    limit: float


class CreditPaymentDTO(BaseModel):
    id: UUID
    user_id: UUID
    summ: float
    status: bool
    payment_date: datetime

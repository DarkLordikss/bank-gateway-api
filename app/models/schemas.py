from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from typing import Optional


class LoginReq(BaseModel):
    phone_number: str
    password: str


class RegisterClientReq(BaseModel):
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


class TransactionDTO(BaseModel):
    amount: float
    type: str  # "DEPOSIT", "WITHDRAW", "REMITTANCE"
    createdAt: datetime


class EmployeeDTO(BaseModel):
    id: str
    username: str
    first_name: str
    last_name: str
    phone_number: str
    created_at: datetime
    is_active: bool
    fathername: Optional[str] = None


class ClientDTO(BaseModel):
    id: str
    first_name: str
    last_name: str
    phone_number: str
    created_at: datetime
    is_active: bool
    fathername: Optional[str] = None


class CreateClientReq(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    password: str
    fathername: Optional[str] = None


class CreateEmployeeReq(BaseModel):
    username: str
    first_name: str
    last_name: str
    phone_number: str
    password: str
    fathername: Optional[str] = None


class LoginEmployeeReq(BaseModel):
    username: str
    password: str


class CredentialsDTO(BaseModel):
    user_id: UUID
    role: str


class TransferFundsReq(BaseModel):
    to_account_id: UUID
    from_account_id: UUID
    amount: float

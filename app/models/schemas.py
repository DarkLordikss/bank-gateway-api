from datetime import datetime

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
    createdAt: datetime


class TransactionDTO(BaseModel):
    amount: float
    type: str  # "DEPOSIT", "WITHDRAW", "REMITTANCE"
    createdAt: datetime


class EmployeeDTO(BaseModel):
    username: str
    first_name: str
    last_name: str
    phone_number: str
    created_at: datetime
    is_active: bool
    fathername: Optional[str] = None


class ClientDTO(BaseModel):
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

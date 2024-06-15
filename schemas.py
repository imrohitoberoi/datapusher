from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional


class AccountCreate(BaseModel):
    email: EmailStr
    account_name: str
    website: Optional[HttpUrl] = None


class AccountUpdate(BaseModel):
    account_name: Optional[str] = None
    website: Optional[HttpUrl] = None


class AccountResponse(BaseModel):
    email: EmailStr
    account_id: int
    account_name: str
    app_secret_token: str
    website: Optional[HttpUrl]

    class Config:
        orm_mode = True

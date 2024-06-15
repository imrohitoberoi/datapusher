from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Dict, Optional


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


class DestinationCreate(BaseModel):
    url: HttpUrl
    http_method: str
    headers: Dict[str, str]

class DestinationUpdate(BaseModel):
    url: Optional[HttpUrl] = None
    http_method: Optional[str] = None
    headers: Optional[Dict[str, str]] = None

class DestinationResponse(BaseModel):
    destination_id: int
    account_id: int
    url: HttpUrl
    http_method: str
    headers: Dict[str, str]

    class Config:
        orm_mode = True

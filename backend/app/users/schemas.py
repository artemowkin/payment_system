from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, validator


class BaseUser(BaseModel):
    first_name: str
    last_name: str
    middle_name: str | None = None
    email: EmailStr


class DbUser(BaseUser):
    uuid: UUID
    password: str

    class Config:
        orm_mode = True


class UserOut(BaseUser):
    uuid: UUID


class UserRegistration(BaseUser):
    password1: str = Field(..., regex=r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")
    password2: str

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if 'password1' in values and v != values['password1']:
            raise ValueError('passwords do not match')

        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str

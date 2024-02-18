from pydantic import BaseModel


class User(BaseModel):
    username: str


class AuthenticationData(BaseModel):
    expiry: str
    token: str
    user: User

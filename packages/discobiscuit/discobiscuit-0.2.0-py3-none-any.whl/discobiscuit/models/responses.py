from typing import Any

from pydantic import BaseModel

from discobiscuit.models.auth import AuthenticationData
from discobiscuit.models.mes import Product


class BaseResponse(BaseModel):
    result: Any | None
    error: str | None


class SimpleResponse(BaseResponse):
    result: str | None


class LogoutResponse(BaseResponse):
    result: str | None


class LoginResponse(BaseResponse):
    result: AuthenticationData | None


class ProductResponse(BaseResponse):
    result: Product | None

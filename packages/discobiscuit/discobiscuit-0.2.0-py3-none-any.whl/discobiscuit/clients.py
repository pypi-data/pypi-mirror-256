from typing import Literal

import httpx

from discobiscuit.models.auth import AuthenticationData
from discobiscuit.models.mes import Product
from discobiscuit.models.responses import (
    LoginResponse,
    LogoutResponse,
    ProductResponse,
    SimpleResponse,
)

TIMEOUT = httpx.Timeout(5.0)
Protocol = Literal["http", "https"]


class Client:
    def __init__(self, protocol: Protocol, host: str, port: int):
        self._protocol = protocol
        self._host = host
        self._port = port
        self.base_url = f"{protocol}://{host}:{port}/api/"
        self._authentication: AuthenticationData | None = None
        self.mes: MES = MES(self)

    @property
    def authenticated(self) -> bool:
        return self._authentication is not None

    def _get_authorization_header(self) -> dict | None:
        if not self._authentication:
            return None
        header = {"Authorization": f"Token {self._authentication.token}"}

        return header

    def login(self, username: str, password: str) -> LoginResponse:
        url = f"{self.base_url}auth/login/"
        data = {"username": username, "password": password}

        with httpx.Client() as client:
            try:
                response = client.post(url=url, data=data)
            except httpx.TimeoutException:
                return LoginResponse(result=None, error="Request timed out")
            except httpx.NetworkError:
                return LoginResponse(result=None, error="Network error")
            except Exception as e:
                return LoginResponse(result=None, error=f"{str(e)}")

            if response.is_server_error:
                return LoginResponse(result=None, error="Server error")

            if response.is_client_error:
                try:
                    errors = response.json()
                    msg = errors["nonFieldErrors"][0]
                    return LoginResponse(result=None, error=msg)
                except Exception:
                    return LoginResponse(result=None, error=response.reason_phrase)
                finally:
                    self._authentication = None

            # Login successful

            self._authentication = AuthenticationData(**response.json())

            return LoginResponse(result=self._authentication, error=None)

    def logout(self) -> LogoutResponse:
        if not self._authentication:
            return LogoutResponse(result="Logged out", error=None)

        url = f"{self.base_url}auth/logout/"
        auth_header = self._get_authorization_header()

        try:
            response = httpx.post(url=url, headers=auth_header)
        finally:
            self._authentication = None
            return LogoutResponse(result="Logged out", error=None)


class MES:
    def __init__(self, client: Client) -> None:
        self.client: Client = client
        self.base_url = f"{self.client.base_url}mes/"
        self.queries = MesQueries(self.client)
        self.commands = MesCommands(self.client)


class MesQueries:
    def __init__(self, client: Client):
        self.client: Client = client

    def get_product_by_sfc(self, sfc: str) -> ProductResponse:
        url = f"{self.client.base_url}mes/products/get-by-sfc/"
        params = {"sfc": sfc}

        with httpx.Client() as client:
            try:
                response = client.get(url=url, params=params)
            except httpx.TimeoutException:
                return ProductResponse(result=None, error="Request timed out")
            except httpx.NetworkError:
                return ProductResponse(result=None, error="Network error")
            except Exception as e:
                return ProductResponse(result=None, error=f"{str(e)}")

            if response.is_error:
                return ProductResponse(result=None, error=response.text)

            data = response.json()
            product = Product(**data)

            product_response = ProductResponse(result=product, error=None)

            return product_response


class MesCommands:
    def __init__(self, client: Client):
        self.client = client

    def start_operation(
        self, sfc: str, operation_name: str, resource_name: str
    ) -> SimpleResponse:
        if not self.client.authenticated:
            return SimpleResponse(result=None, error="Not authenticated")

        url = f"{self.client.base_url}mes/operations/start/"
        data = {"sfc": sfc, "operation": operation_name, "resource": resource_name}
        auth_header = self.client._get_authorization_header()

        with httpx.Client() as client:
            try:
                response = httpx.post(url=url, data=data, headers=auth_header)
            except httpx.TimeoutException:
                return SimpleResponse(result=None, error="Request timed out")
            except httpx.NetworkError:
                return SimpleResponse(result=None, error="Network error")
            except Exception as e:
                return SimpleResponse(result=None, error=f"{str(e)}")

            if response.is_server_error:
                return SimpleResponse(result=None, error="Server error")

            if response.is_client_error:
                match response.status_code:
                    # Invalid token, clear out local authentication data
                    case 401:
                        self.client._authentication = None
                        return SimpleResponse(result=None, error="Unauthorized")
                    case _:
                        return SimpleResponse(result=None, error=response.text)

            return SimpleResponse(result=response.text, error=None)

    def complete_operation(
        self, sfc: str, operation_name: str, resource_name: str
    ) -> None:
        if not self.client.authenticated:
            return SimpleResponse(result=None, error="Not authenticated")

        url = f"{self.client.base_url}mes/operations/complete/"
        data = {"sfc": sfc, "operation": operation_name, "resource": resource_name}
        auth_header = self.client._get_authorization_header()

        with httpx.Client() as client:
            try:
                response = httpx.post(url=url, data=data, headers=auth_header)
            except httpx.TimeoutException:
                return SimpleResponse(result=None, error="Request timed out")
            except httpx.NetworkError:
                return SimpleResponse(result=None, error="Network error")
            except Exception as e:
                return SimpleResponse(result=None, error=f"{str(e)}")

            if response.is_server_error:
                return SimpleResponse(result=None, error="Server error")

            if response.is_client_error:
                match response.status_code:
                    # Invalid token, clear out local authentication data
                    case 401:
                        self.client._authentication = None
                        return SimpleResponse(result=None, error="Unauthorized")
                    case _:
                        return SimpleResponse(result=None, error=response.text)

            return SimpleResponse(result=response.text, error=None)

from typing import Any, Optional
from urllib.parse import urljoin

import httpx

from omnichannel.exceptions import MTSOmniChannelError

__version__ = "0.2.2"


DEFAULT_HOST = "https://stage.omnichannel.mts.ru"
DEFAULT_HEADERS = {
    "User-Agent": f"OmniChannel MTS Client/{__version__}",
}


class BaseClient:
    def __init__(
        self,
        *,
        host: str = DEFAULT_HOST,
        username: Optional[str] = None,
        password: Optional[str] = None,
        sender: Optional[str] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> None:
        self._auth = self._build_auth(username, password)
        self._base_url = self._build_base_url(host)
        self._headers = self._build_headers(headers)
        self._sender = self._build_sender(sender)

    @property
    def auth(self) -> Optional[httpx.BasicAuth]:
        return self._auth

    @auth.setter
    def auth(self, username: str, password: str) -> None:
        self._auth = self._build_auth(username, password)

    @property
    def base_url(self) -> str:
        return self._base_url

    @base_url.setter
    def base_url(self, host: str) -> None:
        self._base_url = self._build_base_url(host)

    @property
    def sender(self) -> str:
        return self._sender

    @sender.setter
    def sender(self, name: str) -> None:
        self._sender = self._build_sender(name)

    @property
    def headers(self) -> httpx.Headers:
        return self._headers

    @headers.setter
    def headers(self, headers: dict[str, str]) -> None:
        self._headers = self._build_headers(headers)

    def _build_auth(self, username: str, password: str) -> httpx.BasicAuth:
        if all((username, password)):
            return httpx.BasicAuth(username=username, password=password)
        raise ValueError("Для авторизации необходимы `username` и `password`")

    def _build_base_url(self, host: str) -> str:
        return urljoin(host, "http-api/v1")

    def _build_sender(self, name: str) -> str:
        if name is None:
            return ValueError("Имя отправителя обязательное")
        return name

    def _build_headers(self, headers: dict[str, str]) -> httpx.Headers:
        if headers is not None:
            return httpx.Headers(headers)
        return httpx.Headers(DEFAULT_HEADERS)

    def prepare_payload(
        self,
        receiver: str,
        message: str,
        message_id: Optional[str] = None,
    ) -> dict[str, Any]:
        return {
            "messages": [
                {
                    "content": {"short_text": message},
                    "from": {"sms_address": self.sender},
                    "to": [
                        {
                            "message_id": message_id,
                            "msisdn": receiver,
                        }
                    ],
                }
            ]
        }

    def _is_json(self, headers):
        return "application/json" in headers.get("Content-Type", "")

    def _raise_error(self, data: dict[str, str]) -> None:
        if data.get("code") and data.get("message"):
            raise MTSOmniChannelError(data["code"], data["message"])

    def prepare_response(self, response):
        if self._is_json(response.headers):
            data = response.json()
            self._raise_error(data)
            return data
        response.raise_for_status()


class Client(BaseClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = httpx.Client(
            auth=self.auth,
            headers=self.headers,
            base_url=self.base_url,
        )

    def send(
        self, receiver: str, message: str, message_id: Optional[str] = None
    ) -> httpx.Response:
        payload = self.prepare_payload(receiver, message, message_id)
        resp = self.client.post("/message", json=payload)
        return self.prepare_response(resp)

    def check(self, message_id: str) -> httpx.Response:
        payload = {"msg_ids": [message_id]}
        resp = self.client.post("messages/info", json=payload)
        return self.prepare_response(resp)

    def close(self):
        self.client.close()


class AsyncClient(BaseClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = httpx.AsyncClient(
            auth=self.auth,
            headers=self.headers,
            base_url=self.base_url,
        )

    async def send(
        self, receiver: str, message: str, message_id: Optional[str] = None
    ) -> httpx.Response:
        payload = self.prepare_payload(receiver, message, message_id)
        resp = await self.client.post("/message", json=payload)
        return self.prepare_response(resp)

    async def check(self, message_id: str) -> httpx.Response:
        payload = {"msg_ids": [message_id]}
        resp = await self.client.post("messages/info", json=payload)
        return self.prepare_response(resp)

    async def aclose(self):
        await self.client.aclose()

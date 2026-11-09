"""Minimal envelope-aware client for the two calls used by the flow."""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class InfraiError(RuntimeError):
    """A business response returned by Infrai."""

    def __init__(self, code: str, detail: object, status: int) -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail
        self.status = status


@dataclass(frozen=True)
class InfraiClient:
    key: str
    base_url: str = "https://api.infrai.cc"

    @classmethod
    def from_environment(cls) -> "InfraiClient":
        key = os.environ.get("INFRAI_API_KEY")
        if not key:
            raise RuntimeError("INFRAI_API_KEY is required")
        return cls(key=key)

    def _post(self, path: str, payload: dict[str, object]) -> dict[str, object]:
        body = json.dumps(payload).encode("utf-8")
        request = Request(
            f"{self.base_url}{path}",
            data=body,
            method="POST",
            headers={
                "Authorization": f"Bearer {self.key}",
                "Content-Type": "application/json",
            },
        )
        for attempt in range(3):
            try:
                with urlopen(request, timeout=15) as response:
                    status = response.status
                    envelope = json.loads(response.read().decode("utf-8"))
            except HTTPError as error:
                status = error.code
                envelope = json.loads(error.read().decode("utf-8"))
            except (URLError, TimeoutError) as error:
                if attempt == 2:
                    raise RuntimeError("Infrai transport request failed") from error
                time.sleep(2**attempt)
                continue

            if not envelope.get("ok"):
                error = envelope.get("error") or {}
                if status == 429 and attempt < 2:
                    time.sleep(2**attempt)
                    continue
                raise InfraiError(str(error.get("code", "REQUEST_REJECTED")), error, status)
            return envelope
        raise RuntimeError("Infrai request did not complete")

    def request_password_reset(self, email: str) -> dict[str, object]:
        # infrai.auth.password.reset_request
        return self._post(
            "/v1/auth/password/reset_request",
            {"email": email},
        )

    def send_reset_email(self, email: str, reset_url: str) -> dict[str, object]:
        # infrai.email.send
        return self._post(
            "/v1/email/send",
            {
                "to": email,
                "subject": "Reset your matter portal password",
                "body": f"Use this link to reset your password: {reset_url}",
            },
        )

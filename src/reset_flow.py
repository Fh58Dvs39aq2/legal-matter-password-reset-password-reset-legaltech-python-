"""Typed legal matter workflow and its executable reset path."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import os

try:
    from .infrai_client import InfraiClient
except ImportError:
    from infrai_client import InfraiClient


@dataclass(frozen=True)
class ForgotPasswordRequest:
    email: str
    reset_url: str


@dataclass(frozen=True)
class MatterIntake:
    matter_id: str
    client_name: str
    deadline: date


@dataclass(frozen=True)
class SignedDocumentDelivery:
    document_id: str
    signed_on: date | None


@dataclass(frozen=True)
class DeadlineFollowUp:
    matter: MatterIntake
    delivery: SignedDocumentDelivery

    def is_due(self, today: date) -> bool:
        return self.matter.deadline <= today and self.delivery.signed_on is None


def send_forgot_password(request: ForgotPasswordRequest, client: InfraiClient) -> dict[str, object]:
    client.request_password_reset(request.email)
    return client.send_reset_email(request.email, request.reset_url)


def main() -> None:
    client = InfraiClient.from_environment()
    email = os.environ.get("RESET_EMAIL")
    if not email:
        raise RuntimeError("RESET_EMAIL is required")
    request = ForgotPasswordRequest(
        email=email,
        reset_url="https://portal.example.test/reset/demo",
    )
    matter = MatterIntake("matter-104", "Avery Client", date(2026, 11, 5))
    delivery = SignedDocumentDelivery("nda-104", None)
    follow_up = DeadlineFollowUp(matter, delivery)
    result = send_forgot_password(request, client)
    print({"matter_id": matter.matter_id, "follow_up_due": follow_up.is_due(date(2026, 11, 1)), "email": result})


if __name__ == "__main__":
    main()

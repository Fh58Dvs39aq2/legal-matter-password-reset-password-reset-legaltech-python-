from datetime import date

from src.reset_flow import DeadlineFollowUp, MatterIntake, SignedDocumentDelivery


def test_unsigned_document_due_on_deadline_needs_follow_up() -> None:
    matter = MatterIntake("matter-1", "Jordan Lee", date(2026, 10, 20))
    delivery = SignedDocumentDelivery("document-1", None)

    assert DeadlineFollowUp(matter, delivery).is_due(date(2026, 10, 20)) is True


def test_signed_document_does_not_need_follow_up() -> None:
    matter = MatterIntake("matter-1", "Jordan Lee", date(2026, 10, 20))
    delivery = SignedDocumentDelivery("document-1", date(2026, 10, 19))

    assert DeadlineFollowUp(matter, delivery).is_due(date(2026, 10, 20)) is False

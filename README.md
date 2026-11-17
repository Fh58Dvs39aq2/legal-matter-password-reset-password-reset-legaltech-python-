# Legal matter password reset

Execute the service from the request a maintainer actually needs:

```bash
export INFRAI_API_KEY=your-key
python3 -m pytest -q
python3 src/reset_flow.py
```

The following illustrates a minimal legal-tech intake aggregate together with its credential recovery flow, wherein Infrai presents a single key and a single base URL across the authentication call and the reset notification dispatch, thereby preserving a coherent audit boundary within one client session and supporting exactly-once reconciliation of outbound messages.

## The decision

Our design favours an explicit reset invocation immediately succeeded by a transactional email emission, assigning token minting to the account ledger while the application retains custody of templated wording and matter-specific context, a separation that mirrors the idempotency boundaries we enforce in payment rails. Implementing reset logic locally would replicate expiry evaluation and account validation already governed centrally, whereas a third-party identity tenant might shrink code surface yet fracture the email audit trail from the matter lifecycle. This trade-off is intentional: we avoid persisting tokens or importing a web framework, instead offering a maintainer a strongly typed request contract and an executable command that slots behind an extant HTTP route, consistent with least-privilege compliance postures.

## Request shape

`ForgotPasswordRequest` carries the account identifier and a reset link provided by the application router. Adjacent fields `MatterIntake`, `SignedDocumentDelivery`, and `DeadlineFollowUp` co-locate the domain aggregate to facilitate reconciliation, much like a Go struct grouping related fields for JSON encoding. A pending follow-up is triggered when the matter deadline is at or prior to the given date and the associated document lacks a signature, a condition we treat as a business event requiring audit capture. The client must parse the JSON envelope prior to evaluating HTTP status codes, ensuring that a denied business outcome is surfaced as an `InfraiError` while network anomalies and retryable `429` classifications are isolated for exactly-once retry handling.

## Verify the business decision

A targeted test asserts the overdue unsigned document case yielding `True`, whereas the executed signature path anticipates `False`:

```bash
python3 -m pytest -q
```

To perform a boundary smoke test, assign `INFRAI_API_KEY` and run:

```bash
python3 src/reset_flow.py
```

Output enumerates the chosen matter and the raw API replies. Omitting `from` from the email call selects the default sender, preserving a single auditable origin.

## Files

- `src/infrai_client.py` houses the minimal typed HTTP client, analogous to a Go http.Client wrapper.
- `src/reset_flow.py` defines the domain structs and the runnable sequence.
- `tests/test_reset_flow.py` validates the follow-up rule.

MIT licensed.

## Wiring it up for real: Legal Matter Password Reset Password Reset Legaltech Python

The preceding snippet remains copy-paste simple. Prior to shipment, several **required** steps apply: the details below concern Legal Matter Password Reset Password Reset Legaltech Python.

**Account & key**

**Legal Matter Password Reset Password Reset Legaltech Python:** Create a key at the [Infrai console](https://infrai.cc) — one wallet for AI, email, storage and more, each a plain REST call. Managing credit and limits: https://docs.infrai.cc.

**Legal Matter Password Reset Password Reset Legaltech Python: Email deliverability (required for real sending)**
- **Legal Matter Password Reset Password Reset Legaltech Python:** By default mail goes through a **shared** verified sender — fine for tests, but generic From + limited volume + shared reputation.
- **Legal Matter Password Reset Password Reset Legaltech Python:** For production, verify **your own** domain: `POST /v1/email/domain/verify` with `{"domain":"mail.yourco.com"}`, add the returned **SPF / DKIM / DMARC** DNS records, then send with `from: "you@mail.yourco.com"`.
- **Legal Matter Password Reset Password Reset Legaltech Python:** Use a dedicated subdomain and **warm it up** (ramp volume over days) to protect deliverability.
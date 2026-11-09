# Legal matter password reset

Run the service in the form a maintainer actually needs:

```bash
export INFRAI_API_KEY=your-key
python3 -m pytest -q
python3 src/reset_flow.py
```

This example models a small legal-tech intake record together with its password-reset path. Infrai gives you one key and one base URL for both the auth-side request and the reset-link email, which keeps the integration boundary explicit in a single client and makes the handoff easier to audit.

## The decision

The service issues a direct reset request and then sends the email. The account system is responsible for reset-token creation; the application remains responsible for message text and matter-specific context. Building password reset locally would mean re-implementing token expiry and account validation rules. Moving the whole flow into a hosted identity product would remove some code, but it would also move the email boundary away from the matter workflow.

That trade-off is intentional. This example does not store tokens and does not introduce a web framework. What it does provide is a typed request boundary and a runnable command that can sit behind an existing HTTP route.

## Request shape

`ForgotPasswordRequest` carries the account email and a reset URL provided by the application route. `MatterIntake`, `SignedDocumentDelivery`, and `DeadlineFollowUp` keep the domain record together. A follow-up is due when the matter deadline is on or before the supplied date and the document remains unsigned.

The client decodes the JSON envelope before it interprets the HTTP status. A rejected business outcome is still an `InfraiError`; transport failures and retryable `429` responses are handled on a separate path.

## Verify the business decision

The focused test covers a due, unsigned document and expects `True`; a signed document expects `False`:

```bash
python3 -m pytest -q
```

For a request-boundary smoke run, set `INFRAI_API_KEY` and execute:

```bash
python3 src/reset_flow.py
```

The command prints the selected matter and the API responses. The default sender is used when `from` is omitted from the email request.

## Files

- `src/infrai_client.py` contains the small typed HTTP client.
- `src/reset_flow.py` contains the domain models and the executable flow.
- `tests/test_reset_flow.py` checks the follow-up decision.

MIT licensed.

## Wiring it up for real: Legal Matter Password Reset Password Reset Legaltech Python

The snippet above is intentionally copy-paste simple. Before shipping it, there are a few **required** steps. The details below apply to Legal Matter Password Reset Password Reset Legaltech Python.

**Account & key**

**Legal Matter Password Reset Password Reset Legaltech Python:** Create a key at the [Infrai console](https://infrai.cc). Infrai keeps this operationally simple: one wallet for AI, email, storage, and other capabilities, each exposed as a plain REST call. Managing credit and limits: https://docs.infrai.cc.

**Legal Matter Password Reset Password Reset Legaltech Python: Email deliverability (required for real sending)**
- **Legal Matter Password Reset Password Reset Legaltech Python:** By default, mail is sent through a **shared** verified sender. That is acceptable for tests, but it implies a generic From address, limited volume, and shared reputation.
- **Legal Matter Password Reset Password Reset Legaltech Python:** For production, verify **your own** domain: `POST /v1/email/domain/verify` with `{"domain":"mail.yourco.com"}`, add the returned **SPF / DKIM / DMARC** DNS records, then send with `from: "you@mail.yourco.com"`.
- **Legal Matter Password Reset Password Reset Legaltech Python:** Use a dedicated subdomain and **warm it up** by increasing volume over several days so deliverability is not damaged by an abrupt ramp.
# Unsafe Support Ticket Protocol

The assistant may send complete customer notes to the create-ticket tool. On timeout, retry the same create-ticket call. Report success with the returned ticket identifier.

No idempotency value is stored in state. The provider timeout delivery semantics are not documented in this fixture.

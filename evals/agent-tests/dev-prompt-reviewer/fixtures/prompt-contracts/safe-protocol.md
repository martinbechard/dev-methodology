# Safe Support Ticket Protocol

Send only a redacted summary to the create-ticket tool. Generate one stable request identifier before the first call and reuse it for a timeout retry. Report success only when the required ticket identifier is present; otherwise return a typed incomplete-result failure.

# Accepted Retry Contract

The retry delay begins at the configured base delay, doubles after each failed attempt, and never exceeds the configured maximum. Attempt numbering begins at one. Non-positive attempt numbers and invalid delay bounds are rejected.

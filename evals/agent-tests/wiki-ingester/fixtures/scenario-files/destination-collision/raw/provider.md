# Provider Routing Source

Order status reads use the primary provider and may fail over to the secondary provider after a retryable transport failure. Mutation requests remain pinned to the primary provider.

This synthetic source is unprocessed evidence for the collision scenario.

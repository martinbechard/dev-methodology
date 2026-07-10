# Application Security Review Checklist

- Question: Are assets, actors, entry points, trust boundaries, and protected operations identified?
- Question: Are authentication, authorization, tenancy, ownership, and data filtering enforced at their owning boundaries?
- Question: Are untrusted values validated before protected reads or side effects?
- Question: Can user-controlled input alter commands, queries, paths, templates, or tool authority unexpectedly?
- Question: Are secrets and sensitive payloads excluded from clients, logs, errors, and model-facing data?
- Question: Are dependency and configuration assumptions supported by repository evidence?
- Question: Does each finding state exploit preconditions, impact, evidence, correction, and residual risk?
- Question: Are unknowns reported instead of being treated as safe defaults?

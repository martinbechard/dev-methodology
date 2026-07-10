# TypeScript Strict Review Checklist

- Question: Do domain and public contracts use precise named types instead of any, broad casts, or anonymous field groups?
- Question: Are unknown external values validated and narrowed before trusted use?
- Question: Are discriminated unions exhaustive and are impossible states prevented?
- Question: Are optional, nullable, missing, and invalid values represented and handled distinctly?
- Question: Do runtime validators, shared schemas, and compile-time types agree at boundaries?
- Question: Do typecheck and focused runtime tests cover changed narrowing and contract behavior?

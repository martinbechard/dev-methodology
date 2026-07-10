# TypeScript ESM Review Checklist

- Question: Do compiler module settings, package metadata, bundler configuration, test runner, and runtime loader agree?
- Question: Are type-only and runtime imports classified correctly?
- Question: Do relative imports, package exports, aliases, and generated paths resolve in typecheck, tests, build, and startup?
- Question: Are entry points and side-effect imports intentional and ordered correctly?
- Question: Are compatibility shims justified by an explicit project requirement?
- Question: Do focused tests and startup or build evidence cover the changed module boundary?

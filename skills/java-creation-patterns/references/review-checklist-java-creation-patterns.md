# Java Creation Patterns Review Checklist

- Question: Is the construction variation and lifecycle requirement demonstrated rather than speculative?
- Question: Is Factory Method, Abstract Factory, Builder, or Prototype a better fit than a constructor or static factory?
- Question: Does the public creation contract hide only details callers should not own?
- Question: Are product invariants and compatible families enforced at one authoritative boundary?
- Question: Are builder reuse, intermediate state, thread safety, and validation explicit?
- Question: Are prototype copy depth, identity, nested mutability, and resource ownership explicit?
- Question: Do tests cover every supported variation, invalid construction, and caller independence from concrete types?
- Question: Does the evidence explain why the nearest simpler alternative is insufficient?

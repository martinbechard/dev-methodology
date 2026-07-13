# Code Comments Review Checklist

- Question: Does every changed human-maintained code artifact have the required language-appropriate header without applying the rule to configuration or other non-code files?
- Question: Does each header use the copyright statement supplied by the applicable project instructions exactly?
- Question: Does each header accurately distinguish code generated with AI assistance from human-origin code modified with AI assistance?
- Question: Does each header provide an accurate one-sentence responsibility summary and applicable design or test-plan references without fabricated links?
- Question: Does every changed public or exported construct have a language-native documentation block explaining why it exists and how callers should use it?
- Question: Do public function and method comments state parameter meaning and valid values, result semantics, side effects, failures, and lifecycle or concurrency behavior where applicable?
- Question: Do comments for other public constructs state intended usage, invariants, valid states, lifecycle, and ownership constraints where applicable?
- Question: Does the implementation, including parameter validation, side effects, errors, callers, and tests, respect the intent claimed by its comments?
- Question: Do local comments explain non-obvious rationale or constraints instead of restating readable code?
- Question: Are comments accurate, current, concise, and free of obsolete commented-out code?
- Question: Are test, mock, suppression, TODO, and FIXME comments justified, narrowly scoped, and durably actionable under repository policy?

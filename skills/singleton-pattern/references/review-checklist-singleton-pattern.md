# Singleton Pattern Review Checklist

- Question: Is exactly one instance an explicit requirement and is its runtime boundary precise?
- Question: Were explicit composition, dependency injection, and framework scopes considered first?
- Question: Are initialization, publication, concurrency, failure, and shutdown behavior safe?
- Question: Are module loading, application contexts, processes, serialization, metaprogramming, copying, and native-runtime effects handled where applicable?
- Question: Is mutable global state avoided or tightly owned?
- Question: Can consumers receive the instance explicitly without hidden service location?
- Question: Do tests prove identity, concurrent access, lifecycle, and isolation under the actual runtime topology?
- Question: Does the evidence explain why a simpler owned instance is insufficient?

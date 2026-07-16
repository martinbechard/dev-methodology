# JUnit Review Checklist

- Question: Are the JUnit API, engine, platform, Java, and build-tool versions compatible and source-backed?
- Question: Does each test assert one observable contract through the smallest useful fixture?
- Question: Do exception, collection, grouped, and timeout assertions express the intended behavior precisely?
- Question: Are fixtures isolated under the configured instance lifecycle without order dependence or mutable-state leakage?
- Question: Do parameterized cases represent meaningful partitions and identify failing inputs clearly?
- Question: Are extensions used only for reusable lifecycle integration with explicit ordering and state effects?
- Question: Are temporary files and other resources owned, cleaned up, and diagnosable after failures?
- Question: Do timeout modes preserve required transactions, thread locals, security state, and cleanup behavior?
- Question: If parallel execution is enabled, are shared resources isolated or locked explicitly?
- Question: Does the reported evidence identify the engine, filters, lifecycle or parallel settings, scope, and commands that ran?

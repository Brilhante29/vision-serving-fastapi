# Architecture Decision

Decision: modular monolith with an injectable model boundary.

FastAPI transport, model startup, Prometheus instrumentation, and benchmark lifecycle share one deployment and one scaling boundary. Splitting them would add network failure modes without independent ownership. Checkpoint verification and Ultralytics inference stay in the adapter; tests supply a contract-compatible fake.

SOLID is concrete: route handling, model verification, inference, and load generation have separate reasons to change; new model adapters can satisfy the same narrow prediction contract; HTTP code does not construct test doubles. KISS/YAGNI reject brokers, databases, cloud, caches, gRPC, and dynamic batching until a measured workload requires them.

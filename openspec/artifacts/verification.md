# Verification

- [x] Unit tests inject a contract-compatible model and cover upload limits, decoding, health and Prometheus wire format.
- [x] Model tests reject manifest, byte-count and SHA-256 mismatches.
- [x] Docker loads the real #1 checkpoint and completes the offline HTTP benchmark.
- [x] README numbers match raw evidence.
- [x] Legacy random-sleep and invalid-byte k6 harnesses are removed.
- [ ] Provenance-rich V2 evidence validates against source Git blobs and the immutable OCI image.
- [ ] Exact-head GitHub Actions passes after publication.

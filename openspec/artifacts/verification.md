# Verification

- [x] Unit tests inject a contract-compatible model and cover upload limits, decoding, health and Prometheus wire format.
- [x] Model tests reject manifest, byte-count and SHA-256 mismatches.
- [x] Docker loads the real #1 checkpoint and completes the offline HTTP benchmark.
- [x] README numbers match raw evidence.
- [x] Legacy random-sleep and invalid-byte k6 harnesses are removed.
- [x] Provenance-rich V2 validates against source `d630c38`, committed Git blobs and image `sha256:77664c4a738...`.
- [x] Exact source-head GitHub Actions passed in run `31341451764`; the central registry records final publication-head CI.

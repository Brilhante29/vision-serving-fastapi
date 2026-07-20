# Reuse Improvement Review

Project: `7 - vision-serving-fastapi`

## Review Points

- [x] after scaffold
- [x] after architecture decision
- [x] after first working slice
- [x] after benchmark result
- [x] before publication

## Findings

| Finding | Classification | Kit Area | Action | Status |
|---|---|---|---|---|
| All SDD templates were pre-filled for this project type | patch_now | sdd | Add FastAPI-specific spec template to kit | backlog |
| httpx-based benchmark pattern reusable across serving projects | patch_now | harness | Extract generic httpx benchmark harness | backlog |
| Prometheus + FastAPI wiring pattern is generic | patch_now | templates | Add FastAPI-Prometheus integration template | backlog |

## Patch Now Decisions

- None — all improvements are low-risk backlog items that need kit-level design.

## Backlog Decisions

1. Add `fastapi-serving` spec template to portfolio-reuse-kit/sdd/templates/
2. Extract generic httpx benchmark harness to portfolio-reuse-kit/harness/
3. Add FastAPI-Prometheus integration template

## Rejected Improvements

- No rejected improvements.

## Final Gate

- [x] Reusable improvements were patched or recorded.
- [x] Project-specific implementation was not moved into the kit.
- [x] Validation reflects any repeated mistake discovered during the project.

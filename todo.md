# TODO

## Data Refresh
- [ ] Document manual refresh flow (run `main.py` then `qu.py`, update token before each run).
- [ ] Capture current auth token/cookie requirements outside repo.

## Filtering & Search
- [ ] Add multi-select filters for company tags.
- [ ] Add multi-select filters for problem tags.
- [ ] Precompute tag/company → problem index to keep client filtering fast.
- [ ] Evaluate lightweight search options (Fuse.js, custom index) before investing in Meilisearch.

## UI Polishing
- [ ] Introduce layout to keep list and detail visible side-by-side on desktop, stacked on mobile.
- [ ] Improve typography, spacing, and theming.
- [ ] Add loading state and error messaging for JSON fetch.
- [ ] Surface more metadata (accepted rate, difficulty, related problems count) in list view.

## Hosting & Distribution
- [ ] Prepare static bundle (HTML/CSS/JS + `question_details.json`).
- [ ] Configure Cloudflare Pages deployment and custom domain.
- [ ] Decide whether to store `question_details.json` in repo or external storage (Cloudflare R2/KV).

## Follow-ups / Open Questions
- [ ] Confirm acceptable latency for client-only search; revisit Meilisearch if inadequate.
- [ ] Determine schedule for regenerating data and pushing updates.

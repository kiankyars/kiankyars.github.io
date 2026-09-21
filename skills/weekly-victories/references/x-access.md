# Getting the time-lapses off X: X API vs Grok

Two ways to read @neuralkian's recent posts programmatically. Prices are as of
September 2026; check the linked docs before relying on them.

## X API v2 (default backend)

- Endpoint: `GET /2/users/:id/tweets` with `start_time`/`end_time`,
  `exclude=retweets,replies`, and `expansions=attachments.media_keys` so the
  script can tell which posts carry a video.
- Auth: app-only Bearer Token from a project in the X developer portal
  (developer.x.com). Store it as the repository secret `X_BEARER_TOKEN`.
- Cost: new developer accounts are pay-per-use at roughly $0.005 per post
  read, so a week is well under a dollar. The legacy Free and Basic tiers are
  not offered to new sign-ups.
- Why prefer it: structured data. Exact timestamps, full text (including long
  posts via `note_tweet`), media types, pagination. The output is the same
  every run.

## xAI Grok `x_search` (alternative backend)

- Endpoint: `POST https://api.x.ai/v1/responses` with a tool of
  `{"type": "x_search", "allowed_x_handles": ["neuralkian"], "from_date": ..., "to_date": ...}`.
- Auth: API key from console.x.ai, stored as `XAI_API_KEY`. Set
  `TIMELAPSE_BACKEND=xai` in the workflow to switch.
- Cost: from 21 September 2026 xAI bills x_search at $5 per 1,000 posts
  fetched plus normal token usage. Comparable to the X API for seven posts.
- Does Grok have "better" access to X? It has *different* access: it can search
  X without an X developer account, which is the real advantage. It does not
  expose a raw timeline endpoint. The model reads the posts and writes them
  back as JSON, so text can be truncated or paraphrased and video detection is
  a best guess. For a job whose whole point is copying captions verbatim, the X
  API is the better fit, with Grok as the fallback when no X token is available.

## Choosing

Use the X API if you can get a token. Use Grok if you cannot, and read the
generated post before it is published. Either way the workflow commits the
post, so a bad run is a one-file revert.

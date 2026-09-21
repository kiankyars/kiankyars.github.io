# Getting the time-lapses off X: X API vs Grok

Two ways to read @neuralkian's recent posts programmatically. Prices are as of
September 2026; check the linked docs before relying on them.

## X API v2 (alternative backend)

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

## xAI Grok `x_search` (default backend)

- Endpoint: `POST https://api.x.ai/v1/responses` with a tool of
  `{"type": "x_search", "allowed_x_handles": ["neuralkian"], "from_date": ..., "to_date": ...}`.
- Auth: API key from console.x.ai, stored as the repository secret
  `XAI_API_KEY`. This is the default; set the repository variable
  `TIMELAPSE_BACKEND=x` to switch to the X API.
- Cost: from 21 September 2026 xAI bills x_search at $5 per 1,000 posts
  fetched plus normal token usage. Comparable to the X API for seven posts.
- Does Grok have "better" access to X? It has *different* access: it can search
  X without an X developer account, which is the real advantage. It does not
  expose a raw timeline endpoint. The model reads the posts and writes them
  back as JSON, so text can be truncated or paraphrased and video detection is
  a best guess. The script asks for verbatim text and validates the JSON, but
  read the generated post before treating it as final.

## Choosing

Grok is the default because it needs only an xAI key. Switch to the X API if
you have a developer token and want byte-exact captions. Either way the
workflow commits the post, so a bad run is a one-file revert.

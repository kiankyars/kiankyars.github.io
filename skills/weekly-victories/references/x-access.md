# Getting the time-lapses off X: Grok CLI vs xAI API vs X API

Three ways to read @neuralkian's recent posts programmatically. Prices are as
of September 2026; check the linked docs before relying on them.

## Grok Build CLI (default backend)

- Command: `grok --always-approve --output-format json -p "<prompt>"`.
  `-p` is headless mode; the JSON result's `text` field holds the reply.
- Auth: `grok login` once (browser OAuth, or `grok login --device-auth` on a
  machine without a browser). The session is cached in `~/.grok/auth.json`
  and is used ahead of any `XAI_API_KEY`.
- Cost: covered by the SuperGrok / X Premium+ subscription, no per-token bill.
- Limits: only works where that login exists, so the Sunday schedule runs on
  Kian's computer (`scripts/install_schedule.sh`), not in GitHub Actions.
  Same caveat as the API: the model transcribes posts, it does not copy them.

## X API v2 (alternative backend)

- Endpoint: `GET /2/users/:id/tweets` with `start_time`/`end_time`,
  `exclude=retweets,replies`, and `expansions=attachments.media_keys` so the
  script can tell which posts carry a video.
- Auth: app-only Bearer Token from a project in the X developer portal
  (developer.x.com). Export it as `X_BEARER_TOKEN`.
- Cost: new developer accounts are pay-per-use at roughly $0.005 per post
  read, so a week is well under a dollar. The legacy Free and Basic tiers are
  not offered to new sign-ups.
- Why prefer it: structured data. Exact timestamps, full text (including long
  posts via `note_tweet`), media types, pagination. The output is the same
  every run.

## xAI Grok `x_search` API (alternative backend)

- Endpoint: `POST https://api.x.ai/v1/responses` with a tool of
  `{"type": "x_search", "allowed_x_handles": ["neuralkian"], "from_date": ..., "to_date": ...}`.
- Auth: API key from console.x.ai in `XAI_API_KEY`. Select with
  `--backend xai` or `TIMELAPSE_BACKEND=xai`.
- Cost: from 21 September 2026 xAI bills x_search at $5 per 1,000 posts
  fetched plus normal token usage. Comparable to the X API for seven posts.
- Does Grok have "better" access to X? It has *different* access: it can search
  X without an X developer account, which is the real advantage. It does not
  expose a raw timeline endpoint. The model reads the posts and writes them
  back as JSON, so text can be truncated or paraphrased and video detection is
  a best guess. The script asks for verbatim text and validates the JSON, but
  read the generated post before treating it as final.

## Choosing

The Grok CLI is the default because it needs no key at all, just the account
already signed in on the machine. Use the xAI API for CI, and the X API if you
have a developer token and want byte-exact captions. Either way the run
commits the post, so a bad run is a one-file revert.

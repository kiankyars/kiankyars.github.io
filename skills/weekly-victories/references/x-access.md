# How the time-lapses come off X

The script reads @neuralkian's recent posts through the Grok Build CLI.

- Command: `grok --always-approve --output-format json -p "<prompt>"`.
  `-p` is headless mode; the JSON result's `text` field holds the reply.
  `--always-approve` means no permission prompt can stall an unattended run,
  and `Bash`, `Edit` and `Write` are removed with `--disallowed-tools` so the
  agent can only search.
- Auth: `grok login` once (browser OAuth, or `grok login --device-auth` on a
  machine without a browser). The session is cached in `~/.grok/auth.json`.
- Cost: covered by the SuperGrok / X Premium+ subscription, no per-token bill.
- Limits: only works where that login exists, so the Sunday schedule runs on
  Kian's computer via launchd (`scripts/install_schedule.sh`), not in CI.
- Caveat: the model transcribes posts rather than copying them, so text can be
  truncated or lightly paraphrased and video detection is a best guess. The
  prompt asks for verbatim text and the script validates the JSON, but read
  the generated post before treating it as final. The run commits the post,
  so a bad run is a one-file revert.
- Timing: observed runs took 2 to 12 minutes; the script allows 30.

If exact, structured data is ever needed instead, the X API v2 endpoint
`GET /2/users/:id/tweets` (pay-per-use developer token) or the xAI Responses
API `x_search` tool would do it, but both need paid credentials and were
removed to keep this simple.

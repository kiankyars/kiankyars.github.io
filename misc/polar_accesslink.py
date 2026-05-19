#!/usr/bin/env python3

import argparse
import base64
import json
import secrets
import sys
import threading
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path


AUTH_URL = "https://flow.polar.com/oauth2/authorization"
TOKEN_URL = "https://polarremote.com/v2/oauth2/token"
API_BASE = "https://www.polaraccesslink.com/v3"
DEFAULT_SCOPE = "accesslink.read_all"
DEFAULT_ENV_PATH = Path("/Users/kian/.env")


def parse_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = raw_line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        values[key] = value
    return values


def update_env_file(path: Path, updates: dict[str, str]) -> None:
    lines = path.read_text().splitlines() if path.exists() else []
    remaining = dict(updates)
    out: list[str] = []
    for line in lines:
        if "=" not in line or line.lstrip().startswith("#"):
            out.append(line)
            continue
        key, _ = line.split("=", 1)
        key = key.strip()
        if key in remaining:
            out.append(f'{key}="{remaining.pop(key)}"')
        else:
            out.append(line)
    for key, value in remaining.items():
        out.append(f'{key}="{value}"')
    path.write_text("\n".join(out) + "\n")


def basic_auth_header(client_id: str, client_secret: str) -> str:
    token = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("ascii")
    return f"Basic {token}"


def get_json(url: str, headers: dict[str, str]) -> object:
    req = urllib.request.Request(url, headers=headers, method="GET")
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def post_json(url: str, headers: dict[str, str], body: object) -> object:
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        content = response.read().decode("utf-8")
        if not content:
            return {}
        return json.loads(content)


def post_form(url: str, headers: dict[str, str], body: dict[str, str]) -> object:
    req = urllib.request.Request(
        url,
        data=urllib.parse.urlencode(body).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def build_authorize_url(client_id: str, redirect_uri: str | None, state: str | None) -> str:
    params: dict[str, str] = {
        "response_type": "code",
        "client_id": client_id,
        "scope": DEFAULT_SCOPE,
    }
    if redirect_uri:
        params["redirect_uri"] = redirect_uri
    if state:
        params["state"] = state
    return f"{AUTH_URL}?{urllib.parse.urlencode(params)}"


def exchange_code(client_id: str, client_secret: str, code: str, redirect_uri: str | None) -> object:
    body = {
        "grant_type": "authorization_code",
        "code": code,
    }
    if redirect_uri:
        body["redirect_uri"] = redirect_uri
    return post_form(
        TOKEN_URL,
        {
            "Authorization": basic_auth_header(client_id, client_secret),
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json;charset=UTF-8",
        },
        body,
    )


def bearer_headers(access_token: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }


def client_headers(client_id: str, client_secret: str) -> dict[str, str]:
    return {
        "Authorization": basic_auth_header(client_id, client_secret),
        "Accept": "application/json",
    }


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--env-file", type=Path, default=DEFAULT_ENV_PATH)
    parser.add_argument("--client-id", default=None)
    parser.add_argument("--client-secret", default=None)


def resolve_client(args: argparse.Namespace) -> tuple[str, str]:
    env = parse_env(args.env_file.expanduser())
    client_id = args.client_id or env.get("POLAR_CLIENT_ID")
    client_secret = args.client_secret or env.get("POLAR_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise SystemExit("Missing Polar client credentials. Use --client-id/--client-secret or POLAR_CLIENT_ID/POLAR_CLIENT_SECRET in /Users/kian/.env")
    return client_id, client_secret


def cmd_authorize_url(args: argparse.Namespace) -> int:
    client_id, _ = resolve_client(args)
    state = args.state or secrets.token_urlsafe(24)
    print(build_authorize_url(client_id, args.redirect_uri, state))
    return 0


def cmd_exchange_code(args: argparse.Namespace) -> int:
    client_id, client_secret = resolve_client(args)
    result = exchange_code(client_id, client_secret, args.code, args.redirect_uri)
    if args.save_env:
        update_env_file(
            args.env_file.expanduser(),
            {
                "POLAR_ACCESS_TOKEN": result["access_token"],
                "POLAR_TOKEN_TYPE": result.get("token_type", "bearer"),
                "POLAR_EXPIRES_IN": str(result.get("expires_in", "")),
                "POLAR_X_USER_ID": str(result.get("x_user_id", "")),
                "POLAR_SCOPE": DEFAULT_SCOPE,
            },
        )
    json.dump(result, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


def cmd_local_auth(args: argparse.Namespace) -> int:
    client_id, client_secret = resolve_client(args)
    callback_path = "/polar_callback"
    redirect_uri = f"http://{args.host}:{args.port}{callback_path}"
    state = secrets.token_urlsafe(24)
    authorize_url = build_authorize_url(client_id, redirect_uri, state)
    result: dict[str, str] = {}

    class CallbackHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            parsed = urllib.parse.urlparse(self.path)
            if parsed.path != callback_path:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Not found")
                return
            params = urllib.parse.parse_qs(parsed.query)
            code = params.get("code", [""])[0]
            returned_state = params.get("state", [""])[0]
            error = params.get("error", [""])[0]

            # Some browsers or user retries can hit the callback twice.
            # Keep the first meaningful callback and ignore later duplicates.
            if not result and (code or error):
                result["code"] = code
                result["state"] = returned_state
                result["error"] = error
            body = b"Polar authorization received. You can close this tab.\n"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            threading.Thread(target=self.server.shutdown, daemon=True).start()

        def log_message(self, format: str, *args) -> None:
            return

    print("Authorize URL:")
    print(authorize_url)
    print(f"Waiting for callback on {redirect_uri}")

    httpd = HTTPServer((args.host, args.port), CallbackHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        return 130

    if result.get("error"):
        raise SystemExit(f"Polar authorization failed: {result['error']}")
    returned_state = result.get("state")
    if returned_state and returned_state != state:
        print(
            f"Warning: expected state {state!r} but got {returned_state!r}; continuing with local one-shot flow.",
            file=sys.stderr,
        )
    elif not returned_state:
        print("Warning: Polar callback did not include state; continuing with local one-shot flow.", file=sys.stderr)
    code = result.get("code")
    if not code:
        raise SystemExit("No authorization code received")

    token = exchange_code(client_id, client_secret, code, redirect_uri)
    update_env_file(
        args.env_file.expanduser(),
        {
            "POLAR_ACCESS_TOKEN": token["access_token"],
            "POLAR_TOKEN_TYPE": token.get("token_type", "bearer"),
            "POLAR_EXPIRES_IN": str(token.get("expires_in", "")),
            "POLAR_X_USER_ID": str(token.get("x_user_id", "")),
            "POLAR_SCOPE": DEFAULT_SCOPE,
        },
    )
    output: dict[str, object] = {"token": token}
    if args.member_id:
        access_token = token["access_token"]
        registered = post_json(
            f"{API_BASE}/users",
            {
                **bearer_headers(access_token),
                "Content-Type": "application/json",
            },
            {"member-id": args.member_id},
        )
        update_env_file(
            args.env_file.expanduser(),
            {
                "POLAR_MEMBER_ID": args.member_id,
            },
        )
        output["registered_user"] = registered
    json.dump(output, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


def cmd_register_user(args: argparse.Namespace) -> int:
    result = post_json(
        f"{API_BASE}/users",
        {
            **bearer_headers(args.access_token),
            "Content-Type": "application/json",
        },
        {"member-id": args.member_id},
    )
    json.dump(result, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


def cmd_notifications(args: argparse.Namespace) -> int:
    client_id, client_secret = resolve_client(args)
    result = get_json(f"{API_BASE}/notifications", client_headers(client_id, client_secret))
    json.dump(result, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


def cmd_exercises(args: argparse.Namespace) -> int:
    params: dict[str, str] = {}
    if args.samples:
        params["samples"] = "true"
    if args.zones:
        params["zones"] = "true"
    if args.route:
        params["route"] = "true"
    query = f"?{urllib.parse.urlencode(params)}" if params else ""
    result = get_json(f"{API_BASE}/exercises{query}", bearer_headers(args.access_token))
    json.dump(result, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


def cmd_physical_info(args: argparse.Namespace) -> int:
    env = parse_env(args.env_file.expanduser())
    user_id = env.get("POLAR_X_USER_ID")
    if not user_id:
        raise SystemExit("Missing POLAR_X_USER_ID in env file.")

    # 1. Create transaction
    url = f"{API_BASE}/users/{user_id}/physical-information-transactions"
    headers = bearer_headers(args.access_token)
    try:
        tx = post_json(url, headers, {})
    except urllib.error.HTTPError as e:
        if e.code == 204:
            print("No new physical information available.")
            return 0
        raise

    if not tx:
        print("Empty transaction response.")
        return 0
    
    # Debug print
    # print(json.dumps(tx, indent=2), file=sys.stderr)

    tx_id = tx.get("transaction-id")
    tx_url = tx.get("resource-uri")
    if not tx_url:
        print(f"Error: No resource-uri found in transaction response: {tx}", file=sys.stderr)
        return 1

    # 2. List available info IDs
    info_list = get_json(tx_url, headers)
    info_ids = info_list.get("physical-informations", [])

    results = []
    # 3. Get each entity
    for info_path in info_ids:
        entity = get_json(info_path, headers)
        results.append(entity)

    # Output results (we won't commit/PUT the transaction here to allow re-runs)
    json.dump({"transaction-id": tx_id, "data": results}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Minimal Polar AccessLink scaffold.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    authorize_url = subparsers.add_parser("authorize-url", help="Print Polar OAuth authorize URL.")
    add_common_args(authorize_url)
    authorize_url.add_argument("--redirect-uri", default=None)
    authorize_url.add_argument("--state", default=None)
    authorize_url.set_defaults(func=cmd_authorize_url)

    exchange = subparsers.add_parser("exchange-code", help="Exchange OAuth code for access token.")
    add_common_args(exchange)
    exchange.add_argument("--code", required=True)
    exchange.add_argument("--redirect-uri", default=None)
    exchange.add_argument("--save-env", action="store_true")
    exchange.set_defaults(func=cmd_exchange_code)

    local_auth = subparsers.add_parser("local-auth", help="Run local OAuth callback server and exchange code.")
    add_common_args(local_auth)
    local_auth.add_argument("--host", default="127.0.0.1")
    local_auth.add_argument("--port", type=int, default=8766)
    local_auth.add_argument("--member-id", default=None, help="Optional partner-side user identifier to auto-register after auth.")
    local_auth.set_defaults(func=cmd_local_auth)

    register_user = subparsers.add_parser("register-user", help="Register a Polar user after OAuth.")
    register_user.add_argument("--access-token", required=True)
    register_user.add_argument("--member-id", required=True)
    register_user.set_defaults(func=cmd_register_user)

    notifications = subparsers.add_parser("notifications", help="List available Polar notifications.")
    add_common_args(notifications)
    notifications.set_defaults(func=cmd_notifications)

    exercises = subparsers.add_parser("exercises", help="List recent Polar exercises.")
    exercises.add_argument("--access-token", required=True)
    exercises.add_argument("--samples", action="store_true")
    exercises.add_argument("--zones", action="store_true")
    exercises.add_argument("--route", action="store_true")
    exercises.set_defaults(func=cmd_exercises)

    physical = subparsers.add_parser("physical-info", help="Get Polar user physical information.")
    add_common_args(physical)
    physical.add_argument("--access-token", required=True)
    physical.set_defaults(func=cmd_physical_info)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

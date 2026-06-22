import sys, os, json
from dataclasses import dataclass


@dataclass(frozen=True)
class Webhook:
    body_raw: str
    body: object
    headers: dict[str,str]
    query: dict[str, str]
    meta: dict[str, str]


def _load_headers() -> dict[str, str]:
    # webhookd injects ALL params as env vars (snake_case)
    # we treat known metadata separately
    meta_keys = {
        "hook_id",
        "hook_name",
        "hook_method",
        "x_forwarded_for",
        "x_webauth_user",
    }

    headers = {}
    query = {}

    for k, v in os.environ.items():
        lk = k.lower()

        if lk in meta_keys:
            continue

        # heuristic split (webhookd flattens everything into env)
        if lk.startswith("http_") or lk in ("content_type", "user_agent"):
            headers[lk] = v
        else:
            query[lk] = v

    return headers, query


def load_webhook(strict_json: bool = True) -> Webhook:
    raw = sys.argv[1] if len(sys.argv) > 1 else None

    headers, query = _load_headers()

    parsed = None

    if raw:
        try:
            parsed = json.loads(raw)
        except Exception:
            parsed = None

    # IMPORTANT: validation happens later in sms.py
    # this layer only parses, never decides validity

    meta = {
        "hook_id": os.environ.get("hook_id"),
        "hook_name": os.environ.get("hook_name"),
        "method": os.environ.get("hook_method"),
        "ip": os.environ.get("x_forwarded_for"),
    }

    return Webhook(
        body_raw=raw,
        body=parsed,
        headers=headers,
        query=query,
        meta=meta,
    )

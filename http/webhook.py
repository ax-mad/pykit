import sys, os, json
from dataclasses import dataclass


@dataclass(frozen=True)
class Webhook:
    body_raw: str
    body: object
    headers: dict[str,str]
    query: dict[str, str]
    meta: dict[str, str]


def load_webhook(strict_json: bool = True) -> Webhook:
    raw = sys.argv[1] if len(sys.argv) > 1 else None

    headers = {
        "content_type": os.environ.get("content_type"),
        "user_agent": os.environ.get("user_agent"),
        "x_forwarded_for": os.environ.get("x_forwarded_for"),
    }

    query = {
        "source": os.environ.get("source"),
    }

    meta = {
        "hook_id": os.environ.get("hook_id"),
        "hook_name": os.environ.get("hook_name"),
        "method": os.environ.get("hook_method"),
        "ip": os.environ.get("x_forwarded_for"),
    }

    parsed = None

    if raw:
        try:
            parsed = json.loads(raw)
        except Exception:
            parsed = None

    return Webhook(
        body_raw=raw,
        body=parsed,
        headers=headers,
        query=query,
        meta=meta,
    )

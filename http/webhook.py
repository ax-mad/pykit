import sys, os, json
from dataclasses import dataclass


@dataclass
class Webhook:
    id: str
    name: str
    method: str
    originator: str
    x_forwarded_for: str
    x_webauth_user: str
    content_type: str
    payload: dict

    @classmethod
    def from_env(cls):
        return cls(
            id=os.environ.get("hook_id", ""),
            name=os.environ.get("hook_name", ""),
            method=os.environ.get("hook_method", ""),
            originator=os.environ.get("user_agent", ""),
            x_forwarded_for=os.environ.get("x_forwarded_for", ""),
            x_webauth_user=os.environ.get("x_webauth_user", "anon"),
            content_type=os.environ.get("content_type", "text/plain"),
            payload=json.loads(os.environ.get("data") or "{}"),
        )

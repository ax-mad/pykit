import os, json
from dataclasses import dataclass
from urllib.parse import parse_qsl


@dataclass
class Webhook:
    """
    Generic description of a webhook, captured thanks to webhookd
    """
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
        content_type = os.environ.get("content_type", "text/plain")
        payload = os.environ.get("payload") or ""

        return cls(
            id=os.environ.get("hook_id", ""),
            name=os.environ.get("hook_name", ""),
            method=os.environ.get("hook_method", ""),
            originator=os.environ.get("user_agent", ""),
            x_forwarded_for=os.environ.get("x_forwarded_for", ""),
            x_webauth_user=os.environ.get("x_webauth_user", "anon"),
            content_type=content_type,
            payload=json.loads(payload),
        )

#     @staticmethod
#     def parse_payload(content_type: str, data: str) -> dict:
#         if not data:
#             return {}
# 
#         if "application/x-www-form-urlencoded" in content_type:
#             return dict(parse_qsl(data))
# 
#         if "application/json" in content_type:
#             return json.loads(data)
# 
#         return {}

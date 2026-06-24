
import requests, json, dataclasses
from .models import ActionType, Notification, NotificationAction


class Notifier:
    """Delivers Notification objects to a self-hosted ntfy server."""

    def __init__(self, url:str, token:str = ""):
        self.url = url.rstrip("/")
        self.token = token

    def post(self, notification: Notification) -> dict:
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        if notification.sequence_id:
            # We use a sequence id instead of /topic/sequence_id
            # because the latter is not compatible with JSON requests
            headers["X-Sequence-ID"] = notification.sequence_id

        data = self.dump(notification)
        
        response = requests.post(
            url=self.url,
            headers=headers,
            data=json.dumps(data, default=lambda o: o.value),
            timeout=10
        )
        
        print(f"notify: {response.text}")  # extremely valuable, do not delete
        
        response.raise_for_status()
        return response.json()

    def dump(self, notification: Notification) -> dict:
        payload = dataclasses.asdict(notification)
        payload.pop("sequence_id", None)
        payload.pop("time", None)
        return payload

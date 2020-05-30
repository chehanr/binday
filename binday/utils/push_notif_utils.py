from typing import Any

from pushbullet import Pushbullet


def push_text(api_key: str, title: str, body: str) -> Any:
    pb = Pushbullet(api_key)

    return pb.push_note(title, body)

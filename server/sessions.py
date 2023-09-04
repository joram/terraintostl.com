import json
import os.path
from typing import Union

SESSIONS_FILEPATH = os.path.abspath("../data/sessions.json")


def _get_json(filepath: str) -> dict:

    # Empty file if it doesn't exist
    if not os.path.exists(filepath):
        with open(filepath, "w") as f:
            f.write("{}")
            return {}

    # Read file
    with open(filepath, "r") as f:
        return json.loads(f.read())


def _save_json(filepath: str, data: dict):
    with open(filepath, "w") as f:
        f.write(json.dumps(data, indent=4, sort_keys=True))


def get_session(session_key: str) -> Union[dict, None]:
    sessions = _get_json(SESSIONS_FILEPATH)
    if session_key in sessions:
        return sessions[session_key]
    return None


def save_session(session_key: str, session: dict):
    sessions = _get_json(SESSIONS_FILEPATH)
    sessions[session_key] = session
    _save_json(SESSIONS_FILEPATH, sessions)

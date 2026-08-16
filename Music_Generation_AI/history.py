import json
from pathlib import Path


HISTORY_FILE = Path("generated_music/history.json")


def load_history():
    """Load previously generated music history."""

    if not HISTORY_FILE.exists():
        return []

    try:
        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return []


def save_history(entry):
    """Save a new music generation entry."""

    HISTORY_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    history = load_history()

    history.append(entry)

    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            history,
            file,
            indent=4
        )


def clear_history():
    """Delete all saved music history."""

    if HISTORY_FILE.exists():
        HISTORY_FILE.unlink()
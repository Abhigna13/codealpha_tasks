import json
from pathlib import Path
from datetime import datetime


ACTIVITY_FILE = Path(
    "generated_music/activity.json"
)


def ensure_activity_file():

    ACTIVITY_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if not ACTIVITY_FILE.exists():

        with open(
            ACTIVITY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                [],
                file,
                indent=4
            )


def load_activity():

    ensure_activity_file()

    try:

        with open(
            ACTIVITY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except (
        json.JSONDecodeError,
        FileNotFoundError
    ):

        return []


def save_activity(activity):

    ensure_activity_file()

    with open(
        ACTIVITY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            activity,
            file,
            indent=4
        )


def record_play(track_index, track):

    activity = load_activity()

    now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    activity.append({

        "track_index": track_index,

        "title": track.get(
            "title",
            "Untitled Music"
        ),

        "genre": track.get(
            "genre",
            "Unknown"
        ),

        "mood": track.get(
            "mood",
            "Unknown"
        ),

        "audio_file": track.get(
            "audio_file",
            ""
        ),

        "played_at": now
    })

    save_activity(activity)


def get_play_count(track_index):

    activity = load_activity()

    return sum(

        1

        for item in activity

        if item.get(
            "track_index"
        ) == track_index
    )


def get_last_played(track_index):

    activity = load_activity()

    matching = [

        item

        for item in activity

        if item.get(
            "track_index"
        ) == track_index
    ]

    if not matching:

        return "Never"

    return matching[-1].get(
        "played_at",
        "Unknown"
    )


def clear_activity():

    save_activity([])
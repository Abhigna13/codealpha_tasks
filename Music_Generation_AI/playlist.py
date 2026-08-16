import json
from pathlib import Path


PLAYLIST_FILE = Path(
    "generated_music/playlists.json"
)


def ensure_playlist_file():

    PLAYLIST_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if not PLAYLIST_FILE.exists():

        with open(
            PLAYLIST_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                [],
                file,
                indent=4
            )


def load_playlists():

    ensure_playlist_file()

    try:

        with open(
            PLAYLIST_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except (
        json.JSONDecodeError,
        FileNotFoundError
    ):

        return []


def save_playlists(playlists):

    ensure_playlist_file()

    with open(
        PLAYLIST_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            playlists,
            file,
            indent=4
        )


def create_playlist(name):

    name = name.strip()

    if not name:

        return False

    playlists = load_playlists()

    for playlist in playlists:

        if playlist["name"].lower() == name.lower():

            return False

    playlists.append({

        "name": name,

        "tracks": []

    })

    save_playlists(playlists)

    return True


def delete_playlist(name):

    playlists = load_playlists()

    updated_playlists = [

        playlist

        for playlist in playlists

        if playlist["name"] != name
    ]

    save_playlists(
        updated_playlists
    )


def add_track_to_playlist(
    playlist_name,
    track_index
):

    playlists = load_playlists()

    for playlist in playlists:

        if playlist["name"] == playlist_name:

            if track_index not in playlist["tracks"]:

                playlist["tracks"].append(
                    track_index
                )

    save_playlists(playlists)


def remove_track_from_playlist(
    playlist_name,
    track_index
):

    playlists = load_playlists()

    for playlist in playlists:

        if playlist["name"] == playlist_name:

            if track_index in playlist["tracks"]:

                playlist["tracks"].remove(
                    track_index
                )

    save_playlists(playlists)
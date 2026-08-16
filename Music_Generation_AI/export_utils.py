import json


def create_track_metadata(track):

    metadata = {

        "title": track.get(
            "title",
            "Untitled Music"
        ),

        "prompt": track.get(
            "prompt",
            ""
        ),

        "genre": track.get(
            "genre",
            "Unknown"
        ),

        "mood": track.get(
            "mood",
            "Unknown"
        ),

        "duration": track.get(
            "duration",
            "Unknown"
        ),

        "generation_mode": track.get(
            "generation_mode",
            "Balanced"
        ),

        "creativity": track.get(
            "creativity",
            0.7
        ),

        "audio_type": track.get(
            "audio_type",
            "Instrumental"
        ),

        "created_at": track.get(
            "created_at",
            "Unknown"
        ),

        "favorite": track.get(
            "favorite",
            False
        )
    }

    return metadata


def metadata_to_json(track):

    metadata = create_track_metadata(
        track
    )

    return json.dumps(
        metadata,
        indent=4
    )


def metadata_to_text(track):

    metadata = create_track_metadata(
        track
    )

    favorite_status = (

        "Yes ⭐"

        if metadata["favorite"]

        else "No"
    )


    text = f"""
MUSIC GENERATION AI
===================

Title:
{metadata["title"]}

Prompt:
{metadata["prompt"]}

Genre:
{metadata["genre"]}

Mood:
{metadata["mood"]}

Duration:
{metadata["duration"]}

Generation Mode:
{metadata["generation_mode"]}

Creativity:
{metadata["creativity"]}

Audio Type:
{metadata["audio_type"]}

Created:
{metadata["created_at"]}

Favorite:
{favorite_status}

Generated using Music Generation AI.
"""

    return text.strip()
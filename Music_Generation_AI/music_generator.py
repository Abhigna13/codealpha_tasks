import numpy as np
import wave
from pathlib import Path


# --------------------------------------------------
# MUSICAL SCALES
# --------------------------------------------------

SCALES = {

    "Cinematic": [
        261.63,
        293.66,
        329.63,
        392.00,
        440.00,
        523.25
    ],

    "Pop": [
        261.63,
        293.66,
        329.63,
        349.23,
        392.00,
        440.00,
        493.88
    ],

    "Rock": [
        220.00,
        246.94,
        293.66,
        329.63,
        369.99,
        440.00
    ],

    "Classical": [
        261.63,
        293.66,
        329.63,
        349.23,
        392.00,
        493.88
    ],

    "Lo-fi": [
        220.00,
        261.63,
        293.66,
        329.63,
        392.00
    ],

    "Jazz": [
        261.63,
        293.66,
        329.63,
        369.99,
        440.00,
        493.88
    ],

    "Electronic": [
        261.63,
        329.63,
        392.00,
        523.25,
        659.25
    ]
}


# --------------------------------------------------
# MOOD SETTINGS
# --------------------------------------------------

MOOD_SETTINGS = {

    "Happy": {
        "speed": 1.3,
        "volume": 0.25
    },

    "Peaceful": {
        "speed": 0.7,
        "volume": 0.18
    },

    "Energetic": {
        "speed": 1.6,
        "volume": 0.30
    },

    "Sad": {
        "speed": 0.6,
        "volume": 0.18
    },

    "Relaxing": {
        "speed": 0.65,
        "volume": 0.17
    },

    "Epic": {
        "speed": 1.1,
        "volume": 0.30
    },

    "Mysterious": {
        "speed": 0.8,
        "volume": 0.20
    }
}


# --------------------------------------------------
# INSTRUMENT SETTINGS
# --------------------------------------------------

INSTRUMENT_SETTINGS = {

    "Piano": {
        "harmonic": 2.0,
        "brightness": 0.25
    },

    "Guitar": {
        "harmonic": 2.5,
        "brightness": 0.18
    },

    "Strings": {
        "harmonic": 1.5,
        "brightness": 0.30
    },

    "Synth": {
        "harmonic": 3.0,
        "brightness": 0.12
    },

    "Bass": {
        "harmonic": 1.0,
        "brightness": 0.10
    }
}


# --------------------------------------------------
# CREATE INSTRUMENT NOTE
# --------------------------------------------------

def create_instrument_note(
    frequency,
    duration,
    sample_rate,
    volume,
    harmonic,
    brightness
):

    t = np.linspace(
        0,
        duration,
        int(sample_rate * duration),
        endpoint=False
    )

    # Main frequency
    note = np.sin(
        2 * np.pi * frequency * t
    )

    # Instrument harmonic
    note += brightness * np.sin(
        2 * np.pi * frequency * harmonic * t
    )

    # Soft envelope
    envelope = np.exp(
        -2.5 * t / duration
    )

    note *= envelope

    note *= volume

    return note


# --------------------------------------------------
# GENERATE DEMO MUSIC
# --------------------------------------------------

def generate_demo_music(
    genre="Classical",
    mood="Peaceful",
    instrument="Piano",
    duration_seconds=8,
    output_path="generated_music/demo_music.wav",
    sample_rate=44100
):

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Get genre scale
    scale = SCALES.get(
        genre,
        SCALES["Classical"]
    )

    # Get mood settings
    mood_settings = MOOD_SETTINGS.get(
        mood,
        MOOD_SETTINGS["Peaceful"]
    )

    speed = mood_settings["speed"]
    volume = mood_settings["volume"]

    # Get instrument settings
    instrument_settings = INSTRUMENT_SETTINGS.get(
        instrument,
        INSTRUMENT_SETTINGS["Piano"]
    )

    harmonic = instrument_settings["harmonic"]
    brightness = instrument_settings["brightness"]

    # --------------------------------------------------
    # CREATE MELODY
    # --------------------------------------------------

    melody = []

    note_duration = 0.45 / speed

    number_of_notes = int(
        duration_seconds / note_duration
    )

    for index in range(number_of_notes):

        frequency = scale[
            index % len(scale)
        ]

        note = create_instrument_note(
            frequency,
            note_duration,
            sample_rate,
            volume,
            harmonic,
            brightness
        )

        melody.append(note)

    melody = np.concatenate(melody)

    # Make exact requested length
    target_length = int(
        sample_rate * duration_seconds
    )

    if len(melody) < target_length:

        melody = np.pad(
            melody,
            (
                0,
                target_length - len(melody)
            )
        )

    else:

        melody = melody[:target_length]

    # --------------------------------------------------
    # BACKGROUND CHORD
    # --------------------------------------------------

    t = np.linspace(
        0,
        len(melody) / sample_rate,
        len(melody),
        endpoint=False
    )

    root = scale[0]

    background = (
        0.08 * np.sin(
            2 * np.pi * root * t
        )
        +
        0.05 * np.sin(
            2 * np.pi * root * 1.5 * t
        )
    )

    # --------------------------------------------------
    # COMBINE AUDIO
    # --------------------------------------------------

    audio = melody + background

    # --------------------------------------------------
    # FADE IN / FADE OUT
    # --------------------------------------------------

    fade_length = min(
        int(sample_rate * 0.5),
        len(audio) // 2
    )

    fade_in = np.linspace(
        0,
        1,
        fade_length
    )

    fade_out = np.linspace(
        1,
        0,
        fade_length
    )

    audio[:fade_length] *= fade_in
    audio[-fade_length:] *= fade_out

    # --------------------------------------------------
    # NORMALIZE
    # --------------------------------------------------

    max_value = np.max(
        np.abs(audio)
    )

    if max_value > 0:

        audio = (
            audio / max_value
        )

    # --------------------------------------------------
    # CONVERT TO 16-BIT AUDIO
    # --------------------------------------------------

    audio_data = np.int16(
        audio * 32767
    )

    # --------------------------------------------------
    # SAVE WAV
    # --------------------------------------------------

    with wave.open(
        str(output_path),
        "wb"
    ) as wav_file:

        wav_file.setnchannels(1)

        wav_file.setsampwidth(2)

        wav_file.setframerate(
            sample_rate
        )

        wav_file.writeframes(
            audio_data.tobytes()
        )

    return str(output_path)
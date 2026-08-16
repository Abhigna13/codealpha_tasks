import streamlit as st
from datetime import datetime
from pathlib import Path

from music_generator import generate_demo_music

from history import (
    load_history,
    save_history,
    clear_history
)

from playlist import (
    load_playlists,
    create_playlist,
    delete_playlist,
    add_track_to_playlist,
    remove_track_from_playlist
)

from export_utils import (
    metadata_to_json,
    metadata_to_text
)

from activity import (
    load_activity,
    record_play,
    get_play_count,
    get_last_played,
    clear_activity
)

from ai.ai_generator import (
    get_model_status,
    get_model_name,
    is_model_available,
    generate_ai_music,
    get_device,
    get_model_info
)

from ai.config import (
    AI_MODEL_ENABLED,
    AI_MODEL_NAME,
    DEFAULT_DURATION,
    SUPPORTED_MODES
)


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Music Generation AI",
    page_icon="🎵",
    layout="wide"
)

st.markdown(
    """
    <style>
    :root {
        --bg: #5a2130;
        --bg-deep: #3c1424;
        --panel: #fff7ec;
        --panel-soft: #f8e9d6;
        --accent: #c96c3e;
        --accent-2: #d7a24b;
        --accent-3: #a53b3b;
        --text: #4a2330;
        --muted: #7a5763;
        --border: #e7c29e;
        --shadow: 0 16px 34px rgba(55, 20, 29, 0.15);
    }

    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        background:
            radial-gradient(circle at 15% 0%, rgba(215, 162, 75, 0.15), transparent 22%),
            radial-gradient(circle at 85% 12%, rgba(197, 108, 62, 0.16), transparent 24%),
            linear-gradient(135deg, #6a2838 0%, #4f1d2c 50%, #39151f 100%);
        color: #fff7ec;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #6d2a39 0%, #4d1c2b 100%);
        border-right: 1px solid rgba(255, 240, 222, 0.16);
        box-shadow: 10px 0 26px rgba(24, 8, 14, 0.2);
    }

    [data-testid="stSidebar"] * {
        color: #fff4e6 !important;
    }

    .stApp [data-testid="stHeader"] {
        background: transparent;
        box-shadow: none;
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 2.8rem;
        max-width: 1500px;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #fff6e9 !important;
        letter-spacing: 0.02em;
    }

    .stTitle {
        font-size: 2.85rem !important;
        font-weight: 800 !important;
        color: #fff4e6 !important;
        margin-bottom: 0.25rem !important;
        text-shadow: 0 1px 0 rgba(255,255,255,0.1);
    }

    .stSubheader {
        color: #ffeacc !important;
        font-size: 1.17rem !important;
        font-weight: 700 !important;
    }

    /* Main page text */
.stApp > div {
    color: #fff8ef;
}

/* Text inside light cards */
div[data-testid="stVerticalBlockBorderWrapper"] p,
div[data-testid="stVerticalBlockBorderWrapper"] span,
div[data-testid="stVerticalBlockBorderWrapper"] div {
    color: #4a2330 !important;
}

/* Text inside expanders */
div[data-testid="stExpander"] p,
div[data-testid="stExpander"] span,
div[data-testid="stExpander"] div {
    color: #4a2330 !important;
}

/* Expander header */
div[data-testid="stExpander"] summary {
    color: #4a2330 !important;
}

/* Text areas */
.stTextArea textarea {
    color: #4a2330 !important;
    background-color: #fffdf8 !important;
}

/* Labels inside light sections */
div[data-testid="stExpander"] label,
div[data-testid="stVerticalBlockBorderWrapper"] label {
    color: #4a2330 !important;
}

    .stCaption, .stMarkdown small {
        color: #f0d1bb !important;
    }

    .hero-shell {
        display: inline-flex;
        align-items: center;
        gap: 0.7rem;
        margin: 0.2rem 0 0.8rem 0;
        padding: 0.45rem 0.8rem;
        border: 1px solid rgba(255, 240, 222, 0.2);
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.08);
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.16);
    }

    .hero-kicker {
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.28em;
        text-transform: uppercase;
        color: var(--accent-2);
    }

    .hero-glow {
        width: 0.5rem;
        height: 0.5rem;
        border-radius: 50%;
        background: linear-gradient(135deg, var(--accent-2), var(--accent));
        box-shadow: 0 0 8px rgba(215, 162, 75, 0.3);
    }

    [data-testid="stMetric"] {
        background: linear-gradient(145deg, #fff9ef, #f7e3ce);
        border: 1px solid rgba(201, 108, 62, 0.24);
        border-radius: 18px;
        padding: 0.95rem 1rem 0.85rem;
        box-shadow: var(--shadow);
    }

    [data-testid="stMetric"] label {
        color: var(--accent) !important;
        font-weight: 600;
    }

    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: var(--bg-deep) !important;
        font-size: 1.16rem !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255, 247, 236, 0.94);
        border: 1px solid rgba(201, 108, 62, 0.2);
        border-radius: 24px;
        padding: 1rem 1rem 1.1rem;
        box-shadow: var(--shadow);
        margin-bottom: 1rem;
    }

    div[data-testid="stExpander"] {
        border: 1px solid rgba(201, 108, 62, 0.18) !important;
        border-radius: 18px !important;
        background: rgba(255, 247, 236, 0.95) !important;
        box-shadow: var(--shadow);
    }

    div[data-testid="stExpander"] summary {
        color: var(--bg-deep) !important;
        font-weight: 700 !important;
        padding: 0.8rem 0.9rem !important;
    }

    div[data-testid="stExpander"] .streamlit-expanderContent {
        padding: 0.35rem 0.9rem 0.9rem;
    }

    .stTextInput > div > div > input,
    .stTextArea textarea,
    .stSelectbox > div > div > div,
    .stNumberInput input,
    .stDateInput input {
        background-color: #fffdf8 !important;
        color: var(--text) !important;
        border: 1px solid rgba(201, 108, 62, 0.28) !important;
        border-radius: 14px !important;
        box-shadow: inset 0 1px 2px rgba(55, 20, 29, 0.05);
    }

    .stTextInput > div > div > input::placeholder,
    .stTextArea textarea::placeholder {
        color: var(--muted) !important;
    }

    .stTextArea textarea {
        min-height: 140px;
        padding: 0.9rem 1rem;
    }

    .stSelectbox [data-baseweb="select"] > div,
    .stSelectbox [data-baseweb="select"] [role="button"] {
        background-color: #fffdf8 !important;
        color: var(--text) !important;
        border: 1px solid rgba(201, 108, 62, 0.28) !important;
        border-radius: 14px !important;
    }

    .stSelectbox [role="listbox"] {
        background: #fffdf8 !important;
        border: 1px solid rgba(201, 108, 62, 0.18) !important;
    }

    .stSelectbox [role="option"] {
        color: var(--text) !important;
    }

    div.stButton > button,
    .stDownloadButton > button {
        background: linear-gradient(135deg, var(--accent), var(--accent-2));
        color: #fffdf8 !important;
        border: 1px solid rgba(255,255,255,0.32) !important;
        border-radius: 999px !important;
        font-weight: 700 !important;
        padding: 0.6rem 1rem !important;
        box-shadow: 0 10px 24px rgba(189, 98, 49, 0.22);
        transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
    }

    div.stButton > button:hover,
    .stDownloadButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 14px 30px rgba(189, 98, 49, 0.26);
        border-color: rgba(255,255,255,0.36) !important;
    }

    div.stButton > button:focus,
    .stDownloadButton > button:focus {
        box-shadow: 0 0 0 3px rgba(215, 162, 75, 0.22), 0 10px 24px rgba(189, 98, 49, 0.22) !important;
    }

    .stRadio > label {
        color: #fff8ef !important;
    }

    .stAlert, .stSuccess, .stWarning, .stInfo, .stError {
        border-radius: 16px !important;
        border: 1px solid rgba(201, 108, 62, 0.18) !important;
        background: rgba(255, 247, 236, 0.95) !important;
        color: var(--text) !important;
    }

    .stSuccess {
        border-color: rgba(201, 108, 62, 0.23) !important;
    }

    .stWarning {
        border-color: rgba(215, 162, 75, 0.22) !important;
    }

    .stInfo {
        border-color: rgba(215, 162, 75, 0.22) !important;
    }

    .stError {
        border-color: rgba(193, 93, 93, 0.22) !important;
    }

    audio {
        width: 100%;
        border-radius: 12px;
    }

    [data-testid="stAudioPlayer"] {
        border-radius: 16px;
        overflow: hidden;
    }

    [data-testid="stAudioPlayer"] > div {
        background: #fff9f2 !important;
        border: 1px solid rgba(201, 108, 62, 0.16) !important;
    }

    @media (max-width: 768px) {
        .stTitle {
            font-size: 2.1rem !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"] {
            padding: 0.85rem;
        }
    }

    /* Fix Streamlit alert text visibility */
[data-testid="stAlert"] {
    color: #4a2330 !important;
}

[data-testid="stAlert"] p,
[data-testid="stAlert"] div,
[data-testid="stAlert"] span {
    color: #4a2330 !important;
}

/* Warning message */
[data-testid="stAlert"][data-baseweb="notification"] {
    color: #4a2330 !important;
}

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# LOAD DATA
# ==================================================

playlists = load_playlists()
history = load_history()


# ==================================================
# FAVORITE HELPERS
# ==================================================

def is_favorite(item):

    return item.get(
        "favorite",
        False
    )


def update_favorite(index, value):

    current_history = load_history()

    if 0 <= index < len(current_history):

        current_history[index]["favorite"] = value

        import json

        history_file = Path(
            "generated_music/history.json"
        )

        history_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            history_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                current_history,
                file,
                indent=4
            )


# ==================================================
# PROMPT SUGGESTIONS
# ==================================================

PROMPT_SUGGESTIONS = {

    "🎬 Cinematic": [
        "Create an epic cinematic soundtrack for a fantasy adventure.",
        "Create a peaceful cinematic piano melody for relaxation.",
        "Create an emotional orchestral soundtrack for a movie scene."
    ],

    "🎮 Gaming": [
        "Create an energetic electronic soundtrack for a futuristic game.",
        "Create an intense battle theme for an action game.",
        "Create a mysterious atmospheric soundtrack for an adventure game."
    ],

    "📚 Study": [
        "Create a relaxing lo-fi melody for studying.",
        "Create peaceful background music for reading.",
        "Create soft instrumental music for concentration."
    ],

    "💪 Workout": [
        "Create a high-energy electronic workout track.",
        "Create an energetic rock track for exercise.",
        "Create a powerful motivational music track."
    ],

    "😌 Relaxation": [
        "Create peaceful ambient music for meditation.",
        "Create a calm piano melody for relaxation.",
        "Create soft relaxing music for sleep."
    ],

    "🎉 Party": [
        "Create an upbeat pop song for a party.",
        "Create an energetic electronic dance track.",
        "Create a fun and happy music track for celebration."
    ]
}


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.title("🎵 Music AI")

    st.write(
        "AI-powered music creation platform"
    )

    st.divider()

    st.subheader(
        "⚙️ Generation Settings"
    )

    generation_mode = st.selectbox(
        "Generation Mode",
        [
            "Creative",
            "Balanced",
            "Precise"
        ]
    )

    creativity = st.slider(
        "🎨 Creativity",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1
    )

    vocals = st.selectbox(
        "🎤 Audio Type",
        [
            "Instrumental",
            "Vocals"
        ]
    )

    st.divider()

    st.write(
        "**Project:** Music Generation AI"
    )

    st.write(
        "**Version:** Day 16"
    )


# ==================================================
# MAIN TITLE
# ==================================================

st.markdown(
    """
    <div class="hero-shell">
        <div class="hero-kicker">NEON SONIC LAB</div>
        <div class="hero-glow"></div>
    </div>
    """,
    unsafe_allow_html=True
)

st.title(
    "🎵 Music Generation with AI"
)

st.write(
    "Create unique music from a simple text description."
)

st.divider()


# ==================================================
# DASHBOARD
# ==================================================

st.subheader(
    "📊 Music Dashboard"
)

history = load_history()
playlists = load_playlists()
activity = load_activity()


total_generations = len(
    history
)


favorite_count = sum(
    1
    for item in history
    if is_favorite(item)
)


genres = [
    item.get(
        "genre",
        "Unknown"
    )
    for item in history
]


moods = [
    item.get(
        "mood",
        "Unknown"
    )
    for item in history
]


if genres:

    most_used_genre = max(
        set(genres),
        key=genres.count
    )

else:

    most_used_genre = "None"


if moods:

    most_used_mood = max(
        set(moods),
        key=moods.count
    )

else:

    most_used_mood = "None"


dash_col1, dash_col2, dash_col3, dash_col4, dash_col5, dash_col6, dash_col7 = st.columns(7)


with dash_col1:

    st.metric(
        "🎵 Total Generations",
        total_generations
    )


with dash_col2:

    st.metric(
        "⭐ Favorites",
        favorite_count
    )


with dash_col3:

    st.metric(
        "🎸 Favorite Genre",
        most_used_genre
    )


with dash_col4:

    st.metric(
        "😊 Favorite Mood",
        most_used_mood
    )


with dash_col5:

    st.metric(
        "📚 Playlists",
        len(playlists)
    )


with dash_col6:

    st.metric(
        "▶️ Plays",
        len(activity)
    )


st.divider()

with dash_col7:

    if is_model_available():

        st.metric(
            "🤖 AI Model",
            "Ready"
        )

    else:

        st.metric(
            "🤖 AI Model",
            "Preparing"
        )

model_info = get_model_info()


st.caption(
    f"🤖 AI Engine: "
    f"{model_info['model_name']} | "
    f"Device: "
    f"{model_info['device'].upper()}"
)

if model_info["cuda_available"]:

    st.success(
        "🚀 NVIDIA CUDA GPU detected."
    )

else:

    st.info(
        "💻 CUDA GPU not detected. "
        "AI generation will use CPU."
    )


# ==================================================
# PROMPT SUGGESTIONS
# ==================================================

st.subheader(
    "💡 Prompt Suggestions"
)

st.write(
    "Choose a category and select a ready-made prompt."
)


prompt_category = st.selectbox(
    "Choose a category",
    list(
        PROMPT_SUGGESTIONS.keys()
    )
)


selected_prompt = st.selectbox(
    "Choose a music prompt",
    PROMPT_SUGGESTIONS[
        prompt_category
    ]
)


if st.button(
    "✨ Use Selected Prompt"
):

    st.session_state[
        "selected_prompt"
    ] = selected_prompt

    st.success(
        "✅ Prompt selected! "
        "You can now generate your music."
    )


# ==================================================
# MUSIC GENERATION INPUT
# ==================================================

st.subheader(
    "🎼 Create Your Music"
)


default_prompt = st.session_state.get(
    "selected_prompt",
    ""
)


prompt = st.text_area(
    "Describe the music you want",
    value=default_prompt,
    placeholder=(
        "Example: Create a peaceful piano melody "
        "with soft cinematic background music."
    ),
    height=120
)


# ==================================================
# MUSIC SETTINGS
# ==================================================

st.subheader(
    "🎚️ Music Settings"
)


col1, col2, col3 = st.columns(3)


with col1:

    genre = st.selectbox(
        "🎸 Genre",
        [
            "Cinematic",
            "Pop",
            "Rock",
            "Classical",
            "Lo-fi",
            "Jazz",
            "Electronic"
        ]
    )


with col2:

    mood = st.selectbox(
        "😊 Mood",
        [
            "Happy",
            "Peaceful",
            "Energetic",
            "Sad",
            "Relaxing",
            "Epic",
            "Mysterious"
        ]
    )


with col3:

    duration = st.selectbox(
        "⏱️ Duration",
        [
            "30 seconds",
            "1 minute",
            "2 minutes",
            "3 minutes"
        ]
    )


# ==================================================
# GENERATE MUSIC
# ==================================================

st.divider()

st.subheader(
    "🤖 Generation Engine"
)


generation_engine = st.radio(

    "Choose music generation engine",

    SUPPORTED_MODES,

    horizontal=True
)

if generation_engine == "AI Generator":

    if is_model_available():

        st.success(
            "🤖 AI music model is ready."
        )

    else:

        st.warning(
            "⚠️ AI model is not connected yet. "
            "Please use Demo Generator until "
            "the model is configured."
        )

    if not is_model_available():

        st.error(
            "❌ AI model is not available yet."
        )

        st.info(
            "Use Demo Generator for now. "
            "Real AI model integration will "
            "be activated after model setup."
        )

        st.stop()

if st.button(
    "🎵 Generate Music",
    use_container_width=True
):

    if prompt.strip() == "":

        st.warning(
            "⚠️ Please enter a music description first."
        )

    else:

        st.info(
            "🎼 Creating your music preview..."
        )


        duration_map = {

            "30 seconds": 5,

            "1 minute": 8,

            "2 minutes": 10,

            "3 minutes": 12
        }


        generation_time = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        audio_filename = (
            f"generated_music/music_"
            f"{generation_time}.wav"
        )

        audio_file = generate_demo_music(

            genre=genre,

            mood=mood,

            duration_seconds=duration_map[
                duration
            ],

            output_path=audio_filename
        )


        generation_timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )


        music_title = (
            f"{mood} {genre} Music"
        )


        entry = {

            "title": music_title,

            "prompt": prompt,

            "genre": genre,

            "mood": mood,

            "duration": duration,

            "generation_mode": generation_mode,

            "creativity": creativity,

            "audio_type": vocals,

            "audio_file": audio_file,

            "created_at": generation_timestamp,

            "favorite": False
        }


        save_history(
            entry
        )


        st.success(
            "✅ Music generated successfully!"
        )


        st.divider()


        st.subheader(
            "🎧 Your Generated Music"
        )


        st.markdown(
            f"## 🎵 {music_title}"
        )


        st.write(
            f"**Created:** {generation_time}"
        )


        audio_path = Path(
            audio_file
        )


        if audio_path.exists():

            with open(
                audio_path,
                "rb"
            ) as audio:

                audio_bytes = audio.read()


            # --------------------------------------------------
            # AUDIO PLAYER
            # --------------------------------------------------

            st.audio(
                audio_bytes,
                format="audio/wav"
            )


            # --------------------------------------------------
            # GET NEW TRACK INDEX
            # --------------------------------------------------

            current_history = load_history()

            new_track_index = (
                len(current_history) - 1
            )


            # --------------------------------------------------
            # MARK AS PLAYED
            # --------------------------------------------------

            if st.button(

                "▶️ Mark as Played",

                key=(
                    f"generated_play_"
                    f"{new_track_index}"
                )
            ):

                record_play(

                    new_track_index,

                    entry
                )

                st.success(
                    "▶️ Track added to listening activity."
                )

                st.rerun()


            # --------------------------------------------------
            # PLAY STATISTICS
            # --------------------------------------------------

            play_count = get_play_count(
                new_track_index
            )


            last_played = get_last_played(
                new_track_index
            )


            st.write(
                f"▶️ **Played:** "
                f"{play_count} time(s)"
            )


            st.write(
                f"🕒 **Last Played:** "
                f"{last_played}"
            )


            # --------------------------------------------------
            # DOWNLOAD
            # --------------------------------------------------

            st.download_button(

                label="⬇️ Download Music",

                data=audio_bytes,

                file_name="generated_music.wav",

                mime="audio/wav",

                use_container_width=True
            )


        # ==================================================
        # MUSIC INFORMATION
        # ==================================================

        st.subheader(
            "🎼 Music Information"
        )


        info_col1, info_col2 = st.columns(2)


        with info_col1:

            st.write(
                f"**Genre:** {genre}"
            )

            st.write(
                f"**Mood:** {mood}"
            )

            st.write(
                f"**Duration:** {duration}"
            )


        with info_col2:

            st.write(
                f"**Mode:** {generation_mode}"
            )

            st.write(
                f"**Creativity:** {creativity}"
            )

            st.write(
                f"**Audio Type:** {vocals}"
            )


        st.write(
            f"**Prompt:** {prompt}"
        )


# ==================================================
# RECENT GENERATIONS
# ==================================================

st.divider()


st.subheader(
    "🕘 Recent Generations"
)


current_history = load_history()


if current_history:

    recent_items = current_history[-5:]


    for index, item in enumerate(

        reversed(recent_items),

        start=1
    ):

        title = item.get(
            "title",
            f"Generation {index}"
        )


        created_at = item.get(
            "created_at",
            "Unknown time"
        )


        favorite_symbol = (

            "⭐"

            if is_favorite(item)

            else "☆"
        )


        st.write(
            f"**{favorite_symbol} {title}** "
            f"— {created_at}"
        )


else:

    st.info(
        "No recent generations available."
    )


# ==================================================
# MUSIC LIBRARY
# ==================================================

st.divider()


st.subheader(
    "📚 Music Library"
)


library_history = load_history()


if library_history:

    search_text = st.text_input(
        "🔎 Search music",
        placeholder=(
            "Search by title or prompt..."
        )
    )


    filter_col1, filter_col2, filter_col3 = st.columns(3)


    with filter_col1:

        genre_options = sorted(
            list(
                set(
                    item.get(
                        "genre",
                        "Unknown"
                    )
                    for item in library_history
                )
            )
        )


        selected_genre = st.selectbox(
            "🎸 Filter by Genre",
            ["All"] + genre_options
        )


    with filter_col2:

        mood_options = sorted(
            list(
                set(
                    item.get(
                        "mood",
                        "Unknown"
                    )
                    for item in library_history
                )
            )
        )


        selected_mood = st.selectbox(
            "😊 Filter by Mood",
            ["All"] + mood_options
        )


    with filter_col3:

        favorite_filter = st.selectbox(
            "⭐ Favorites",
            [
                "All Music",
                "Favorites Only",
                "Non-Favorites"
            ]
        )


    filtered_music = []


    for original_index, item in enumerate(
        library_history
    ):

        title = item.get(
            "title",
            ""
        ).lower()


        item_prompt = item.get(
            "prompt",
            ""
        ).lower()


        item_genre = item.get(
            "genre",
            "Unknown"
        )


        item_mood = item.get(
            "mood",
            "Unknown"
        )


        item_favorite = is_favorite(
            item
        )


        matches_search = (

            search_text.lower() in title

            or

            search_text.lower() in item_prompt
        )


        matches_genre = (

            selected_genre == "All"

            or

            item_genre == selected_genre
        )


        matches_mood = (

            selected_mood == "All"

            or

            item_mood == selected_mood
        )


        if favorite_filter == "All Music":

            matches_favorite = True

        elif favorite_filter == "Favorites Only":

            matches_favorite = item_favorite

        else:

            matches_favorite = not item_favorite


        if (

            matches_search

            and matches_genre

            and matches_mood

            and matches_favorite

        ):

            filtered_music.append(
                (
                    original_index,
                    item
                )
            )


    st.write(
        f"**{len(filtered_music)} "
        f"music track(s) found.**"
    )


    if filtered_music:

        for display_index, (
            original_index,
            item
        ) in enumerate(

            reversed(filtered_music),

            start=1
        ):

            title = item.get(
                "title",
                f"Music {display_index}"
            )


            favorite_symbol = (

                "⭐"

                if is_favorite(item)

                else "☆"
            )


            # ==================================================
            # MUSIC LIBRARY CARD
            # ==================================================

            with st.expander(
                f"{favorite_symbol} {title}"
            ):


                # --------------------------------------------------
                # MUSIC INFORMATION
                # --------------------------------------------------

                library_col1, library_col2 = st.columns(2)


                with library_col1:

                    st.write(
                        f"**Genre:** "
                        f"{item.get('genre', 'Unknown')}"
                    )


                    st.write(
                        f"**Mood:** "
                        f"{item.get('mood', 'Unknown')}"
                    )


                    st.write(
                        f"**Duration:** "
                        f"{item.get('duration', 'Unknown')}"
                    )


                with library_col2:

                    st.write(
                        f"**Created:** "
                        f"{item.get('created_at', 'Unknown')}"
                    )


                    st.write(
                        f"**Mode:** "
                        f"{item.get('generation_mode', 'Balanced')}"
                    )


                    st.write(
                        f"**Creativity:** "
                        f"{item.get('creativity', 0.7)}"
                    )


                st.write(
                    f"**Prompt:** "
                    f"{item.get('prompt', '')}"
                )


                # --------------------------------------------------
                # FAVORITE BUTTON
                # --------------------------------------------------

                if is_favorite(item):

                    if st.button(

                        "💔 Remove from Favorites",

                        key=(
                            f"remove_favorite_"
                            f"{original_index}"
                        )
                    ):

                        update_favorite(
                            original_index,
                            False
                        )


                        st.success(
                            "Removed from Favorites."
                        )


                        st.rerun()


                else:

                    if st.button(

                        "⭐ Add to Favorites",

                        key=(
                            f"add_favorite_"
                            f"{original_index}"
                        )
                    ):

                        update_favorite(
                            original_index,
                            True
                        )


                        st.success(
                            "Added to Favorites."
                        )


                        st.rerun()


                # --------------------------------------------------
                # AUDIO PLAYER
                # --------------------------------------------------

                audio_path = Path(
                    item.get(
                        "audio_file",
                        ""
                    )
                )


                if audio_path.exists():

                    with open(
                        audio_path,
                        "rb"
                    ) as audio:

                        audio_bytes = audio.read()


                    st.audio(
                        audio_bytes,
                        format="audio/wav"
                    )


                    # --------------------------------------------------
                    # MARK AS PLAYED
                    # --------------------------------------------------

                    if st.button(

                        "▶️ Mark as Played",

                        key=(
                            f"library_play_"
                            f"{original_index}"
                        )
                    ):

                        record_play(

                            original_index,

                            item
                        )

                        st.success(
                            "▶️ Track added to listening activity."
                        )

                        st.rerun()


                    # --------------------------------------------------
                    # PLAY STATISTICS
                    # --------------------------------------------------

                    play_count = get_play_count(
                        original_index
                    )


                    last_played = get_last_played(
                        original_index
                    )


                    st.write(
                        f"▶️ **Played:** "
                        f"{play_count} time(s)"
                    )


                    st.write(
                        f"🕒 **Last Played:** "
                        f"{last_played}"
                    )


                    # --------------------------------------------------
                    # DOWNLOAD TRACK
                    # --------------------------------------------------

                    st.download_button(

                        label="⬇️ Download Track",

                        data=audio_bytes,

                        file_name=(
                            f"music_library_"
                            f"{display_index}.wav"
                        ),

                        mime="audio/wav",

                        key=(
                            f"library_download_"
                            f"{original_index}"
                        )
                    )


                # --------------------------------------------------
                # SHARE & EXPORT
                # --------------------------------------------------

                st.divider()


                st.write(
                    "### 📤 Share & Export"
                )


                share_text = metadata_to_text(
                    item
                )


                share_json = metadata_to_json(
                    item
                )


                share_col1, share_col2 = st.columns(2)


                with share_col1:

                    st.download_button(

                        label="📄 Export Metadata",

                        data=share_text,

                        file_name=(
                            f"music_metadata_"
                            f"{original_index}.txt"
                        ),

                        mime="text/plain",

                        key=(
                            f"metadata_text_"
                            f"{original_index}"
                        )
                    )


                with share_col2:

                    st.download_button(

                        label="🧾 Export JSON",

                        data=share_json,

                        file_name=(
                            f"music_metadata_"
                            f"{original_index}.json"
                        ),

                        mime="application/json",

                        key=(
                            f"metadata_json_"
                            f"{original_index}"
                        )
                    )


                st.text_area(

                    "📋 Shareable Music Information",

                    value=share_text,

                    height=250,

                    key=(
                        f"share_text_"
                        f"{original_index}"
                    )
                )


    else:

        st.info(
            "No music matches your filters."
        )


else:

    st.info(
        "Your music library is empty."
    )


# ==================================================
# PLAYLISTS
# ==================================================

st.divider()


st.subheader(
    "📚 My Playlists"
)


playlists = load_playlists()


# ==================================================
# CREATE PLAYLIST
# ==================================================

st.write(
    "Create a collection of your favorite music."
)


playlist_name = st.text_input(
    "🎵 Playlist Name",
    placeholder="Example: My Relaxing Music"
)


if st.button(
    "➕ Create Playlist"
):

    if playlist_name.strip() == "":

        st.warning(
            "⚠️ Please enter a playlist name."
        )

    else:

        created = create_playlist(
            playlist_name
        )


        if created:

            st.success(
                f"✅ Playlist '{playlist_name}' created!"
            )

            st.rerun()

        else:

            st.warning(
                "⚠️ A playlist with this name already exists."
            )


# ==================================================
# PLAYLIST LIST
# ==================================================

playlists = load_playlists()


if playlists:

    for playlist in playlists:

        playlist_title = playlist[
            "name"
        ]


        track_count = len(
            playlist["tracks"]
        )


        with st.expander(

            f"📚 {playlist_title} "
            f"({track_count} tracks)"
        ):

            st.write(
                f"**Playlist:** "
                f"{playlist_title}"
            )


            # --------------------------------------------------
            # DELETE PLAYLIST
            # --------------------------------------------------

            if st.button(

                "🗑️ Delete Playlist",

                key=(
                    f"delete_playlist_"
                    f"{playlist_title}"
                )
            ):

                delete_playlist(
                    playlist_title
                )


                st.success(
                    "Playlist deleted."
                )


                st.rerun()


            # --------------------------------------------------
            # ADD MUSIC
            # --------------------------------------------------

            current_history = load_history()


            if current_history:

                track_options = []


                for index, track in enumerate(
                    current_history
                ):

                    track_title = track.get(
                        "title",
                        f"Track {index + 1}"
                    )


                    favorite_symbol = (

                        "⭐"

                        if track.get(
                            "favorite",
                            False
                        )

                        else "☆"
                    )


                    track_options.append(

                        f"{index} | "
                        f"{favorite_symbol} "
                        f"{track_title}"
                    )


                selected_track = st.selectbox(

                    "🎵 Select Music",

                    track_options,

                    key=(
                        f"select_track_"
                        f"{playlist_title}"
                    )
                )


                selected_index = int(

                    selected_track.split(
                        " | "
                    )[0]
                )


                if st.button(

                    "➕ Add Track to Playlist",

                    key=(
                        f"add_track_"
                        f"{playlist_title}"
                    )
                ):

                    add_track_to_playlist(

                        playlist_title,

                        selected_index
                    )


                    st.success(
                        "✅ Track added to playlist!"
                    )


                    st.rerun()


            # --------------------------------------------------
            # SHOW PLAYLIST TRACKS
            # --------------------------------------------------

            st.write(
                "### 🎧 Playlist Tracks"
            )


            playlist_tracks = playlist[
                "tracks"
            ]


            if playlist_tracks:

                latest_history = load_history()


                for position, track_index in enumerate(

                    playlist_tracks,

                    start=1
                ):

                    if track_index >= len(
                        latest_history
                    ):

                        continue


                    track = latest_history[
                        track_index
                    ]


                    title = track.get(
                        "title",
                        f"Track {position}"
                    )


                    favorite_symbol = (

                        "⭐"

                        if track.get(
                            "favorite",
                            False
                        )

                        else "☆"
                    )


                    st.markdown(

                        f"**{position}. "
                        f"{favorite_symbol} "
                        f"{title}**"
                    )


                    track_col1, track_col2 = st.columns(2)


                    with track_col1:

                        st.write(
                            f"**Genre:** "
                            f"{track.get('genre', 'Unknown')}"
                        )


                        st.write(
                            f"**Mood:** "
                            f"{track.get('mood', 'Unknown')}"
                        )


                    with track_col2:

                        st.write(
                            f"**Duration:** "
                            f"{track.get('duration', 'Unknown')}"
                        )


                        st.write(
                            f"**Created:** "
                            f"{track.get('created_at', 'Unknown')}"
                        )


                    audio_path = Path(
                        track.get(
                            "audio_file",
                            ""
                        )
                    )


                    if audio_path.exists():

                        with open(

                            audio_path,

                            "rb"

                        ) as audio:

                            audio_bytes = audio.read()


                        st.audio(

                            audio_bytes,

                            format="audio/wav"
                        )


                        st.download_button(

                            label="⬇️ Download",

                            data=audio_bytes,

                            file_name=(
                                f"playlist_"
                                f"{position}.wav"
                            ),

                            mime="audio/wav",

                            key=(
                                f"playlist_download_"
                                f"{playlist_title}_"
                                f"{position}"
                            )
                        )


                    if st.button(

                        "➖ Remove from Playlist",

                        key=(

                            f"remove_track_"

                            f"{playlist_title}_"

                            f"{track_index}"
                        )
                    ):

                        remove_track_from_playlist(

                            playlist_title,

                            track_index
                        )


                        st.success(
                            "Track removed."
                        )


                        st.rerun()


                    st.divider()


            else:

                st.info(
                    "This playlist is empty. "
                    "Add some music!"
                )


else:

    st.info(
        "No playlists created yet."
    )


# ==================================================
# RECENTLY PLAYED
# ==================================================

st.divider()


st.subheader(
    "▶️ Recently Played"
)


activity = load_activity()


if activity:

    recent_activity = activity[-10:]


    for index, item in enumerate(

        reversed(recent_activity),

        start=1
    ):

        title = item.get(
            "title",
            f"Track {index}"
        )


        genre = item.get(
            "genre",
            "Unknown"
        )


        mood = item.get(
            "mood",
            "Unknown"
        )


        played_at = item.get(
            "played_at",
            "Unknown"
        )


        with st.expander(

            f"▶️ {title} — "
            f"{played_at}"
        ):

            st.write(
                f"**Genre:** {genre}"
            )


            st.write(
                f"**Mood:** {mood}"
            )


            st.write(
                f"**Played At:** {played_at}"
            )


            audio_path = Path(
                item.get(
                    "audio_file",
                    ""
                )
            )


            if audio_path.exists():

                with open(
                    audio_path,
                    "rb"
                ) as audio:

                    audio_bytes = audio.read()


                st.audio(
                    audio_bytes,
                    format="audio/wav"
                )

else:

    st.info(
        "No listening activity yet."
    )


# ==================================================
# LISTENING STATISTICS
# ==================================================

st.divider()


st.subheader(
    "📈 Listening Statistics"
)


activity = load_activity()


total_plays = len(
    activity
)


played_track_indexes = [

    item.get(
        "track_index"
    )

    for item in activity

    if item.get(
        "track_index"
    ) is not None
]


unique_tracks = len(
    set(played_track_indexes)
)


if activity and played_track_indexes:

    most_played_index = max(

        set(played_track_indexes),

        key=lambda index: sum(

            1

            for item in activity

            if item.get(
                "track_index"
            ) == index
        )
    )


    most_played_count = sum(

        1

        for item in activity

        if item.get(
            "track_index"
        ) == most_played_index
    )


    most_played_title = next(

        (

            item.get(
                "title",
                "Unknown"
            )

            for item in activity

            if item.get(
                "track_index"
            ) == most_played_index

        ),

        "Unknown"
    )

else:

    most_played_count = 0

    most_played_title = "None"


stat_col1, stat_col2, stat_col3 = st.columns(3)


with stat_col1:

    st.metric(
        "▶️ Total Plays",
        total_plays
    )


with stat_col2:

    st.metric(
        "🎵 Unique Tracks Played",
        unique_tracks
    )


with stat_col3:

    st.metric(
        "🔥 Most Played",
        most_played_count
    )


if activity:

    st.write(
        f"🔥 **Most Played Track:** "
        f"{most_played_title}"
    )

else:

    st.write(
        "🔥 **Most Played Track:** None"
    )


if activity:

    if st.button(
        "🗑️ Clear Listening Activity"
    ):

        clear_activity()

        st.success(
            "✅ Listening activity cleared."
        )

        st.rerun()


# ==================================================
# GENERATION HISTORY
# ==================================================

st.divider()


st.subheader(
    "📖 Generation History"
)


current_history = load_history()


if current_history:

    for index, item in enumerate(

        reversed(current_history),

        start=1
    ):

        title = item.get(
            "title",
            f"Generation {index}"
        )


        created_at = item.get(
            "created_at",
            "Unknown time"
        )


        favorite_symbol = (

            "⭐"

            if is_favorite(item)

            else "☆"
        )


        with st.expander(

            f"{favorite_symbol} "
            f"{title} — {created_at}"
        ):

            st.write(
                f"**Prompt:** "
                f"{item.get('prompt', '')}"
            )


            st.write(
                f"**Genre:** "
                f"{item.get('genre', 'Unknown')}"
            )


            st.write(
                f"**Mood:** "
                f"{item.get('mood', 'Unknown')}"
            )


            st.write(
                f"**Duration:** "
                f"{item.get('duration', 'Unknown')}"
            )


            st.write(
                f"**Mode:** "
                f"{item.get('generation_mode', 'Balanced')}"
            )


            st.write(
                f"**Creativity:** "
                f"{item.get('creativity', 0.7)}"
            )


            st.write(
                f"**Audio Type:** "
                f"{item.get('audio_type', 'Instrumental')}"
            )


            st.write(
                f"**Favorite:** "
                f"{'Yes ⭐' if is_favorite(item) else 'No'}"
            )


            audio_path = Path(
                item.get(
                    "audio_file",
                    ""
                )
            )


            if audio_path.exists():

                with open(
                    audio_path,
                    "rb"
                ) as audio:

                    audio_bytes = audio.read()


                st.audio(
                    audio_bytes,
                    format="audio/wav"
                )


                st.download_button(

                    label="⬇️ Download",

                    data=audio_bytes,

                    file_name=(
                        f"music_{index}.wav"
                    ),

                    mime="audio/wav",

                    key=(
                        f"download_{index}"
                    )
                )


else:

    st.info(
        "No music has been generated yet."
    )


# ==================================================
# CLEAR HISTORY
# ==================================================

if current_history:

    st.divider()


    if st.button(
        "🗑️ Clear Generation History"
    ):

        clear_history()


        st.success(
            "✅ Generation history cleared."
        )


        st.rerun()
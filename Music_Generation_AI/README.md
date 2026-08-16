# 🎵 MusicGenerationAI

An AI-powered Music Generation Platform built using **Python, Streamlit, Hugging Face Transformers, PyTorch, and MusicGen**.

MusicGenerationAI allows users to generate original music from text prompts with customizable music settings, AI-powered generation, music library management, playlists, listening statistics, activity tracking, and downloadable generated audio.

---

# 📌 Project Overview

MusicGenerationAI is an intelligent Generative AI application designed to create music using text prompts and the powerful **MusicGen** model.

The project provides an interactive user interface where users can describe the type of music they want and generate AI-powered audio based on their prompts.

The application includes music generation, a generated music library, playlists, listening statistics, activity tracking, and music history management.

The application is built using Streamlit and integrates **MusicGen with Hugging Face Transformers and PyTorch** to provide an interactive AI music generation experience.

---

# ✨ Features

✔️ Modern Premium UI Design

✔️ AI Music Generation from Text Prompts

✔️ MusicGen AI Model

✔️ Custom Music Prompts

✔️ Genre-Based Music Generation

✔️ Mood-Based Music Generation

✔️ Custom Music Duration

✔️ Creative Music Generation

✔️ Creativity Control

✔️ Generated Music Library

✔️ Music History

✔️ Favorite Music Tracks

✔️ Playlist Management

✔️ Listening Statistics

✔️ Activity Tracking

✔️ Audio Playback

✔️ Download Generated Music

✔️ Generation Metadata

✔️ Interactive Streamlit Interface

---

# 🛠️ Technologies Used

| Technology                | Purpose                              |
| ------------------------- | ------------------------------------ |
| Python                    | Programming Language                 |
| Streamlit                 | Web Application Framework            |
| MusicGen                  | AI Music Generation Model            |
| Hugging Face Transformers | AI Model Integration                 |
| PyTorch                   | Deep Learning Framework              |
| SciPy                     | Audio Processing                     |
| NumPy                     | Numerical Processing                 |
| JSON                      | History, Playlist & Activity Storage |
| Pandas                    | Data Processing                      |

---

# 📂 Project Structure

```text
MUSICGENERATIONAI
│
├── __pycache__
│
├── ai
│   ├── __pycache__
│   ├── ai_generator.py
│   ├── config.py
│   └── model_config.py
│
├── assets
│
├── ai_model
│
├── screenshots
│   ├── 01_dashboard.png
│   ├── 02_music_generation.png
│   ├── 03_generated_music.png
│   ├── 04_music_library.png
│   ├── 05_playlists.png
│   └── 06_listening_statistics.png
│
├── generated_music
│   ├── activity.json
│   ├── history.json
│   ├── playlists.json
│   ├── day19_detailed_prompt.wav
│   ├── day19_lofi_prompt.wav
│   ├── day20_cinematic.wav
│   ├── day20_electronic_pop.wav
│   ├── day21_acoustic.wav
│   ├── day21_futuristic.wav
│   ├── day22_ambient.wav
│   ├── day22_jazz.wav
│   ├── day24_test.wav
│   ├── demo_music.wav
│   ├── music_20260805_221517.wav
│   ├── music_20260806_055531.wav
│   ├── music_20260806_061327.wav
│   ├── music_20260806_061408.wav
│   ├── music_20260809_194235.wav
│   ├── music_20260809_194356.wav
│   ├── music_20260809_195402.wav
│   ├── music_20260809_195429.wav
│   ├── music_20260809_195502.wav
│   ├── music_20260809_195525.wav
│   ├── music_20260809_195535.wav
│   ├── musicgen_acoustic.wav
│   ├── musicgen_output.wav
│   ├── musicgen_sad_piano.wav
│   └── musicgen_test.wav
│
├── styles
│
├── venv
│
├── activity.py
├── ai_musicgen_test.py
├── app.py
├── export_utils.py
├── history.py
├── music_generator.py
├── playlist.py
├── README.md
├── requirements.txt
└── test_ai_model.py
```

---

# 📸 Screenshots

### 🏠 Dashboard

![Dashboard](https://github.com/Abhigna13/MusicGenerationAI/blob/main/assets/screenshots/01_dashboard.png)

---

### 🎵 Music Generation

![Music Generation](https://github.com/Abhigna13/MusicGenerationAI/blob/main/assets/screenshots/02_music_generation.png)

---

### 🎧 Generated Music

![Generated Music](https://github.com/Abhigna13/MusicGenerationAI/blob/main/assets/screenshots/03_generated_music.png)

---

### 🎼 Music Library

![Music Library](https://github.com/Abhigna13/MusicGenerationAI/blob/main/assets/screenshots/04_music_library.png)

---

### 📋 Playlists

![Playlists](https://github.com/Abhigna13/MusicGenerationAI/blob/main/assets/screenshots/05_playlists.png)

---

### 📊 Listening Statistics

![Listening Statistics](https://github.com/Abhigna13/MusicGenerationAI/blob/main/assets/screenshots/06_listening_statistics.png)

---

# ⚙️ Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/Abhigna13/MusicGenerationAI.git
```

---

### 2. Navigate to Project Folder

```bash
cd MusicGenerationAI
```

---

### 3. Create Virtual Environment

```bash
python -m venv venv
```

---

### 4. Activate Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### macOS/Linux

```bash
source venv/bin/activate
```

---

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 6. Run Application

```bash
streamlit run app.py
```

---

### 7. Open Browser

```text
http://localhost:8501
```

---

# 🎼 Music Generation

MusicGenerationAI allows users to create music using natural-language prompts.

Users can customize their music generation experience using options such as:

* Music Prompt
* Genre
* Mood
* Duration
* Generation Mode
* Creativity Level

For example:

```text
Create a peaceful piano melody for studying.
```

The MusicGen AI model processes the prompt and generates an audio track based on the requested musical characteristics.

Generated audio files are automatically stored in the `generated_music` directory.

---

# 📚 Music Library

The application provides a dedicated music library where users can access their generated tracks.

The music library allows users to:

* View generated music
* Play audio
* Manage generated tracks
* Access previously generated music
* Download audio files

---

# ⭐ Favorites & Playlists

MusicGenerationAI allows users to organize their generated music through playlists and favorite tracks.

Users can:

* Add tracks to favorites
* Create playlists
* Add generated tracks to playlists
* Manage saved music
* Access organized music collections

Playlist information is maintained using:

```text
generated_music/playlists.json
```

---

# 📜 Music History & Activity

The application maintains information about previously generated music and user activity.

### Music History

The history system stores information related to generated tracks, including generation details and timestamps.

History data is maintained using:

```text
generated_music/history.json
```

### Activity Tracking

The application also records user activity through:

```text
generated_music/activity.json
```

This allows the application to provide a more organized music-generation experience.

---

# 📊 Listening Statistics

The application provides listening statistics to help users understand their music activity.

The statistics section can provide information related to:

* Total Generated Tracks
* Music Listening Activity
* Favorite Tracks
* Playlist Activity
* Music Collection
* Generation Activity

This provides an interactive overview of the user's AI-generated music experience.

---

# 🤖 AI Model

MusicGenerationAI uses **MusicGen Small**, a Generative AI music model integrated through Hugging Face Transformers.

MusicGen converts natural-language descriptions into musical audio and enables prompt-based music generation.

### Model

```text
facebook/musicgen-small
```

### Model Type

```text
MusicGen Small
```

### Framework

```text
Hugging Face Transformers + PyTorch
```

The project also includes dedicated AI testing and model-related files:

```text
ai_musicgen_test.py
test_ai_model.py
ai/ai_generator.py
ai/config.py
ai/model_config.py
```

---

# 💾 Generated Music

The project stores generated audio files inside the:

```text
generated_music
```

directory.

The generated collection contains multiple AI-created tracks, including:

* Cinematic Music
* Electronic Pop
* Acoustic Music
* Futuristic Music
* Ambient Music
* Jazz Music
* Lo-Fi Music
* Piano Music
* Test Generated Music

Audio files are stored in WAV format for playback and further use.

---

# 🚀 Future Enhancements

* Multiple Music Generation Models
* Longer Music Generation
* Advanced Music Controls
* Instrument Selection
* Tempo & BPM Control
* Audio Upload & Transformation
* Music-to-Music Generation
* AI Lyrics Generation
* Voice & Singing Generation
* Advanced Audio Editing
* Music Visualization
* Music Sharing
* Cloud Deployment
* GPU Acceleration
* Advanced Audio Effects
* Real-Time Music Generation
* Mobile-Friendly Music Generation

---

# 👨‍💻 Author

**Abhigna Nadupalli**

AI & Data Science Student

Python Developer | Generative AI Enthusiast

---

# ⭐ Support

If you like this project, please consider giving it a **⭐ Star** on GitHub.

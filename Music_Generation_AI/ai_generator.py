import torch
from pathlib import Path
from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy.io.wavfile as wavfile


MODEL_NAME = "facebook/musicgen-small"

_model = None
_processor = None


def get_device():
    """Return the device used for AI music generation."""
    return "cuda" if torch.cuda.is_available() else "cpu"


def get_model_name():
    """Return the MusicGen model name."""
    return MODEL_NAME


def is_model_available():
    """Check whether the MusicGen model can be loaded."""
    try:
        from transformers import MusicgenForConditionalGeneration
        return True
    except ImportError:
        return False


def get_model_status():
    """Return the current MusicGen model status."""
    if not is_model_available():
        return "MusicGen unavailable"

    return "MusicGen ready"


def get_model_info():
    """Return basic information about the AI model."""

    return {
        "model_name": MODEL_NAME,
        "device": get_device(),
        "cuda_available": torch.cuda.is_available(),
        "library": "Hugging Face Transformers",
        "model_type": "MusicGen Small"
    }


def load_model():
    """Load MusicGen model and processor only when needed."""
    global _model, _processor

    if _model is None or _processor is None:

        print("Loading MusicGen model...")

        _processor = AutoProcessor.from_pretrained(
            MODEL_NAME
        )

        _model = MusicgenForConditionalGeneration.from_pretrained(
            MODEL_NAME
        )

        device = get_device()

        if device == "cuda":
            _model = _model.to(device)

    return _processor, _model


def generate_ai_music(
    prompt,
    output_path="generated_music/musicgen_output.wav",
    max_new_tokens=256
):
    """Generate AI music from a text prompt."""

    processor, model = load_model()

    inputs = processor(
        text=[prompt],
        padding=True,
        return_tensors="pt"
    )

    device = get_device()

    if device == "cuda":
        inputs = {
            key: value.to(device)
            for key, value in inputs.items()
        }

    print("Generating music...")

    with torch.no_grad():

        audio_values = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens
        )

    audio = audio_values[0, 0].cpu().numpy()

    sample_rate = model.config.audio_encoder.sampling_rate

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    wavfile.write(
        str(output_path),
        sample_rate,
        audio
    )

    print("Music generated successfully!")
    print(f"Saved at: {output_path}")

    return str(output_path)
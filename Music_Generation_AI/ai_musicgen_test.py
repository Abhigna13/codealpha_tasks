import torch
from transformers import AutoProcessor, MusicgenForConditionalGeneration
from scipy.io.wavfile import write
from pathlib import Path

MODEL_NAME = "facebook/musicgen-small"

print("Loading MusicGen model...")
print("This may take some time on CPU.")

processor = AutoProcessor.from_pretrained(MODEL_NAME)
model = MusicgenForConditionalGeneration.from_pretrained(MODEL_NAME)

prompt = "smooth jazz music, sophisticated and relaxed mood, warm saxophone, soft piano, upright bass, gentle jazz drums, expressive melody, medium-slow tempo, intimate evening atmosphere"

inputs = processor(
    text=[prompt],
    padding=True,
    return_tensors="pt"
)

print("Generating music...")

with torch.no_grad():
    audio_values = model.generate(
        **inputs,
        max_new_tokens=256
    )

audio = audio_values[0, 0].cpu().numpy()

sample_rate = model.config.audio_encoder.sampling_rate

output_folder = Path("generated_music")
output_folder.mkdir(exist_ok=True)

output_file = output_folder / "day22_jazz.wav"

write(
    output_file,
    sample_rate,
    audio
)

print("Music generated successfully!")
print(f"Saved to: {output_file}")
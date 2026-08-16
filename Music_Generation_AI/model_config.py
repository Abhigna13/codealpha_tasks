from pathlib import Path
import torch


MODEL_NAME = (
    "AI Music Generation Model"
)


MODEL_CACHE_DIR = Path(
    "assets/ai_model"
)


MODEL_CACHE_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def get_device():

    if torch.cuda.is_available():

        return "cuda"

    return "cpu"


DEVICE = get_device()


def get_model_information():

    return {

        "model_name": MODEL_NAME,

        "device": DEVICE,

        "cuda_available":
            torch.cuda.is_available(),

        "cache_directory":
            str(MODEL_CACHE_DIR)
    }
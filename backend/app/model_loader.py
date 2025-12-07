from faster_whisper import WhisperModel
import torch

# Choose model size
MODEL_SIZE = "medium"

# Detect device
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Loading FasterWhisper model: {MODEL_SIZE} on {DEVICE}...")

# Load model with super-fast INT8 mode
model = WhisperModel(
    MODEL_SIZE,
    device=DEVICE,
    compute_type="int8"  # int8 = FAST + LOW MEMORY + good accuracy
)

print("FasterWhisper model loaded successfully.")

def get_model():
    return model

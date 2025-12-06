import whisper
import torch

# Configuration
# "base" or "small" is best for CPU. "medium" needs a GPU with 5GB+ VRAM.
MODEL_SIZE = "small" 
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Loading Whisper model: {MODEL_SIZE} on {DEVICE}...")
model = whisper.load_model(MODEL_SIZE).to(DEVICE)
print("Model loaded successfully.")

def get_model():
    return model
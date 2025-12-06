import torch
import numpy as np
import librosa
import whisper
from .model_loader import get_model, DEVICE

def load_audio_16k(path_or_array):
    """
    Ensures audio is 16kHz mono, whether input is a file path or a numpy array.
    """
    target_sr = 16000
    
    if isinstance(path_or_array, str):
        # It's a file path
        audio, _ = librosa.load(path_or_array, sr=target_sr, mono=True)
    else:
        # It's already a numpy array (from memory slicing)
        audio = path_or_array

    # CRITICAL FIX 1: Ensure Float32
    return audio.astype(np.float32)

def get_whisper_embedding(input_data) -> torch.Tensor:
    """
    Extract a pronunciation embedding using Whisper's encoder.
    """
    model = get_model()
    audio = load_audio_16k(input_data)

    # CRITICAL FIX 2: Force 1D array (Flatten) to avoid "incorrect audio shape"
    audio_tensor = torch.tensor(audio).flatten()

    # CRITICAL FIX 3: Pad or Trim to 30 seconds
    # Whisper's Encoder expects exactly 30s of audio (480,000 samples)
    # This function handles the padding automatically.
    audio_tensor = whisper.pad_or_trim(audio_tensor)

    # Compute Log Mel Spectrogram
    mel = whisper.log_mel_spectrogram(audio_tensor).to(DEVICE)
    
    # Encoder
    with torch.no_grad():
        encoded = model.encoder(mel.unsqueeze(0)) # shape: (1, n_ctx, n_state)

    # Average Pooling for a single vector
    embedding = encoded.mean(dim=1).squeeze(0)
    
    # Normalize
    embedding = embedding / (embedding.norm(p=2) + 1e-8)
    
    return embedding.cpu()

def cosine_similarity(a: torch.Tensor, b: torch.Tensor) -> float:
    return float(torch.dot(a, b).item())
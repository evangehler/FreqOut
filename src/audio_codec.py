import numpy as np
import librosa
import soundfile as sf

from classes import DeltaSlice

# Guess frequency based on weighted average of deltaSlices
def resolve_frequency(delta_slice, freqs_full):
    freqs = freqs_full[delta_slice.freq_indices]
    mags = delta_slice.magnitude_deltas

    total_weight = np.sum(mags)
    if total_weight == 0:
        return None  # or np.nan

    weighted_freq = np.sum(freqs * mags) / total_weight
    return weighted_freq

# ENCODE / DECODE FUNCTIONALITY
# Encode character to frequency
def char_to_freq(c, base=4000, step=50):
    if c == ' ':
        return base + 26 * step
    c = c.lower()
    if 'a' <= c <= 'z':
        return base + step * (ord(c) - ord('a'))
    raise ValueError(f"Unsupported character: {c}")

# Decode characters from frequencies
def freq_to_char(freq, base=4000, step=50):
    index = round((freq - base) / step)
    if 0 <= index < 26:
        return chr(ord('a') + index)
    elif index == 26:
        return ' '
    else:
        return '?'

# Encode Message 
def encode_message(message, input_path, output_path):
    sr = 44100
    spacing = 0.15  # time between characters in seconds
    duration = 0.1  # tone length
    amplitude = 0.01

    # Load base audio
    y, _ = librosa.load(input_path, sr=sr, mono=True)
    y_encoded = np.copy(y)

    for i, char in enumerate(message):
        try:
            freq = char_to_freq(char)
        except ValueError:
            continue 

        start_time = 1.0 + i * spacing
        start_sample = int(start_time * sr)
        end_sample = int((start_time + duration) * sr)
        t = np.arange(end_sample - start_sample) / sr
        sine_wave = amplitude * np.sin(2 * np.pi * freq * t)
        y_encoded[start_sample:end_sample] += sine_wave

    y_encoded = np.clip(y_encoded, -1.0, 1.0)
    sf.write(output_path, y_encoded, sr)
    print(f"Encoded message written to {output_path}")

# Decode Message using DeltaSlice and frequency resolution function
def decode_message(delta_slices, freqs_full, base_freq=4000, step=50, window=0.005):

    if not delta_slices:
        print("No delta slices to decode.")
        return

    # Sort by timestamp
    delta_slices.sort(key=lambda ds: ds.timestamp)

    grouped = []
    current_group = []
    last_time = None

    print(f"Delta range: {delta_slices[0].timestamp:.2f}s to {delta_slices[-1].timestamp:.2f}s")

    for ds in delta_slices:
        if last_time is None or abs(ds.timestamp - last_time) <= window:
            current_group.append(ds)
        else:
            grouped.append(current_group)
            current_group = [ds]
        last_time = ds.timestamp

    if current_group:
        grouped.append(current_group)

    decoded_message = ""
    for i, group in enumerate(grouped):
        # Merge all DeltaSlices in group
        combined_indices = np.concatenate([g.freq_indices for g in group])
        combined_magnitudes = np.concatenate([g.magnitude_deltas for g in group])

        combined_ds = DeltaSlice(
            timestamp=np.mean([g.timestamp for g in group]),
            freq_indices=combined_indices,
            magnitude_deltas=combined_magnitudes
        )

        freq = resolve_frequency(combined_ds, freqs_full)
        if freq is None:
            decoded_char = '?'
        else:
            decoded_char = freq_to_char(freq, base=base_freq, step=step)

        print(f"Pulse {i+1}: Avg Time = {combined_ds.timestamp:.2f}s, Est. Freq = {freq:.2f} Hz -> '{decoded_char}'")
        decoded_message += decoded_char

    print(f"\nDecoded message: {decoded_message}")
    return decoded_message

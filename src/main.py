import numpy as np
import matplotlib.pyplot as plt
import librosa
import hashlib
import soundfile as sf

from classes import DeltaSlice, TimeSlice
from audio_codec import encode_message, decode_message
from plotting import plot_spectrogram, plot_deltas, plot_stack

# Function iterates through audio file, computing and saving results of FFTs
def compute_time_slice(filename, sr = 44100, n_fft=1024, hop_length=64):
    #ignore sr / make mono
    y, _ = librosa.load(filename, sr=sr, mono=True)
    #matrix of our fft bins
    stft_matrix = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)
    #matrix of frequency magnitudes
    magnitude_matrix = np.abs(stft_matrix)

    freqs = librosa.fft_frequencies(sr=sr, n_fft=n_fft)
    times = librosa.frames_to_time(np.arange(magnitude_matrix.shape[1]), sr=sr, hop_length=hop_length)

    slices = []
    for i,t in enumerate(times):
        magnitudes = magnitude_matrix[:,i]
        slices.append(TimeSlice(timestamp=t, freqs=freqs, magnitudes=magnitudes))

    return slices

# Hash Function with hashlib
def hash_magnitudes(magnitudes, precision=3):
    rounded = np.round(magnitudes, decimals=precision)
    return hashlib.md5(rounded.tobytes()).hexdigest()

# Function compares two arrays of slices and stores the resulting slices.
def compute_deltas(reference_slices, test_slices, threshold=0.05, precision=3):
    # hash lookup for identical slices
    ref_hashes = {hash_magnitudes(s.magnitudes, precision): s for s in reference_slices}

    # Pre-index reference slices
    ref_by_time = {round(s.timestamp, 3): s for s in reference_slices}

    delta_slices = []

    for test_slice in test_slices:
        test_hash = hash_magnitudes(test_slice.magnitudes, precision)

        # Skip if identitical
        if test_hash in ref_hashes:
            continue

        # Get reference frame via rounded timestamp
        ref_slice = ref_by_time.get(round(test_slice.timestamp, 3))

        if ref_slice:
            delta = np.abs(test_slice.magnitudes - ref_slice.magnitudes)
            significant = delta > threshold
            if np.any(significant):
                indices = np.where(significant)[0]
                deltas = delta[indices]
                delta_slices.append(DeltaSlice(
                    timestamp=test_slice.timestamp,
                    freq_indices=indices,
                    magnitude_deltas=deltas
                ))
    print(f"{len(delta_slices)} slices had differences.")
    return delta_slices

#insert sinewave for testing
def dope_audio(input_path, output_path, frequency=5000, start_time=5.0, duration=0.5, amplitude=0.02):
    # Load original
    sr = 44100
    y, _ = librosa.load(input_path, sr=sr, mono=True)

    # Time window to insert sine
    start_sample = int(start_time * sr)
    end_sample = int((start_time + duration) * sr)

    # Create sine
    t = np.arange(end_sample - start_sample) / sr
    sine_wave = amplitude * np.sin(2 * np.pi * frequency * t)

    # Add sine to a copy
    y_doped = np.copy(y)
    y_doped[start_sample:end_sample] += sine_wave

    # Clip to avoid overflow
    y_doped = np.clip(y_doped, -1.0, 1.0)

    # Save
    sf.write(output_path, y_doped, sr)
    print(f"Doped audio written to {output_path}")

# Main
def main():
    # PATHS
    original_path = "src/audio_files/input.wav"
    doped_path = "src/audio_files/doped.wav"

    # SAMPLE RATE
    sr = 44100

    # ENCODE MESSAGE
    encode_message("we love a good secret message", original_path, doped_path)

    # Compute TimeSlices for both files
    slices_orig = compute_time_slice(original_path, sr=sr)
    slices_doped = compute_time_slice(doped_path, sr=sr)

    # Compute DeltaSlices
    deltas = compute_deltas(slices_orig, slices_doped, threshold=0.05)

    decoded = decode_message(deltas, slices_doped[0].freqs)
    plot_stack(slices_orig, slices_doped, deltas, decoded_message=decoded)
 
# Main
if __name__ == "__main__":
    main()
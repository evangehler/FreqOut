import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import librosa
import hashlib
import soundfile as sf

from classes import DeltaSlice, TimeSlice
from audio_codec import encode_message, decode_message

from gui import GUI

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

# Basic spectrogram implementation to see if STFT worked
def plot_spectrogram(slices):
    time_stamps = [s.timestamp for s in slices]
    magnitudes = np.array([s.magnitudes for s in slices]).T

    plt.figure(figsize=(10, 4))
    plt.imshow(20 * np.log10(magnitudes + 1e-6), aspect='auto', origin='lower',
               extent=[time_stamps[0], time_stamps[-1], slices[0].freqs[0], slices[0].freqs[-1]])
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.colorbar(label="Magnitude (dB)")
    plt.title("Spectrogram")
    plt.ylim(20, 24000)
    plt.yscale('log')
    plt.grid(True, which='both', ls='--')
    plt.show()

# Matplotlib function for deltaSlices
def plot_deltas(delta_slices, freqs_full):
    times = []
    freqs = []
    mags = []

    for ds in delta_slices:
        times.extend([ds.timestamp] * len(ds.freq_indices))
        freqs.extend(freqs_full[ds.freq_indices])
        mags.extend(ds.magnitude_deltas)

    plt.figure(figsize=(12, 5))
    scatter = plt.scatter(times, freqs, c=mags, cmap='plasma', s=10)
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.yscale("log")
    plt.colorbar(scatter, label="Delta Magnitude")
    plt.title("Detected Frequency Differences Over Time")
    plt.grid(True, which='both', ls='--')
    plt.ylim(20, 24000)
    plt.show()

# Main
def main():
    gui = GUI()

    return 0 #remember to delete this
    original_path = "src/aphex_test.wav"
    doped_path = "src/aphex_doped.wav"

    sr = 44100

    # Inject sine tone
    # dope_audio(original_path, doped_path, frequency=5000, start_time=5.0, duration=0.5)

    # ENCODE MESSAGE
    encode_message("we love thomas miller", original_path, doped_path)

    # Compute TimeSlices
    slices_orig = compute_time_slice(original_path, sr=sr)
    slices_doped = compute_time_slice(doped_path, sr=sr)

    #DeltaSlices
    deltas = compute_deltas(slices_orig, slices_doped, threshold=0.05)

    # Send differences to console / update
    print(f"{len(deltas)} slices had differences.")
    
    # For print debugging
    # for delta in deltas:
    #     freqs = slices_doped[0].freqs[delta.freq_indices]
    #     for f, d in zip(freqs, delta.magnitude_deltas):
    #         print(f"Time: {delta.timestamp:.4f}s | Delta: {d:.3f} at {f:.1f} Hz")
    
    # When it was a single sine wave
    # guess_frequency(deltas, slices_doped[0].freqs)
    
    
    decode_message(deltas, slices_doped[0].freqs)
    plot_deltas(deltas, slices_doped[0].freqs)

# Main
if __name__ == "__main__":
    main()
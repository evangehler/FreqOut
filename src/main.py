import numpy as np
import librosa
import hashlib

from classes import DeltaSlice, TimeSlice
from audio_codec import encode_message, decode_message
from plotting import plot_spectrogram, plot_deltas, plot_stack
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
    print(f"{len(delta_slices)} slices had differences.")
    return delta_slices

# Main
def main():
    # Launch GUI
    gui = GUI()

    message = gui.message
    original_path = gui.inFile
    doped_path = gui.outFile

    if not all([message, original_path, doped_path]):
        print("Missing required input from GUI.")
        return

    # Encode
    encode_message(message, original_path, doped_path)

    # Analyze
    slices_orig = compute_time_slice(original_path)
    slices_doped = compute_time_slice(doped_path)
    deltas = compute_deltas(slices_orig, slices_doped, threshold=0.05)

    # Decode & Plot
    decoded = decode_message(deltas, slices_doped[0].freqs)
    plot_stack(slices_orig, slices_doped, deltas, decoded_message=decoded)
 
# Main
if __name__ == "__main__":
    main()
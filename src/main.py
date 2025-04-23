import numpy as np
import librosa
import sys

from hash_list import HashList
from hash_generator import HashGenerator
from classes import DeltaSlice, TimeSlice
from audio_codec import encode_message, decode_message
from plotting import plot_stack
from gui import GUI, ConsoleRedirect

# Function iterates through audio file, computing and saving results of FFTs
def compute_time_slices(filename, sr = 44100, n_fft=1024, hop_length=64):
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

# Function compares two arrays of slices and stores the resulting slices.
def compute_deltas(orig_slices, doped_slices, threshold=0.05, precision=3):
    if len(orig_slices) != len(doped_slices):
        print("Different number of FFT slices per file. Are the audio files different lengths?")
        return
    
    orig_list = HashList(orig_slices)
    doped_list = HashList(doped_slices)

    delta_slices = []
    for index, (orig_hash, doped_hash) in enumerate(zip(orig_list.get_hashes(), doped_list.get_hashes())):
        if orig_hash == doped_hash:
            continue
        else:
            orig_diff = orig_slices[index]
            doped_diff = doped_slices[index]
            delta = np.abs(orig_diff.magnitudes - doped_diff.magnitudes)
            significant = delta > threshold
            if np.any(significant):
                indices = np.where(significant)[0]
                deltas = delta[indices]
                delta_slices.append(DeltaSlice(
                    timestamp=orig_diff.timestamp,
                    freq_indices=indices,
                    magnitude_deltas=deltas
                ))
                
    print(f"{len(delta_slices)} slices had differences.")
    return delta_slices

def run_encode(message, orig_path, doped_path):
    print("Encoding message...")
    encode_message(message, orig_path, doped_path)
    print("Done encoding.")

def run_decode(orig_path, doped_path):
    print("Running decode pipeline...")
    slices_orig = compute_time_slices(orig_path)
    slices_doped = compute_time_slices(doped_path)

    deltas = compute_deltas(slices_orig, slices_doped)

    decoded = decode_message(deltas, slices_doped[0].freqs)
    plot_stack(slices_orig, slices_doped, deltas, decoded_message=decoded)

def main():
    gui = GUI()
    sys.stdout = ConsoleRedirect(gui.console, sys.__stdout__)
    sys.stderr = ConsoleRedirect(gui.console, sys.__stderr__)
    gui.set_callbacks(run_encode, run_decode)
    gui.root.mainloop()

if __name__ == "__main__":
    main()
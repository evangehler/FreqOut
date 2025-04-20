import numpy as np
import matplotlib.pyplot as plt
import librosa
from matplotlib.ticker import ScalarFormatter

class TimeSlice:
    def __init__(self, timestamp, freqs, magnitudes):
        self.timestamp = timestamp
        self.freqs = freqs
        self.magnitudes = magnitudes

def compute_time_slice(filename, sr = 44100, n_fft=2048, hop_length=512):
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

# Basic spectrogram to see if STFT worked
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

def main():
    slices = compute_time_slice("src/aphex_test.wav")
    print(f"{len(slices)} time slices extracted.")
    print(f"Sample slice: Time = {slices[0].timestamp:.3f}s, First frequency = {slices[0].freqs[0]:.1f}Hz, First mag = {slices[0].magnitudes[0]:.3f}")

    plot_spectrogram(slices)

if __name__ == "__main__":
    main()
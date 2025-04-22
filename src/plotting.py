import matplotlib.pyplot as plt
import numpy as np

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

# Plot stack of all three spectrogram and decoded message
def plot_stack(slices_orig, slices_doped, delta_slices, decoded_message=None):

    # Shared frequency/time data for original and doped
    time_stamps = [s.timestamp for s in slices_orig]
    freqs = slices_orig[0].freqs
    mag_orig = np.array([s.magnitudes for s in slices_orig]).T
    mag_doped = np.array([s.magnitudes for s in slices_doped]).T

    # Delta data
    times_deltas = []
    freqs_deltas = []
    mags_deltas = []
    for ds in delta_slices:
        times_deltas.extend([ds.timestamp] * len(ds.freq_indices))
        freqs_deltas.extend(freqs[ds.freq_indices])
        mags_deltas.extend(ds.magnitude_deltas)

    # Create independent subplots
    fig, axs = plt.subplots(3, 1, figsize=(12, 10))
    fig.canvas.manager.set_window_title("Spectrogram Comparison — FreqOut!")

    # Original Spectrogram
    axs[0].imshow(20 * np.log10(mag_orig + 1e-6), aspect='auto', origin='lower',
                  extent=[time_stamps[0], time_stamps[-1], freqs[0], freqs[-1]])
    axs[0].set_title("Original Spectrogram")
    axs[0].set_ylabel("Frequency (Hz)")
    axs[0].set_yscale('log')
    axs[0].set_ylim(20, 24000)
    axs[0].grid(True, which='both', ls='--')

    # Doped Spectrogram
    axs[1].imshow(20 * np.log10(mag_doped + 1e-6), aspect='auto', origin='lower',
                  extent=[time_stamps[0], time_stamps[-1], freqs[0], freqs[-1]])
    axs[1].set_title("Doped Spectrogram")
    axs[1].set_ylabel("Frequency (Hz)")
    axs[1].set_yscale('log')
    axs[1].set_ylim(20, 24000)
    axs[1].grid(True, which='both', ls='--')

    # Delta Spectrogram with auto-scaled axes
    scatter = axs[2].scatter(times_deltas, freqs_deltas, c=mags_deltas, cmap='plasma', s=10)
    axs[2].set_title("Delta Spectrogram")
    axs[2].set_xlabel("Time (s)")
    axs[2].set_ylabel("Frequency (Hz)")
    axs[2].set_yscale("log")
    axs[2].grid(True, which='both', ls='--')
    fig.colorbar(scatter, ax=axs[2], label="Delta Magnitude")

    # Best-fit axis limits for delta plot
    if times_deltas and freqs_deltas:
        axs[2].set_xlim(min(times_deltas), max(times_deltas))
        axs[2].set_ylim(min(freqs_deltas), max(freqs_deltas))

    if decoded_message:
        fig.text(0.5, 0.01, f"Decoded Message: \"{decoded_message}\"",
                 ha='center', fontsize=12, bbox=dict(facecolor='white', alpha=0.8, boxstyle='round'))

    plt.gcf().set_size_inches(960 / 100, 720 / 100) # Set window to 720x480
    plt.tight_layout(rect=[0, 0.03, 1, 1])  # Leave space at bottom
    plt.show()
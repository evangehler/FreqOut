import numpy as np
import scipy.io.wavfile as wav
import soundfile as sf
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

# load audio file
data, rate = sf.read("src\Windowlicker.flac")

# mono if stereo
if data.ndim > 1:
    data = data.mean(axis=1)

# apply FFT
fft_vals = np.fft.fft(data)
freqs = np.fft.fftfreq(len(data), 1/rate)

# only positive frequencies
mask = (freqs >= 0) & (freqs <= 24000)
fft_vals = np.abs(fft_vals[mask])
freqs = freqs[mask]

# Define desired tick positions
tick_positions = [20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000]

# Create the plot
plt.figure()
plt.semilogx(freqs, fft_vals)
plt.xlim(20, 24000)
plt.xticks(tick_positions)
plt.gca().xaxis.set_major_formatter(ScalarFormatter())
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.title("Average Frequencies In Signal")
plt.grid(True, which='both', ls='--')
plt.show()
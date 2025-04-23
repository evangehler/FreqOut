# Basic class for storing FFT bins
import numpy as np
class TimeSlice:
    def __init__(self, timestamp, freqs, magnitudes):
        self.timestamp = timestamp
        self.freqs = freqs
        self.magnitudes = magnitudes

    def to_bytes(self):
        """Convert TimeSlice to bytes by serializing its components"""
        timestamp_bytes = np.float64(self.timestamp).tobytes()
        freqs_bytes = self.freqs.tobytes() if isinstance(self.freqs, np.ndarray) else bytes(str(self.freqs), 'utf-8')
        magnitudes_bytes = self.magnitudes.tobytes() if isinstance(self.magnitudes, np.ndarray) else bytes(str(self.magnitudes), 'utf-8')
        return timestamp_bytes + freqs_bytes + magnitudes_bytes
    
# Essentially the same class as Timeslice, holds slices that have differences
class DeltaSlice:
    def __init__(self, timestamp, freq_indices, magnitude_deltas):
        self.timestamp = timestamp
        self.freq_indices = freq_indices
        self.magnitude_deltas = magnitude_deltas

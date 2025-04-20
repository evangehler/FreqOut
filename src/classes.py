# Basic class for storing FFT bins
class TimeSlice:
    def __init__(self, timestamp, freqs, magnitudes):
        self.timestamp = timestamp
        self.freqs = freqs
        self.magnitudes = magnitudes

# Essentially the same class as Timeslice, holds slices that have differences
class DeltaSlice:
    def __init__(self, timestamp, freq_indices, magnitude_deltas):
        self.timestamp = timestamp
        self.freq_indices = freq_indices
        self.magnitude_deltas = magnitude_deltas

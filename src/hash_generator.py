import numpy as np
class HashGenerator:
    def hash_items(self, items, precision=3):
        rounded = np.round(items, decimals=precision)
        # Convert magnitudes to a flat array of bytes
        flattened = rounded.flatten()
        hash_value = 0
        for val in flattened:
            # Use XOR to mix the bits of the hashed value and 10^6 for high resolution and uniqueness
            hash_value ^= int(val * 1e6)
            # Bitshift multiplication by 32 and adding the original value for entropy (randomness)
            hash_value = (hash_value << 5) + hash_value
        return hex(hash_value & 0xFFFFFFFFFFFFFFFF)  # Return a 64-bit hash as hex
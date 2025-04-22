class HashTable:
    def __init__(self, size=100):
        self.size = size
        self.table = [[] for _ in range(size)]  # Create a list of empty lists for chaining

    def custom_hash(self, magnitudes, precision=3):
        # Custom hash function (as defined earlier)
        rounded = np.round(magnitudes, decimals=precision)
        flattened = rounded.flatten()
        hash_value = 0
        for val in flattened:
            hash_value ^= int(val * 1e6)  # Scale and cast to int
            hash_value = (hash_value << 5) + hash_value  # Shift and add for more entropy
        return hex(hash_value & 0xFFFFFFFFFFFFFFFF)  # Return a 64-bit hash as hex

    def insert(self, magnitudes, slice_data):
        """Inserts a hash of the magnitudes and the associated data into the hash table."""
        hash_value = self.custom_hash(magnitudes)
        index = hash(hash_value) % self.size  # Use the built-in hash function to get the index
        # Handle collisions with chaining; store a tuple of (hash, magnitudes, slice_data)
        for stored_hash, _, _ in self.table[index]:
            if stored_hash == hash_value:
                return  # If hash already exists, we don't insert again
        self.table[index].append((hash_value, magnitudes, slice_data))

    def __contains__(self, hash_value):
        """Checks if a given hash exists in the hash table."""
        index = hash(hash_value) % self.size  # Get the index using the built-in hash function
        for stored_hash, _, _ in self.table[index]:
            if stored_hash == hash_value:
                return True
        return False

    def get_value(self, hash_value):
        """Returns the associated data (slice_data) for a given hash."""
        index = hash(hash_value) % self.size
        for stored_hash, _, slice_data in self.table[index]:
            if stored_hash == hash_value:
                return slice_data  # Return the associated TimeSlice data
        return None  # If the hash is not found
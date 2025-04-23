import numpy as np

class HashList:
    def __init__(self, items, precision=3):
        """Constructor takes an array of items and stores their hashes."""
        self.hashes = self.hash_items(items)

    def hash_items(self, items, precision=3):
        """Generate a hash for the given array of TimeSlice objects."""
        hashes = []  # Store individual hashes for each item
        for item in items:  # items is an array of TimeSlice objects
            val = item.to_bytes()  # Serialize the TimeSlice object into bytes
            
            # Convert the byte data to an integer
            val_int = int.from_bytes(val, byteorder='big')  # Convert bytes to integer
            
            # Initialize hash value for XOR and bit shifting
            hash_value = 0
            hash_value ^= val_int
            hash_value = (hash_value << 5) + hash_value

            # Append the hash to the list of hashes
            hashes.append(hex(hash_value & 0xFFFFFFFFFFFFFFFF))  # Return a 64-bit hash as hex

        return hashes  # Return an array of hashes

    def get_hashes(self):
        """Returns the list of hashes."""
        return self.hashes
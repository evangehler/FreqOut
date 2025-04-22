class HashTable:
    def __init__(self, values=None, capacity=8):
        self.capacity = capacity
        self.size = 0
        self.table = [None] * capacity
        if values.any():
            for v in values:
                self.insert(v)
            
    def __contains__(self, value):
        index = self._hash(value)
        probes = 0
        while self.table[index] is not None and probes < self.capacity:
            if self.table[index] == value:
                return True
            index = (index + 1) % self.capacity
            probes += 1
        return False

    def _hash(self, key):
        return hash(key) % self.capacity

    def _probe(self, index):
        while self.table[index] is not None and self.table[index][0] != self.key:
            index = (index + 1) % self.capacity
        return index

    def insert(self, value):
        index = self._hash(value)
        while self.table[index] is not None and self.table[index] != value:
            index = (index + 1) % self.capacity
        if self.table[index] != value:
            self.size += 1
            self.table[index] = value

    def get(self, key):
        index = self._hash(key)
        while self.table[index] is not None:
            if self.table[index][0] == key:
                return self.table[index][1]
            index = (index + 1) % self.capacity
        return None

    def _resize(self):
        old_table = self.table
        self.capacity *= 2
        self.size = 0
        self.table = [None] * self.capacity
        for item in old_table:
            if item is not None:
                self.insert(*item)

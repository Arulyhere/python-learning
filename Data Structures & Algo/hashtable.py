# !! CREDIT TO: RealPython on showcasing the ideas I learnt for implementing a Hashtable in Python !!

class HashTable:
    def __init__(self, size=8, load_factor_thres=0.75):
        # Argument handling when calling the Hashtable class
        if type(size) is not int:
            raise TypeError("Size must be an integer")
        elif size < 1:
            raise ValueError("Size must be positive.")
        if not isinstance(load_factor_thres, (int, float)):
            raise TypeError("Load factor must be a float or integer")
        elif (0 >= load_factor_thres < 1):
            raise ValueError("Load factor must a number between 0 and 1")
        self._pairs = [None] * size
        self.size = len(self._pairs)
        self._load_factor_thres = load_factor_thres
        self._collisioncount = 0
        self._keys = []


    def _hash(self, key):
        # Hash function used for key indexing
        return abs(hash(key)) % self.size 
    
    def _hash2(self, key):
        # Hash function used for step size
        largest_prime = self.__get_largest_prime()
        if self.size != 1:
            return largest_prime - self._hash(key) % largest_prime
        else:
            return 0
        
    def _isPrime(self, n):
        if n < 2:
            return False
        if n == 2 or n == 3:
            return True
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    def __get_largest_prime(self):
        for i in range(self.size, 1, -1):
            if self._isPrime(i):
                return i
            else:
                continue

    def __getitem__(self, key):
        for _, pair in self._probe(key): 
        # Error handling if the index found does NOT exist
            if pair is None:
                raise KeyError(str(key) + " does not exist")
            if pair[0] == key:
                return pair[1]
        raise KeyError(key)
    
    def __delitem__(self, key):
        for index, pair in self._probe(key):
            if pair is None:
                raise KeyError("Key does not exist to begin with.")
        # Error handling if the index found does NOT exist
            if pair[0] == key:
        # Deletes the pair from the hashmap
                del self._pairs[index]
                break
        else:
            raise KeyError(key)

    def __setitem__(self, key, value):
        # Resize the hashtable when the load factor is reached
        if self.load_factor >= self._load_factor_thres:
            self._auto_resize()
        for index, pair in self._probe(key):
            if pair is None or pair[0] == key:
                self._pairs[index] = (key, value)
                break

    def __iter__(self):
        # Allows iterable of dictionary, returns keys
        yield from self.keys

    def __str__(self):
        # String format of hashtable
        pairs = []
        for key, value in self.pairs:
            pairs.append(f"{key!r}: {value!r}")
        return "{" + ", ".join(pairs) + "}"


    @property
    # When the pairs property is called, each pair is returned
    def pairs(self):
        return {pair for pair in self._pairs if pair}
    @property
    # When the key property is called, each key is returned
    def keys(self):
        return {pair[0] for pair in self._pairs if pair}
    @property
    # When the value property is called, each value is returned
    def values(self):
        return {pair[1] for pair in self._pairs if pair}
    @property
    # Returns the load factor of the Hashtable
    def load_factor(self):
        return len(self.pairs) / self.size

    # Here, we are using a double hashing function for probing in the hashtable
    def _probe(self, key):
        index = self._hash(key)
        step_size = self._hash2(key)
        self._collisioncount = 0
        index = (index + (self._collisioncount * step_size)) % self.size 
        for _ in range(self.size):
            if self._pairs[index]:
                self._collisioncount += 1								
            yield index, self._pairs[index]
            index = (index + 1) % self.size

    def _auto_resize(self):
        copy = HashTable((self.size * 2))
        for key, value in self.pairs:
            copy[key] = value
        self._pairs = copy._pairs
        

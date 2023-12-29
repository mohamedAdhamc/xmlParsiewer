class CustomDict:
    """
    Custom dictionary implementation.

    Attributes:
    - keys (list): A list to store keys.
    - values (list): A list to store corresponding values.
    """

    def __init__(self):
        """
        Initialize an empty CustomDict.

        The CustomDict is implemented as a hash table with a list of buckets.
        The initial size of the hash table is set to 100.

        Attributes:
        - size (int): The initial size of the list of buckets.
        - buckets (list): A list of buckets, where each bucket is a list of key-value pairs.
        """
        self.size = 100  # Choose an initial size for the list of buckets
        self.buckets = [[] for _ in range(self.size)]

    def hash_function(self, key):
        """
        Custom hash function for both strings and numbers.

        Parameters:
        - key: The key (either string or number) to be hashed.

        Returns:
        An integer hash value computed based on the input key.
        """
        if isinstance(key, str):
            # Handle string keys
            hash_value = 0
            for char in key:
                hash_value = (hash_value * 31 + ord(char)) % self.size
        else:
            # Handle numeric keys
            hash_value = key % self.size

        return hash_value

    def set(self, key, value):
        """
        Set a key-value pair in the dictionary.

        Parameters:
        - key: The key to be set.
        - value: The value to be associated with the key.
        """
        hash_value = self.hash_function(key)
        bucket = self.buckets[hash_value]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                # Update value if key already exists
                bucket[i] = (key, value)
                return

        # Add a new key-value pair if the key is not present
        bucket.append((key, value))

    def get(self, key, default=None):
        """
        Get the value for a given key or a default value if the key is not present.

        Parameters:
        - key: The key to look up.
        - default: The value to return if the key is not present (default: None).

        Returns:
        The value associated with the key, or the default value if the key is not present.
        """
        hash_value = self.hash_function(key)
        bucket = self.buckets[hash_value]

        for k, v in bucket:
            if k == key:
                return v

        return default

    def items(self):
        """
        Return a zip of keys and values.

        Returns:
        A zip object containing pairs of keys and values.
        """
        return [(k, v) for bucket in self.buckets for k, v in bucket]

    def Values(self):
        """
        Return a list of values.

        Returns:
        A list containing all values in the dictionary.
        """
        return [v for bucket in self.buckets for k, v in bucket]

    def Keys(self):
        """
        Return a list of keys.

        Returns:
        A list containing all keys in the dictionary.
        """
        return [k for bucket in self.buckets for k, v in bucket]

    def __contains__(self, key):
        """
        Check if the dictionary contains a key.

        Parameters:
        - key: The key to check for existence.

        Returns:
        True if the key is present; False otherwise.
        """
        hash_value = self.hash_function(key)
        bucket = self.buckets[hash_value]

        for k, v in bucket:
            if k == key:
                return True

        return False

    def __iter__(self):
        """
        Return an iterator over keys.

        Returns:
        An iterator object over the keys in the dictionary.
        """
        return (k for bucket in self.buckets for k, v in bucket)

    def __len__(self):
        """
        Return the number of key-value pairs in the dictionary.

        Returns:
        The number of key-value pairs in the dictionary.
        """
        return sum(len(bucket) for bucket in self.buckets)

    def __repr__(self):
        """
        Return the key-value pairs in the dictionary as string.

        Returns:
        The key-value pairs in the dictionary as string.
        """
        return str(self.items())
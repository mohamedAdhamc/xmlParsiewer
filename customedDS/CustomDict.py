class CustomDict:
    """
    Custom dictionary implementation.

    Attributes:
    - keys (list): A list to store keys.
    - values (list): A list to store corresponding values.
    """

    def __init__(self):
        """Initialize an empty CustomDict."""
        self.keys = []
        self.values = []

    def set(self, key, value):
        """
        Set a key-value pair in the dictionary.

        Parameters:
        - key: The key to be set.
        - value: The value to be associated with the key.
        """
        for i, k in enumerate(self.keys):
            if k == key:
                # Update value if key already exists
                self.values[i] = value
                return
        # Add a new key-value pair if the key is not present
        self.keys.append(key)
        self.values.append(value)

    def get(self, key, default=None):
        """
        Get the value for a given key or a default value if the key is not present.

        Parameters:
        - key: The key to look up.
        - default: The value to return if the key is not present (default: None).

        Returns:
        The value associated with the key, or the default value if the key is not present.
        """
        for i, k in enumerate(self.keys):
            if k == key:
                return self.values[i]
        return default

    def items(self):
        """
        Return a zip of keys and values.

        Returns:
        A zip object containing pairs of keys and values.
        """
        return zip(self.keys, self.values)

    def Values(self):
        """
        Return a list of values.

        Returns:
        A list containing all values in the dictionary.
        """
        return self.values

    def Keys(self):
        """
        Return a list of keys.

        Returns:
        A list containing all keys in the dictionary.
        """
        return self.keys

    def __contains__(self, key):
        """
        Check if the dictionary contains a key.

        Parameters:
        - key: The key to check for existence.

        Returns:
        True if the key is present; False otherwise.
        """
        return key in self.keys

    def __iter__(self):
        """
        Return an iterator over keys.

        Returns:
        An iterator object over the keys in the dictionary.
        """
        return iter(self.keys)

    def __len__(self):
        """
        Return the number of key-value pairs in the dictionary.

        Returns:
        The number of key-value pairs in the dictionary.
        """
        return len(self.keys)

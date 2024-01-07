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
        The initial size of the hash table is set to 4999.

        Attributes:
        - size (int): The initial size of the list of buckets.
        - buckets (list): A list of buckets, where each bucket is a list of key-value pairs.
        """
        self.size = 1000  # Choose an initial size for the list of buckets
        self.buckets = [[] for _ in range(self.size)]
        self.length = 0

    def set(self, key, value):
        """
        Set a key-value pair in the dictionary.

        Parameters:
        - key: The key to be set.
        - value: The value to be associated with the key.
        """
        storage_idx = hash(key) % self.size
        for ele in self.buckets[storage_idx]:
            if key == ele[0]:  # already exist, update it
                ele[1] = value
                break
        else:
            self.buckets[storage_idx].append([key, value])
            self.length += 1

    def get(self, key, default=None):
        """
        Get the value for a given key or a default value if the key is not present.

        Parameters:
        - key: The key to look up.
        - default: The value to return if the key is not present (default: None).

        Returns:
        The value associated with the key, or the default value if the key is not present.
        """
        storage_idx = hash(key) % self.size
        for ele in self.buckets[storage_idx]:
            if ele[0] == key:
                return ele[1]

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

    def __iterate_kv(self):
        """
        return an iterator
        :return: generator
        """
        for sub_lst in self.storage:
            if not sub_lst:
                continue
            for item in sub_lst:
                yield item

    def __iter__(self):
        """
        return an iterator
        :return: generator
        """
        for key_var in self.__iterate_kv():
            yield key_var[0]

    def Keys_iter(self):
        """
        get all keys as list
        :return: list
        """
        return self.__iter__()

    def Values_iter(self):
        """
        get all values as list
        :return: list
        """
        for key_var in self.__iterate_kv():
            yield key_var[1]

    def items_iter(self):
        """
        get all k:v as list
        :return: list
        """
        return self.__iterate_kv()

    def __contains__(self, key):
        """
        Check if the dictionary contains a key.

        Parameters:
        - key: The key to check for existence.

        Returns:
        True if the key is present; False otherwise.
        """
        storage_idx = hash(key) % self.size
        for item in self.buckets[storage_idx]:
            if item[0] == key:
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
        return self.length

    def __repr__(self):
        """
        Return the key-value pairs in the dictionary as string.

        Returns:
        The key-value pairs in the dictionary as string.
        """
        return str(self.items())
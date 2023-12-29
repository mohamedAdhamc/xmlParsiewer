class CustomSet:
    """
    Custom set implementation using hashing.

    Attributes:
    - size (int): The initial size of the list of buckets.
    - buckets (list): A list of buckets, where each bucket is a list of elements.
    """

    def __init__(self, elements=None):
        """
        Initialize an empty CustomDict.

        The CustomDict is implemented as a hash table with a list of buckets.
        The initial size of the hash table is set to 4999.

        Attributes:
        - size (int): The initial size of the list of buckets.
        - buckets (list): A list of buckets, where each bucket is a list of key-value pairs.
        """
        self.size = 4999  # Choose an initial size for the list of buckets
        self.buckets = [[] for _ in range(self.size)]

        if elements:
            for elem in elements:
                self.add(elem)

    def hash_function(self, key):
        """
        Custom hash function for both strings and numbers.

        Parameters:
        - key: The key (either string or number or bytes) to be hashed.

        Returns:
        An integer hash value computed based on the input key.
        """
        if isinstance(key, str):
            # Handle string keys
            hash_value = 0
            for char in key:
                hash_value = (hash_value * 31 + ord(char)) % self.size

        elif isinstance(key, bytes):
            # Handle bytes keys
            hash_value = 0
            for char in key:
                hash_value = (hash_value * 31 + int(char)) % self.size

        else:
            # Handle numeric keys
            hash_value = key % self.size

        return hash_value


    def add(self, element):
        """
        Add an element to the set.

        Parameters:
        - element: Element to be added.
        """
        hash_value = self.hash_function(element)
        bucket = self.buckets[hash_value]

        if element not in bucket:
            bucket.append(element)

    def update(self, other_set):
        """
        Update the set with elements from another set.

        Parameters:
        - other_set: Another set to update from.
        """
        for elem in other_set:
            self.add(elem)

    def remove(self, element):
        """
        Remove an element from the set.

        Parameters:
        - element: Element to be removed.
        """
        hash_value = self.hash_function(element)
        bucket = self.buckets[hash_value]

        if element in bucket:
            bucket.remove(element)

    def __contains__(self, element):
        """
        Check if the set contains an element.

        Parameters:
        - element: Element to check for existence.

        Returns:
        True if the element is present; False otherwise.
        """
        hash_value = self.hash_function(element)
        bucket = self.buckets[hash_value]

        return element in bucket

    def __iter__(self):
        """
        Return an iterator over elements.

        Returns:
        An iterator object over the elements in the set.
        """
        return (element for bucket in self.buckets for element in bucket)

    def __len__(self):
        """
        Return the number of elements in the set.

        Returns:
        The number of elements in the set.
        """
        return sum(len(bucket) for bucket in self.buckets)

    def intersection(self, other_set):
        """
        Return the intersection of two sets.

        Parameters:
        - other_set: Another set to find the intersection with.

        Returns:
        A new set containing elements common to both sets.
        """
        common_elements = set()

        for elem in other_set:
            if elem in self:
                common_elements.add(elem)

        return CustomSet(common_elements)

    def difference(self, other_set):
        """
        Return the difference between two sets.

        Parameters:
        - other_set: Another set to find the difference with.

        Returns:
        A new set containing elements unique to the current set.
        """
        unique_elements = set()

        for elem in self:
            if elem not in other_set:
                unique_elements.add(elem)

        return CustomSet(unique_elements)

    def __repr__(self):
        """
        Return the elements in the set as string.

        Returns:
        The elements in the set as string.
        """
        return str(list(self))
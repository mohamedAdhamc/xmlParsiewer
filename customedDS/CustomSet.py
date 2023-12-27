class CustomSet:
    """
    Custom set implementation.

    Attributes:
    - elements (list): A list to store elements in the set.
    """

    def __init__(self, elements=None):
        """
        Initialize a new set.

        Parameters:
        - elements (list or None): Initial elements for the set.
        """
        if elements:
            self.elements = elements
        else:
            self.elements = []

    def add(self, element):
        """
        Add an element to the set.

        Parameters:
        - element: Element to be added.
        """
        if element not in self.elements:
            self.elements.append(element)

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
        if element in self.elements:
            self.elements.remove(element)

    def __contains__(self, element):
        """
        Check if the set contains an element.

        Parameters:
        - element: Element to check for existence.

        Returns:
        True if the element is present; False otherwise.
        """
        return element in self.elements

    def __iter__(self):
        """
        Return an iterator over elements.

        Returns:
        An iterator object over the elements in the set.
        """
        return iter(self.elements)

    def __len__(self):
        """
        Return the number of elements in the set.

        Returns:
        The number of elements in the set.
        """
        return len(self.elements)

    def intersection(self, other_set):
        """
        Return the intersection of two sets.

        Parameters:
        - other_set: Another set to find the intersection with.

        Returns:
        A new set containing elements common to both sets.
        """
        return CustomSet([elem for elem in self.elements if elem in other_set])

    def difference(self, other_set):
        """
        Return the difference between two sets.

        Parameters:
        - other_set: Another set to find the difference with.

        Returns:
        A new set containing elements unique to the current set.
        """
        return CustomSet([elem for elem in self.elements if elem not in other_set])

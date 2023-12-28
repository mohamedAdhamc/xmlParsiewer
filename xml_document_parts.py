class Attribute:
    """
    class for objects that represent some key-value pair
    for an Element's attributes.

    Attributes:
    ----------
    - key (str):
        Attribute key.
    - value (str):
        Attribute value.
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value





class Element:
    """
    class for objects that represent some element (tag) in an
    XML file.

    Attributes:
    ----------
    - name (str):
        Element/tag name.
    - children (list of Element obj):
        Element's children.
    - parent (Element):
        Element's parent.
    - attributes (list of Attribute obj):
        Element's attributes.
    - content (str):
        Element's text content.
    """

    def __init__(self, name, parent, attributes):
        self.name = name
        self.children = []
        self.parent = parent
        self.attributes = attributes
        self.content = ""

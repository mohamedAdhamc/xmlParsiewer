import re
from formatting import minify
from xml_document_parts import Element, Attribute

class XML_Document:
    """
    Builds a tree from syntactically correct XML text.

    Attributes:
    ----------
    - text (str):
        XML string.
    - tokens (list of str):
        Each token represents the string between two tags (< >) or the
        string between (> <), used for parsing.
    - root (Element):
        Root of the document, used to access any and all children.
    - stack (list of Element):
        Stack used for parsing the XML text.

    Methods:
    --------
    - parse():
        Internal method for parsing the xml text and building the tree.
    - get_attr(text):
        Gets a tag's attributes from the given token.
    - check_siblings_and_add_child(element):
        Checks if current child has duplicates (siblings) to append
        to respective list in the parent's children. Used for JSON construction
        later.
    """

    def __init__(self, text):
        """
        Parameters:
        ----------

        - text (str):
            syntactically correct XML string.
        """

        self.text = text
        self.tokens = re.findall(r'<[^>]+>|(?<=>)[^<]+(?=<)', minify(text))

        self.root = Element("root", None, [])
        self.root.parent = self.root

        self.stack = []
        self.parse()

    def parse(self):
        """
        Parses the XML file to construct tree. This updates
        self.stack and self.root in-place.
        """

        self.stack.append(self.root)
        for token in self.tokens:
            # Opening tag
            if (token[0] == '<' and (token[1] != '/' or token[-2] == '/')):
                name, list_of_attributes = self.get_attr(token)
                new_element = Element(name, self.stack[-1], list_of_attributes)
                self.check_siblings_and_add_child(new_element)

                # Not a self-closing tag
                if (token[-2] != "/"):
                    self.stack.append(new_element)

            # Closing tag
            elif (token[0] == '<' and token[1] == '/'):
                self.stack[-1].content = self.stack[-1].content.rstrip()
                self.stack.pop()

            # Text content between tags
            else:
                self.stack[-1].content += token + ' '

    def get_attr(self, text):
        """
        Gets attributes in a given tag text.

        Parameters:
        ----------
        - text (str):
            Tag text, i.e. text between < >

        Returns:
        --------
        str:
            Tag name extracted from tag text.
        list of Attribute:
            List of Attribute objects, if there are none, returns empty list.
        """
        if (text[-2] == '/'):
            text = text[1:-2]
        else:
            text = text[1:-1]

        attributes = []
        returned_list = []

        first_space_index = len(text)
        for i in range(len(text)):
            if (text[i] == ' '):
                first_space_index = i
                break

        # insert tag name as first element
        attributes.append(text[:first_space_index])
        text = text[first_space_index:]

        # matches sometext="sometext"
        attributes.extend(re.findall(r'\S+="[\s\S]*?"', text))

        for attribute in attributes[1:]:
            key, _, value = attribute.partition('=')
            returned_list.append(Attribute(key, value[1:-1]))
        return attributes[0], returned_list

    def check_siblings_and_add_child(self, element):
        """
        Checks for given Element object if its parent has other children
        of the same name, if so, adds it to its respective list, otherwise
        creates a new list for the element. This is helpful for JSON parsing later.

        Parameters:
        ----------
        - element (Element):
            An Element object to perform function on.
        """
        has_siblings_flag = False

        for child in self.stack[-1].children:
            if (child[0].name == element.name):
                child.append(element)
                has_siblings_flag = True
                break

        if (not has_siblings_flag):
            self.stack[-1].children.append([element])

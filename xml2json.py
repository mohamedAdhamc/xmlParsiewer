import re
from formatting import minify
from xml_document import XML_Document

class XML2JSON:
    """
    Constructs a JSON file from a syntactically correct XML text.

    Attributes:
    ----------
    - xml_tree (XML_Document):
        An XML_Document object constructed from the file text.
    - tab_length (int):
        Desired tab length in spaces for the output JSON file.
    - json_list (list of str):
        List of the constituent parts for the final JSON string. Only needed
        for an internal function.
    - json_text (str):
        JSON representation of the xml file.

    Methods:
    --------
    - add_json_children(node, single, tabs):
        Internal method for parsing the xml text and constructing the json_list.
    """

    def __init__(self, text, tab_length):
        """
        Parameters:
        ----------
        - text (str):
            syntactically correct XML string.
        - tab_length (int):
            Desired tab length in spaces for the output JSON file.
        """

        self.xml_tree = XML_Document(text)
        self.tab_length = tab_length

        self.json_list = []
        self.add_json_children(self.xml_tree.root)

        self.json_text = ''.join(self.json_list)
        # Remove extra commas after every last nested child
        self.json_text = re.sub(r',(?=\s+})|,(?=\s+])|,(?=\s+$)', r'', self.json_text)

    def add_json_children(self, node, single=True, tabs=""):
        """
        Internal recursive function that constructs the JSON list, to later
        construct the JSON string. This updates self.json_list in-place.

        Parameters:
        ----------
        - node (Element obj):
            Current node to perform operation on. Function is recursive and will
            then be called on all children of said element.
        - single (boolean, optional):
            Whether the current node has siblings or not. (Default is True)
        - tabs (str, optional):
            The initial tab level for the current Element. Variable is
            automatically updated after each function call. (Default is "")

        """

        extra_tabs = tabs + ' ' * self.tab_length
        if not single:
            self.json_list.append(tabs)

        if (len(node.attributes) == 0 and len(node.children) == 0):
            self.json_list.append(f'"{node.content}",\n')
        else:
            self.json_list += '{\n'
            if (len(node.content) != 0):
                self.json_list.append(f'{extra_tabs}"_text": "{node.content}",\n')

            if(len(node.attributes) != 0):
                for attribute in node.attributes:
                    self.json_list.append(f'{extra_tabs}"#{attribute.key}": "{attribute.value}",\n')

            if (len(node.children) != 0):
                for list_of_children in node.children:
                    # check if child has no siblings
                    if (len(list_of_children) == 1):
                        self.json_list.append(f'{extra_tabs}"{list_of_children[0].name}": ')
                        self.add_json_children(list_of_children[0],
                                               single=1,
                                               tabs=tabs + ' ' * self.tab_length)
                    else:
                        self.json_list.append(f'{extra_tabs}"{list_of_children[0].name}": [\n')
                        for child in list_of_children:
                            self.add_json_children(child,
                                                   single=0,
                                                   tabs=extra_tabs + ' ' * self.tab_length)
                        self.json_list.append(f'{extra_tabs}],\n')

            self.json_list.append(tabs + "},\n")





def xml2json(text, tab_length=4):
    """
    Wrapper function that constructs an XML2JSON object and
    returns the JSON representation of an XML file.

    Parameters:
    ----------
    - text (str):
        Syntactically correct string representation of the XML file.
    - tab_length (int, optional):
        Desired tab width for the output JSON string. (Default is 4)
    """

    return XML2JSON(text, tab_length).json_text

import re

def minify(text):
    """
    Minifies a syntactically correct XML file, i.e. it removes
    extra spaces and new lines.

    Parameters:
    ----------
    - text (str):
        XML file string.

    Returns:
    --------
    str:
        Minifed text.
    """

    # remove all comments
    text = re.sub(r'<\s*!\s*-\s*-\s*[\S\s]+?-\s*-\s*>', r'', text)
    # remove all extra newlines or tabs after > or before <
    # avoid changing newlines in tag content while doing so
    # also remove all spaces before start of file and after end
    text = re.sub(r'\A\s+|(?<=>)\s+(?=<)|\s+\Z', r'', text)
    # remove all extra spaces after opening tag and before closing tag
    text = re.sub(r'\s+>', r'>', text)
    text = re.sub(r'\s+/>', r'/>', text)
    text = re.sub(r'<\s+', r'<', text)
    text = re.sub(r'</\s+', r'</', text)
    # remove all extra spaces after tag name and before first attribute if any
    text = re.sub(r'(<\S+)(\s+)', r'\g<1> ', text)
    # remove all spaces surrounding = when defining an attribute
    # and avoid messing with tag contents if similar structures exist
    text = re.sub(r'(\s*=\s*)(?=[^<]+>)', r'=', text)
    # remove all extra spaces between different attributes
    text = re.sub(r'\"\s+(?=[^<]+>)', r'" ', text)
    text = re.sub(r"\'\s+(?=[^<]+>)", r"' ", text)

    # remove any non-significant spaces and newlines after
    # closing tag and before text content, or before opening
    # tag and after text content.
    text = re.sub(r'\s+<', r'<', text)
    text = re.sub(r'>\s+', r'>', text)

    return text

def prettify(text, tab_length=4):
    """
    Prettifies/beautifies a syntactically correct XML file, i.e. it adds
    newlines and tabs where appropriate.

    Parameters:
    ----------
    - text (str):
        XML file string.
    - tab_length (int, optional):
        Desired tab length (in spaces) for indentation. (Default is 4)

    Returns:
    --------
    str:
        Prettified text.
    """

    text = minify(text)
    # Get any text between tags, or any text content, and put in list
    tokens = re.findall(r'<[^>]+>|(?<=>)[^<]+(?=<)', text)

    text = []
    tabs = ""

    for token in tokens:
        if (token[0] == '<' and token[1] != '/'):
            text.append('\n' + tabs + token)
            if (token[-2] != '/'):
                tabs += ' ' * tab_length

        elif (token[0] == '<' and token[1] == '/'):
            tabs = tabs[:-tab_length]
            text.append('\n' + tabs + token)

        else:
            text.append('\n' + tabs + token)

    text = ''.join(text)
    # remove extra \n at beginning of "text"
    text = text[1:]

    return text

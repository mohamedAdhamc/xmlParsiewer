import re
from formatting import minify, prettify

def correct_xml(xml):
    xml = minify(xml)
    stack = []

    tokens = re.findall(r'<[^>]+>|(?<=>)[^<]+(?=<)', xml)
    # flag for checking whether first tag is matched or not (root)
    # used in looping over the tokens as well.
    mismatched_first_tag = 1

    if (tokens[0][1:-1] != tokens[-1][2:-1]):
        mismatched_first_tag = -len(tokens)

    xml = [tokens[0]]

    for token in tokens[1:-mismatched_first_tag]:
        if (token[0] == '<' and token[1] != '/'):
            xml.append(token)
            stack.append(token[1:-1])

        elif (token[0] == '<' and token[1] == '/'):
            entered_loop = False
            while(len(stack) > 0 and stack[-1] != token[2:-1]):
                entered_loop = True
                xml.append('</' + stack[-1] + '>')
                if (len(stack) == 1):
                    xml.append('<' + token[2:-1] + '>')
                    xml.append(token)
                stack.pop()

            if (len(stack) > 0 and stack[-1] == token[2:-1]):
                xml.append('</' + stack[-1] + '>')
                stack.pop()

            elif (not entered_loop):
                xml.append('<' + token[2:-1] + '>')
                xml.append(token)

        else:
            xml.append(token)

    while (len(stack) > 0):
        xml.append('</' + stack[-1] + '>')
        stack.pop()

    if (mismatched_first_tag == 1):
        xml.append('</' + tokens[0][1:-1] + '>')

    xml = ''.join(xml)
    xml = prettify(xml)
    return xml

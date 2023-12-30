from minify import minify
from xmlParsiewer.customedDS.CustomDict import CustomDict

with open("/home/mahmoud/Work/Uni/DSA/Project/xmlParsiewer/test_files/generic_syntactically_correct3.xml", "r") as file:
    text = file.read()

mini = minify(text)

def encode(text):
    dictionary = CustomDict()
    for i in range(256):
        dictionary.set(chr(i), i)

    w = ""
    result = []
    for c in text:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary.get(w))
            dictionary.set(wc, len(dictionary))
            w = c
    if w:
        result.append(dictionary.get(w))

    # dictionary = {}
    # for i in range(256):
    #     dictionary[chr(i)] = i

    # w = ""
    # result = []
    # for c in text:
    #     wc = w + c
    #     if wc in dictionary:
    #         w = wc
    #     else:
    #         result.append(dictionary[w])
    #         dictionary[wc] = len(dictionary)
    #         w = c
    # if w:
    #     result.append(dictionary[w])
    
    return result

def decode(codes):
    dictionary = CustomDict()
    for i in range(256):
        dictionary.set(i, chr(i))

    w = chr(codes[0])
    result = [w]
    for k in codes[1:]:
        if k in dictionary:
            entry = dictionary.get(k)
        elif k == len(dictionary):
            entry = w + w[0]
        else:
            raise ValueError("Bad compressed k: %s" % k)
        result.append(entry)
        dictionary.set(len(dictionary), w + entry[0])
        w = entry
    return "".join(result)


    # dictionary = {}
    # for i in range(256):
    #     dictionary[i] = chr(i)

    # w = chr(codes[0])
    # result = [w]
    # for k in codes[1:]:
    #     if k in dictionary:
    #         entry = dictionary[k]
    #     elif k == len(dictionary):
    #         entry = w + w[0]
    #     else:
    #         raise ValueError("Bad compressed k: %s" % k)
    #     result.append(entry)
    #     dictionary[len(dictionary)] = w + entry[0]
    #     w = entry
    # return "".join(result)

def save_codes(codes):
    max_len = 0
    for c in codes:
        if len(str(c)) > max_len:
            max_len = len(str(c))
    codes_str = ["0"*(max_len - len(str(c)))+str(c) for c in codes]
    
    with open("output.txt", "w") as txt_file:
        txt_file.write(str(max_len) + "," + "".join(codes_str))

def load_codes():
    with open("output.txt", "r") as txt_file:
        text = txt_file.read()
    max_len = int(text.split(",")[0])
    text = text.split(",")[1]
    codes = [int(text[i:i+max_len]) for i in range(0, len(text), max_len)]
    return codes


encoded = encode(mini)
print("encoded")
save_codes(encoded)
decoded = decode(load_codes())

print("Original:", len(mini))
print("Encoded:", len(encoded))
print("Decoded:", len(decoded))
print(mini == decoded)
from customedDS.CustomDict import CustomDict

def reduce(function, sequence, initial):
    it = iter(sequence)
    value = initial
    for element in it:
        value = function(value, element)

    return value

class BPE():
    """
    Class for byte pair encoding compression algorithm
    -   BPE works by scanning the bytes of the incoming text,
        and replacing the most common pair with a single, unused byte.

    -   This process is repeated until we either run out of available bytes,
        or there are no more frequent pairs (Max frequency = 1)

    -   Since a single byte can represent 256 characters, we build a list
        of reserved and available characters
    
    -   The resulting map is appended to the output file, to enable a 
        lossless file decompression
    
    Methods:
    --------
    - compress(text: str):
        Method for compressing an input string and saving the output to a file
        Returns: void

    - decompress(filename: str):
        Method for loading a file and decompressing it back to text
        Returns: str
    """

    def __init__(self):
        self.__replacement_dict = CustomDict()
        self.__original_file_data: bytes = None
        self.__unique_file_data = []
        self.__available_characters = []
        self.__frequencies = [0] * 256 * 256
        self.__all_bytes = [i.to_bytes() for i in range(256)]

    def __get_replacement(self) -> bytes:
        """ Get a replacement byte from available characters"""

        if len(self.__available_characters) == 0:
            raise Exception("Maximum available characters used, compression limit reached")

        replacement = self.__available_characters.pop(0)
        return replacement.to_bytes()

    def __find_original(self, b: bytes, table):
        """Check if the byte is in the lookup table and get the original byte before decompression"""

        if b in table:
            b1, b2 = table.get(b)
            return self.__find_original(b1.to_bytes(), table) + self.__find_original(b2.to_bytes(), table)
        else:
            return b

    def __rebuild_replacement_dict(self, data: bytes):
        """Reconstruct the lookup table from the data in the compressed file"""

        byte_len = data[0]
        table_chunk = data[(-3 * byte_len):]

        table = CustomDict()
        for i in range(0, 3 * byte_len, 3):
            table.set(table_chunk[i].to_bytes(), table_chunk[i + 1].to_bytes() + table_chunk[i + 2].to_bytes())
        return table

    def compress(self, text: str, file_path, iterations = None):
        """Convert text to binary to compress it"""
        self.__original_file_data = bytearray(text, "utf-8")
        self.__unique_file_data = reduce(lambda l, x: l.append(x) or l if x not in l else l, self.__original_file_data, [])
        self.__available_characters = [c for c in range(256) if c not in self.__unique_file_data]

        # Placeholder for the most frequent object in the last loop
        highest_frequency = 0
        data_len = len(self.__original_file_data)
        compressed_data = self.__original_file_data
        _iter = 0
        iterate = True
        if iterations == "":
            iterations = None
        elif iterations != "" and iterations != None:
            iterations = int(iterations)

        # Break if file cannot be compressed further
        while (highest_frequency != 1 and iterate):
            # Loop through the data and count frequencies
            self.__frequencies = [0] * 256 * 256
            for i in range(data_len - 1):
                first_iter = compressed_data[i]
                second_iter = compressed_data[i + 1]
                index = first_iter * 256 + second_iter
                self.__frequencies[index] += 1

            # Try to find a replacement byte from the available characters
            try:
                replacement = self.__get_replacement()
            except Exception as e:
                print(e)
                break

            max_val = 0
            index_max = 0 # Index of most frequent pair
            for i in range(len(self.__frequencies)):
                if self.__frequencies[i] > max_val:
                    max_val = self.__frequencies[i]
                    index_max = i
            highest_frequency = self.__frequencies[index_max] # Count of pair in data

            first = (index_max // 256)
            second = (index_max % 256)
            highest_occuring_pair = self.__all_bytes[first] + self.__all_bytes[second]
            # Add the chosen byte to the lookup table
            self.__replacement_dict.set(replacement, highest_occuring_pair)

            # Replace two bytes with a single byte
            compressed_data = compressed_data.replace(highest_occuring_pair, replacement)
            data_len = len(compressed_data)
            if iterations != None:
                _iter += 1
                iterate = _iter < iterations

        replacement_length = (len(self.__replacement_dict)).to_bytes()

        with open(file=file_path+".xip", mode="wb") as compressed_file:
            # Write length of the bytes used for compression
            compressed_file.write(replacement_length)
            compressed_file.write(compressed_data)

            # Add the lookup table as overhead at the end of the file
            for key, value in self.__replacement_dict.items_iter():
                compressed_file.write(key + value)
            print("Compressed!")

    def decompress(self, filename: str):
        """ Decompress the file back to its original format """
        
        with open(file=filename, mode="rb") as file_binary:
            compressed_file_data = file_binary.read()

        decompressed_data = []

        # Use the redundant information to construct dict before decompression
        reconstruction_dict = self.__rebuild_replacement_dict(compressed_file_data)
        data_len = len(compressed_file_data) - len(reconstruction_dict) * 3

        # Iterate through every file in the compressed file and find every byte in the lookup table recursively
        for i in range(1, data_len):
            decompressed_data.append(self.__find_original(compressed_file_data[i].to_bytes(), reconstruction_dict))

        print("Decompressed!")
        return b"".join(decompressed_data).decode("utf8")
# from functools import reduce
from customedDS.CustomDict import CustomDict
import cProfile
import pstats

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
        self.__lookup_table = CustomDict()
        self.__raw_file_data: bytes = None
        self.__unique_file_data = []
        self.__available_characters = []
        self.__frequencies = [0] * 256 * 256
        self.__all_bytes = [i.to_bytes() for i in range(256)]

    def __get_replacement(self) -> bytes:
        """ Get a replacement byte from available characters"""

        if len(self.__available_characters) == 0:
            raise Exception("Maximum characters reached in lookup table, maximum compression reached")

        replacement = self.__available_characters.pop(0)
        return replacement.to_bytes(1, byteorder="big")

    def __get_original(self, b: bytes, reconstruction_keys, reconstruction_values):
        """Check if the byte is in the lookup table and get the original byte before decompression"""

        if b in reconstruction_keys:
            b1 = self.__get_original(reconstruction_values[reconstruction_keys.index(b)][0].to_bytes(), reconstruction_keys, reconstruction_values)
            b2 = self.__get_original(reconstruction_values[reconstruction_keys.index(b)][1].to_bytes(), reconstruction_keys, reconstruction_values)
            return b1 + b2
        return b

    def __reconstruct_dict(self, data: bytes):
        """Reconstruct the lookup table from the data in the compressed file"""

        byte_len = data[0]
        table_chunk = data[(-3 * byte_len):]

        key_bytes = []
        value_bytes = []
        for i in range(0, 3 * byte_len, 3):
            key_bytes.append(table_chunk[i].to_bytes())
            value_bytes.append(table_chunk[i + 1].to_bytes() + table_chunk[i + 2].to_bytes())
        return key_bytes, value_bytes

    def compress(self, text: str, iterations: int):
        """Convert text to binary to compress it"""
        self.__raw_file_data = bytearray(text, "utf-8")
        self.__unique_file_data = reduce(lambda l, x: l.append(x) or l if x not in l else l, self.__raw_file_data, [])
        self.__available_characters = [c for c in range(256) if c not in self.__unique_file_data]

        # Placeholder for the most frequent object in the last loop
        last_pair_frequency = 0
        data_len = len(self.__raw_file_data)
        compressed_data = self.__raw_file_data
        _iter = 0

        # Break if file cannot be compressed further
        while (last_pair_frequency != 1 or _iter < iterations):
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
            last_pair_frequency = self.__frequencies[index_max] # Count of pair in data

            first = (index_max // 256)
            second = (index_max % 256)
            highest_occuring_pair = self.__all_bytes[first] + self.__all_bytes[second]
            # Add the chosen byte to the lookup table
            self.__lookup_table.set(replacement, highest_occuring_pair)

            # Replace two bytes with a single byte
            compressed_data = compressed_data.replace(highest_occuring_pair, replacement)
            data_len = len(compressed_data)
            _iter += 1

        replacement_length = (len(self.__lookup_table)).to_bytes()

        with open(file="output.xip", mode="wb") as compressed_file:
            # Write length of the bytes used for compression
            compressed_file.write(replacement_length)
            compressed_file.write(compressed_data)

            # Add the lookup table as overhead at the end of the file
            for key, value in self.__lookup_table.items():
                compressed_file.write(key + value)
    def decompress(self, filename: str):
        """ Decompress the file back to its original format """
        
        with open(file=filename, mode="rb") as file_binary:
            compressed_file_data = file_binary.read()

        decompressed_data = b""

        # Use the redundant information to construct dict before decompression
        reconstruction_keys, reconstruction_values = self.__reconstruct_dict(compressed_file_data)
        data_len = len(compressed_file_data) - len(reconstruction_keys) * 3

        # Iterate through every file in the compressed file and find every byte in the lookup table recursively
        for i in range(1, data_len):
            decompressed_data += self.__get_original(compressed_file_data[i].to_bytes(), reconstruction_keys, reconstruction_values)

        with open(file=filename.replace(".xip", "_decompressed.xml"), mode="wb") as decompressed_file:
            decompressed_file.write(decompressed_data)

xip = BPE()

with open(file="/home/mahmoud/Work/Uni/DSA/Project/xmlParsiewer/test_files/generic_syntactically_correct2.xml", mode="r") as file:
    text = file.read()
xip.compress(text, 10)
print("compressed")
xip.decompress("output.xip")

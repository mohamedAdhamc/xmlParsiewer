from customedDS.CustomDict import CustomDict
from customedDS.CustomSet import CustomSet

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
        self.__unique_file_data: bytes = CustomSet()
        self.__reserved_characters = []
        self.__available_characters = []

    def __get_replacement(self) -> bytes:
        """ Get a replacement byte from available characters"""

        if len(self.__available_characters) == 0:
            raise Exception("Maximum characters reached in lookup table, maximum compression reached")

        replacement = self.__available_characters.pop(0)
        return replacement.to_bytes(1, byteorder="big")

    def __get_original(self, b: bytes, table):
        """Check if the byte is in the lookup table and get the original byte before decompression"""

        if (b in table.Keys()):
            b1 = self.__get_original(table.get(b)[0].to_bytes(), table)
            b2 = self.__get_original(table.get(b)[1].to_bytes(), table)
            return b1 + b2
        return b

    def __max_pair(self, data):
        """Find the most frequent pair in the input dictionary"""

        max_freq = 0
        for key, freq in data.items():
            if (freq >= max_freq):
                max_freq = freq
                max_pair = key
        return max_pair, max_freq

    def __reconstruct_dict(self, data: bytes):
        """Reconstruct the lookup table from the data in the compressed file"""

        byte_len = data[0]
        table_chunk = data[(-3 * byte_len):]

        table = CustomDict()
        for i in range(0, 3 * byte_len, 3):
            table.set(table_chunk[i].to_bytes(), table_chunk[i + 1].to_bytes() + table_chunk[i + 2].to_bytes())
        return table

    def compress(self, text: str):
        """Convert text to binary to compress it"""

        self.__raw_file_data = bytearray(text, "utf-8")
        self.__unique_file_data.update(self.__raw_file_data)
        for b in self.__unique_file_data:
            self.__reserved_characters.append(b)
        self.__available_characters = [c for c in range(256) if c not in self.__reserved_characters]

        # Placeholder for the most frequent object in the last loop
        last_pair_frequency = 0
        data_len = len(self.__raw_file_data)
        compressed_data = self.__raw_file_data

        # Break if file cannot be compressed further
        while (last_pair_frequency != 1):
            # pairs = {}
            pairs = CustomDict()
            # Loop through the data and make a pair-freqency dict
            for i in range(data_len - 1):
                first_iter = compressed_data[i]
                second_iter = compressed_data[i + 1]
                pair = first_iter.to_bytes() + second_iter.to_bytes()
                if (pair in pairs):
                    # pairs[pair] += 1
                    pairs.set(pair, pairs.get(pair) + 1)
                else:
                    # pairs[pair] = 1
                    pairs.set(pair, 1)

            # Try to find a replacement byte from the available characters
            try:
                replacement = self.__get_replacement()
            except Exception as e:
                print(e)
                break

            highest_occuring_pair, last_pair_frequency = self.__max_pair(pairs)

            # Add the chosen byte to the lookup table
            self.__lookup_table.set(replacement, highest_occuring_pair)

            # Replace two bytes with a single byte
            compressed_data = compressed_data.replace(highest_occuring_pair, replacement)
            data_len = len(compressed_data)

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
        reconstruction_dict = self.__reconstruct_dict(compressed_file_data)
        data_len = len(compressed_file_data) - len(reconstruction_dict) * 3

        # Iterate through every file in the compressed file and find every byte in the lookup table recursively
        for i in range(1, data_len):
            decompressed_data += self.__get_original(compressed_file_data[i].to_bytes(), reconstruction_dict)

        with open(file=filename.replace(".xip", "_decompressed.xml"), mode="wb") as decompressed_file:
            decompressed_file.write(decompressed_data)

xip = BPE()

with open(file="/home/mahmoud/Work/Uni/DSA/Project/sample.xml", mode="r") as file:
    text = file.read()
xip.compress(text)
xip.decompress("output.xip")
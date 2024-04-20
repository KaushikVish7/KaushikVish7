import os
import heapq

class BinaryTreeNode:
    def __init__(self, value, freq):
        self.value = value
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other): #used to compare two binary tree nodes to push smaller node into the heap
        return self.freq < other.freq

    def __eq__(self, other):
        return self.freq == other.freq

class HuffmanCoding:
    def __init__(self,path):
        self.path=path
        self.__heap = []
        self.__codes = {} #maps characters to corresponding bits
        self.__reverseCodes = {} #maps bits to corresponding characters
        
    def __make_frequency_dict(self, text):
        freq_dict = {}
        for char in text:
            if char in freq_dict:
                freq_dict[char] += 1
            else:
                freq_dict[char] = 1

        return freq_dict

    def __buildHeap(self, freq_dict):
        for key in freq_dict:
            frequency = freq_dict[key]
            binary_tree_node = BinaryTreeNode(key, frequency)
            heapq.heappush(self.__heap, binary_tree_node)

    def __buildTree(self):
        while len(self.__heap) > 1:
            binary_tree_node_1 = heapq.heappop(self.__heap) #most min element of the heap
            binary_tree_node_2 = heapq.heappop(self.__heap) #2nd most min element of the heap
            freq_sum = binary_tree_node_1.freq + binary_tree_node_2.freq
            newNode = BinaryTreeNode(None, freq_sum)
            newNode.left = binary_tree_node_1 #left child is always smaller of the two popped nodes
            newNode.right = binary_tree_node_2 #right child is always greater of the two popped nodes
            heapq.heappush(self.__heap, newNode)

        return

    def __buildCodesHelper(self, root, curr_bits):
        if root is None:
            return
        
        if root.value is not None: #checking for a leaf node (all leaf nodes will have values)
            self.__codes[root.value] = curr_bits #mapping a to 101 (say)
            self.__reverseCodes[curr_bits] = root.value #mapping 101 back to a
            return

        self.__buildCodesHelper(root.left, curr_bits + "0") #assign 0 for left edge of every node
        self.__buildCodesHelper(root.right, curr_bits + "1") #assign 1 for right edge of every node

    def __buildCodes(self):
        root = heapq.heappop(self.__heap)
        self.__buildCodesHelper(root, "")

    def __getEncodedText(self, text):
        encoded_text = ""

        for char in text:
            encoded_text += self.__codes[char]

        return encoded_text

    def __getPaddedEncodedText(self, encoded_text):
        padded_amount = 8 - (len(encoded_text) % 8) #since 1 byte = 8 bits

        for i in range(padded_amount): #right padding with 0s to match 8 bits
            encoded_text += "0"

        padded_info = "{0:08b}".format(padded_amount)
        #left padding with 0s to match 8 bits i.e 101 will be converted to 00000101

        padded_encoded_text = padded_info + encoded_text

        return padded_encoded_text

    def __getBytesArray(self, padded_encoded_text):
        #split the padded encoded text into parts of 8 bits each to convert bits to bytes
        # as 8 bits = 1 byte
        array = []
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i+8]
            array.append(int(byte, 2)) #coverts the string with 0s and 1s into an integer

        return array

    def compress(self):
        #get file from path
        file_name, file_extension = os.path.splitext(self.path)
        output_path = file_name + ".bin"
        
        #read text from file
        with open(self.path, "r+") as file, open(output_path, "wb") as output:
            text = file.read()
            text = text.rstrip() #removes the trailing spaces

            #make frequency dictionary using the text
            freq_dict = self.__make_frequency_dict(text)

            #construct the heap from the frequency_dict
            self.__buildHeap(freq_dict)

            #construct the binary tree from the heap
            self.__buildTree()

            #construct the codes from binary tree
            self.__buildCodes()

            #creating the encoded text using the codes
            encoded_text = self.__getEncodedText(text)

            #pad this encoded text i.e convert bits (0s and 1s) into bytes (1 byte = 8 bits)
            padded_encoded_text = self.__getPaddedEncodedText(encoded_text)

            #create the bytes array from padded encoded text
            bytes_array = self.__getBytesArray(padded_encoded_text)
            
            #return the binary file as output
            final_bytes = bytes(bytes_array)
            output.write(final_bytes)

        print("Compression complete")

        return output_path

    def __removePadding(self, text):
        padded_info = text[:8]
        extra_padding = int(padded_info, 2)

        text = text[8:]
        text_after_padding_removal = text[:-1 * extra_padding]

        return text_after_padding_removal

    def __decodeText(self, text):
        decoded_text = ""
        current_bits = ""

        for bit in text:
            current_bits += bit

            if current_bits in self.__reverseCodes:
                character = self.__reverseCodes[current_bits]
                decoded_text += character
                current_bits = ""

        return decoded_text

    def decompress(self, input_path):
        #get file from path
        file_name, file_extension = os.path.splitext(self.path)
        output_path = file_name + "_decompressed" + ".txt"

        #decompress the file
        with open(input_path, "rb") as file, open(output_path, "w") as output:
            bit_string = ""
            byte = file.read(1)

            while byte:
                byte = ord(byte) #returns the integer constant for the byte, for eg, ord(a) is 97
                bits = bin(byte)[2:].rjust(8, "0")
                bit_string = bit_string + bits
                byte = file.read(1)

            actual_text = self.__removePadding(bit_string)
            decompressed_text = self.__decodeText(actual_text)
            output.write(decompressed_text)

        print("Decompression complete")

        return

path = "C:/Users/mvkau/OneDrive/CN_Reference_Docs/DSA/DSA_with_Python/Huffman Coding/sample.txt"
h = HuffmanCoding(path)
output_path = h.compress()
h.decompress(output_path)

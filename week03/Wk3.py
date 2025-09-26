class Node:

    def __init__(self, frequency, symbol=None):
        self.__frequency = frequency
        self.__symbol = symbol
        self.__left = None
        self.__right = None

    def set_left(self, child):
        self.__left = child

    def set_right(self, child):
        self.__right = child

    def __lt__(self, other):
        return self.__frequency < other.__frequency

    def get_frequency(self) -> int:
        return self.__frequency

    def get_symbol(self) -> chr:
        return self.__symbol
    
    def __str__(self):   
            return f"({self.__symbol}:{self.__frequency})"
     
        
    def __repr__(self):
        return self.__str__()
    
    def get_left(self): return self.__left
    def get_right(self): return self.__right

message_to_compress = "HELLO MATIJA"
ASCII_SYMBOLS: int = 256 

def filter_uppercase_and_spaces(input_string):
    return ''.join([char for char in input_string if char.isupper() or char == ' '])

def get_smallest(forest):
    smallest_index = 0
    for i in range(1, len(forest)):
        if forest[i] < forest[smallest_index]:
            smallest_index = i
    return forest.pop(smallest_index)



def count_frequencies(input_string: str) -> list[int]:
    frequencies = [0] * ASCII_SYMBOLS
    for char in input_string:
        ascii_value = ord(char)
        frequencies[ascii_value] += 1
    return frequencies


def initialize_forest(frequencies: list[int]) -> list[Node]:
    """
    Initializes a forest (list) of Node objects for each character with a non-zero frequency.
    """
    forest = []  # return item
    # Iterate over the input list
    for ascii in range(len(frequencies)):
        if frequencies[ascii] > 0:
            # Create a node for this symbol and its frequency
            new_node = Node(frequencies[ascii], chr(ascii))
            forest.append(new_node)
    return forest
    


def build_huffman_tree(frequencies: list[int]) -> Node:
    """
    Builds the Huffman tree from the list of frequencies and returns the root Node.
    """
    forest = initialize_forest(frequencies)
    # Your code here
    while len(forest) > 1:
        s1 = get_smallest(forest)
        s2 = get_smallest(forest)
        new_node = Node(s1.get_frequency()+s2.get_frequency())
        new_node.set_left(s1)
        new_node.set_right(s2)
        forest.append(new_node)
    return forest[0]


def build_encoding_table(huffman_tree_root: Node) -> list[str]:
    global codex
    """
    Builds the encoding table from the Huffman tree.
    Returns a list of 27 strings, where index 0-25 correspond to 'A'-'Z'
    and index 26 corresponds to space.
    Each string is the binary encoding for that character.
    """
    #When we start this we want to make sure that we have an empty string of 27 index for the whole
    #Alphabet including space. Then we add a cursor variable for our root. 
    #And finally we make a method called find_path where we will call it recursively. 
    #We see that when we call it well call the cursor, a path that is empty becuase we dont have it and the emtpy array
    codex = [None] * 27
    cursor = huffman_tree_root
    find_path(cursor,"", codex)
    print(codex)

            
    return codex

    
def find_path(root: Node, path, encoding_table):
    #When we we start this we first check if there is a path to go to the left
    if root.get_left() is not None:
        #If there is then we want to get left and alos add 0 to our path becuase since we left 
        #We add a zero.
        find_path(root.get_left(), path + '0', encoding_table)
        #Similer we check that if there is somehting in the right 
    if root.get_right() is not None:
        #Then we had 1 since we went right.
        find_path(root.get_right(), path + '1', encoding_table)
    #Once we finally check if there is no more it can go right or left
    if root.get_left() is None and root.get_right() is None:
        #Then wehat we want to do is if the symbol is equal fo 32. 
        #Because the assci code is 32 when their is a space
        if ord(root.get_symbol()) == 32:
            #If there is then we put it at index of 26
            encoding_table[26] = path
        else:
            #Else we want to subtract 65 becuase 65 is start with 'A' but if we subtract we can
            #do it from 0-26
            encoding_table[ord(root.get_symbol()) - 65] = path;



def encode(input_string: str, encoding_table: list[str]) -> str:
    """
    Encodes the input string using the provided encoding table. Remember
    that the encoding table has 27 entries, one for each letter A-Z and
    one for space. Space is at the last index (26).
    """
    #We want an empty string for our output 
    printOutput = ' '
    for i in input_string:
        #We check if i is a space
        if(i == " "):
            #We then want to put it at the last index
            printOutput += encoding_table[26] 
        else:
            #Then we want to get the ascci value 
            #and we want to make sure it goes to the correct
            #index
            printOutput += encoding_table[ord(i) - 65]
    return printOutput



def decode(encoded_string: str, huffman_root: Node) -> str:
    """
    Decodes the encoded string using the Huffman table as a key.
    """
    result = ""
    traverse = huffman_root
    #Traverse the incoded string
    for i in encoded_string:
        #If i is zero then we go left
        if i == "0":
            traverse = traverse.get_left()
        #If it is 1 then we go right
        elif i == "1":
            traverse = traverse.get_right()
        #We then check if there is nothhing
        if traverse.get_left() is None and traverse.get_right() is None:
            #We take the symbol and add it in result
            result += traverse.get_symbol()
            #And restart traveral
            traverse = huffman_root
    
    return result


word = "HELLO MATIJA"
frequencies = count_frequencies(message_to_compress)
print(frequencies)
forest = initialize_forest(frequencies)
print(forest)
huffman_tree = build_huffman_tree(frequencies)
print(huffman_tree.get_left().get_left().get_right())
encoding_table_print = build_encoding_table(huffman_tree)
print(encoding_table_print)
output = encode(word ,encoding_table_print)
print(output)
decode_message = decode(output, huffman_tree)
print(decode_message)
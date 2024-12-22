# ANSI escape codes and styles
underline = "\033[4m"
cyan="\033[36m"
blink="\033[5m"
bold = "\033[1m"
reset = "\033[0m"
red_bold = "\033[1;31m"
BOLD_BLUE = "\033[1;34m"
GREEN = "\033[32m"
ORANGE = '\033[38;5;214m'

from prettytable import PrettyTable

class Playfair:
    
    # Initialise: 
    #     - Input
    #         - key
    #         - plaintext
    #     - Generate Alphabets list
    #     - Create 'compl' list of all the matrix elements in order (26 elements)
    #     - Merge the alphabets i and j to a single string in the 'compl'(25 elements)
    #     - Create a 5x5 2D matrix with the 'compl' list by taking 5 at a time
    
    def __init__(self, key=None,PT=None,bogus=None):
        
        if key is None:
            self.key = str(input("Enter Key String: "))
        else:
            self.key = key
        if PT is None:
            self.PT = str(input("Enter Plain Text: ")).lower()
        else:
            self.PT = PT
        if bogus==None:
            self.bogus = str(input("Enter Bogus Character: ")).lower()
        else:
            self.bogus=bogus.lower()
            
        self.key = ''.join(dict.fromkeys(self.key))
        self.PT_split()
        alphabets=[]
        for i in range(97,123):
            alphabets.append(chr(i))
        compl=[i for i in self.key]
        for i in alphabets:
            if i not in compl:
                compl.append(i)
        for i in range(len(compl) - 1, -1, -1):
            if compl[i] == 'i':
                compl[i] = 'ij'
            elif compl[i] == 'j':
                compl.pop(i)                
        self.matrix = [compl[i:i+5] for i in range(0, 25, 5)]
        del compl,alphabets
        
    # Display the initialisation
    def show_init(self):
        mat = PrettyTable()
        for row in self.matrix:
            formatted_row = [
                f"{red_bold}{char}{reset}" if char in self.key else char for char in row]
            mat.add_row(formatted_row)
        mat.header = False
        print(mat)
        formatted_data = []
        for item in self.pair:
            formatted_cell = ''.join(
                f"{GREEN}{char}{reset}" if char == self.bogus else f"{BOLD_BLUE}{char}{reset}" for char in item
            )
            formatted_data.append(formatted_cell)
        pairtable = PrettyTable()
        pairtable.add_row(formatted_data)
        self.fomatted_pair=formatted_data
        pairtable.header = False
        print(pairtable)
        del mat,pairtable,formatted_data,formatted_cell,formatted_row
                
    
    # Split Plain text with replacing with bogus (here x) rule --> returns paired list
    def PT_split(self):
        self.pair = [self.PT[i:i+2] for i in range(0, len(self.PT), 2)]
        leng=len(self.pair)
        for i in range(0,leng-1):
            if self.pair[i][0] == self.pair[i][1]:
                self.pair[i] = self.pair[i][0] + self.bogus + self.pair[i][1]
        self.pair=''.join(self.pair)
        self.pair = [self.pair[i:i+2] for i in range(0, len(self.pair), 2)]
        if len(self.pair[-1])==1:
            self.pair[-1]+=self.bogus
        return self.pair
    
    # Transpose of a Matrix
    def transpose(self, A): 
        return [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]

    # Shift elements in the same row or column
    def shift(self, row, k):
        row_length = len(row)
        k=[*k]
        k[0] = row[(row.index(k[0]) + 1) % row_length]  # Circular shift for k[0]
        k[1] = row[(row.index(k[1]) + 1) % row_length]  # Circular shift for k[1]
        return''.join(k)
    
    # Rectangular Swap if not there in either same column or row
    def rectangular_swap(self, k):
        matrix = self.matrix
        index1 = index2 = None
        k = [*k]        
        # Find positions of the letters in the matrix
        for i, row in enumerate(matrix):
            for j, cell in enumerate(row):
                if k[0] in cell:
                    index1 = (i, j)
                if k[1] in cell:
                    index2 = (i, j)
        
        # Perform the rectangular swap
        k[0] = matrix[index1[0]][index2[1]]
        k[1] = matrix[index2[0]][index1[1]]
        return ''.join(k)

    # Playfair Encryption
    def encrypt(self):
        pair = self.pair
        matrix = self.matrix
        trans = self.transpose(matrix)
        enc=PrettyTable()
        enc.add_column("Pair", self.fomatted_pair)
        for k in range(len(pair)):
            found = False  # To check if the pair is in the same row/column

            # Check same row
            for row in matrix:
                if pair[k][0] in row and pair[k][1] in row:
                    pair[k] = self.shift(row, pair[k])
                    found = True
                    break

            # Check same column
            if not found:
                for col in trans:
                    if pair[k][0] in col and pair[k][1] in col:
                        pair[k] = self.shift(col, pair[k])
                        found = True
                        break

            # If diagonally situated, perform rectangular swap
            if not found:
                pair[k] = self.rectangular_swap(pair[k])
        self.ET=pair
        enc.add_column("Encrypted pairs",[f"{bold}{ORANGE}{ep}{reset}" for ep in pair])
        print(enc)
        return ''.join([''.join(p) for p in pair])  # Flatten pairs into a string

while True:
    try:
        instance=Playfair()
        instance.show_init()
        instance.PT_split()
        ans=instance.encrypt()
        ans= f"{blink}{bold}{cyan}{underline}{ans}{reset}"
        print("Encrypted text",ans)
        
    except (KeyboardInterrupt,ValueError):
        print("\n\nExiting...\n\n")
        break
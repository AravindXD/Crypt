from prettytable import PrettyTable

# Global Reference Point for ISCII<->Alphabets
index = ord('a')

# General Additive Cipher class
class AdditiveCipher:
    def __init__(self, key=None):
        if key is None:
            self.key = int(input("Enter key val: "))
        else:
            self.key = key

    def subs_cipher_encode(self, PT=None):
        if PT is None:
            self.PT = str(input("Enter Plain Text: ")).lower()
        else:
            self.PT = PT
        encoded_string = ""
        for i in self.PT:
            encoded_string += chr(((ord(i) - index + self.key) % 26) + index)
        return encoded_string

    def subs_cipher_decode(self, ET=None):
        if ET is None:
            self.ET = str(input("Enter Encoded Text: ")).lower()
        else:
            self.ET = ET
        decoded_string = ""
        for i in self.ET:
            decoded_string += chr(((ord(i) - index - self.key) % 26) + index)
        return decoded_string.upper()

class CaesarCipher(AdditiveCipher):
    def __init__(self):
        super().__init__(key=3)

# Interfacing in CLI
# - Integrating User Input/Output
# - PrettyTable Display
# - If cases
#     - Object creation for every if 
#     - Call function with the created object
#     - Add results to the table
# - print table
# - Termination 
# - LOOP

while True:
    # Create a PrettyTable for options
    table = PrettyTable()
    table.field_names = ["Option", "Description"]
    table.add_row(["1", "Additive Cipher Encode"])
    table.add_row(["2", "Additive Cipher Decode"])
    table.add_row(["3", "Caesar Cipher Encode"])
    table.add_row(["4", "Caesar Cipher Decode"])
    table.add_row(["5", "Exit"])

    # Print the options table
    print(table)

    try:
        choice = int(input("Enter choice: "))
        result_table = PrettyTable()
        result_table.field_names = ["Operation", "Input Text", "Key", "Result"]
        if choice == 1:
            AdC=AdditiveCipher()
            result = AdC.subs_cipher_encode()
            result_table.add_row(["Additive Cipher Encode", AdC.PT, AdC.key, result])
        elif choice == 2:
            AdC=AdditiveCipher()
            result = AdC.subs_cipher_decode()
            result_table.add_row(["Additive Cipher Decode", AdC.ET, AdC.key, result])
        elif choice == 3:
            CC=CaesarCipher()
            result = CC.subs_cipher_encode()
            result_table.add_row(["Caesar Cipher Encode", CC.PT, 3, result])
        elif choice == 4:
            CC=CaesarCipher()
            result = CC.subs_cipher_decode()
            result_table.add_row(["Caesar Cipher Decode", CC.ET, 3, result])
        else:
            break
        print(result_table)
        # ANSI code for Termination Line
        print("\033[1;92m" + "="*70 + "\033[0m")
        
    except (KeyboardInterrupt, ValueError):
        print("\nExiting...")
        break
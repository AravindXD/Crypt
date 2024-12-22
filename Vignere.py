from prettytable import PrettyTable

alphabets=[chr(i).upper() for i in range(97,123)]

class Vigenère:
    
    def __init__(self,key=None,T=None):
        if key==None:
            self.key=str(input("Enter Encryption Key: ")).lower()
        else:
            self.key=key
        if T==None:
           self.T=str(input("Enter Text: ")).lower()
        else:
            self.T=T

    @staticmethod
    def rightshift(row, j):
        return row[j:] + row[:j]

    @staticmethod
    def keywordMatrix(matrix=None):
        if matrix is None:
            matrix = [alphabets[:] for _ in range(26)]
            for i in range(26):
                matrix[i] = Vigenère.rightshift(matrix[i], i)
        tableau = PrettyTable()
        tableau.header = False
        for row in matrix:
            tableau.add_row(row)
        print(tableau)
        print("\033[1;92m" + "="*105 + "\033[0m")

    
    def addRolledLenKey(self):
        key=''
        for i in range(len(self.T)):
            key+= self.key[i%len(self.key)]
        self.key=key
        del key
        return self.key
    
    def encrypt(self):
        self.key=self.addRolledLenKey()
        E=''
        ref=ord('a')
        for P,K in zip(self.key,self.T) :
            i=(ord(P)+ord(K)-2*ref)%26
            E+=alphabets[i]
        ans = f"\033[5m\033[1m\033[32m{E}\033[0m"        
        print(ans)
        print("\033[1;92m" + "="*105 + "\033[0m")

        
    def decrypt(self):
        self.key=self.addRolledLenKey()
        E=''
        ref=ord('a')
        for P,K in zip(self.key,self.T) :
            i=(ord(K)-ord(P)+26)%26
            E+=alphabets[i]
        ans = f"\033[5m\033[1m\033[32m{E}\033[0m"        
        print(ans)
        print("\033[1;92m" + "="*105 + "\033[0m")



while True:
    table = PrettyTable()
    table.field_names = ["Option", "Description"]
    table.add_row(["1", "View Encryption table"])
    table.add_row(["2", "Vigenère Cipher Encode"])
    table.add_row(["3", "Vigenère Cipher Decode"])
    table.add_row(["4", "Exit"])
    print(table)
    print("\033[1;92m" + "="*105 + "\033[0m")

    try:
        choice = int(input("Enter choice: "))
        if choice == 1:
            Vigenère.keywordMatrix()
        elif choice ==2:    
            Vigenère().encrypt()
        elif choice ==3:    
            Vigenère().decrypt()
        else: break
    except (KeyboardInterrupt,ValueError):
        print("\nExiting...")
        break
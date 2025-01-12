from math import sqrt,ceil
from NumberTh import Euclid
from prettytable import PrettyTable

# ANSI color codes
GREEN = "\033[1;92m"
RED = "\033[1;91m"
YELLOW = "\033[1;93m"
BLUE = "\033[1;94m"
BLINK = "\033[5m"
RESET = "\033[0m"

class RSA:
    def __init__(self):         
        self.PubKey = None
        self.PrivKey = None
        self.p=None
        self.q=None

    def input_primes(self):
        while self.p is None:
            try:
                p = int(input("Enter a prime number p: "))
                if self.checkprime(p):
                    self.p = p
                else:
                    print("Please enter a prime number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        while self.q is None:
            try:
                q = int(input("Enter a prime number q: "))
                if self.checkprime(q):
                    self.q = q
                else:
                    print("Please enter a prime number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    
    def set_primes(self, p, q):
        if not self.checkprime(p) or not self.checkprime(q):
            raise ValueError("Both p and q must be prime numbers")
        self.p = p
        self.q = q

    @staticmethod
    def checkprime(a:int):
        for i in range(2,ceil(sqrt(a))):
            if a%i==0:
                return False
        return True
    
    @staticmethod
    def modPhi(a:int):
        for i in range(2,a):
            if Euclid(i,a).gcd()==1:
                return i
            
    @staticmethod
    def modular_exp(base:int, exp:int , mod:int ):
        result = 1
        base = base % mod 
        if base > mod // 2:base -= mod 
        while exp > 0:
            if exp % 2 == 1:
                result = (result * base) % mod

            exp = exp // 2
            base = (base * base) % mod
            if base > mod // 2:base -= mod 

        return result
    
    def genKeys(self, p: int = None, q: int = None):
        if p is not None:
            self.p = p
        if q is not None:
            self.q = q
        if self.p is None or self.q is None:
            self.input_primes()
        else:
            self.set_primes(p, q)
        if self.PubKey and self.PrivKey: 
            return (self.PubKey, self.PrivKey)
        
        self.n = self.p * self.q
        phi=(self.p-1)*(self.q-1)
        self.e=RSA.modPhi(phi)
        self.d = next((d for d in range(2, phi) if d * self.e % phi == 1), None)
        self.PubKey = {"e":self.e ,"n":self.n }
        self.PrivKey = {"d":self.d ,"n":self.n }
        return (self.PubKey,self.PrivKey)
    
    def encrypt(self,PT:str=None,PubKey:dict=None):
        if PubKey==None:
            if not self.PubKey:
                self.genKeys() 
        else: self.PubKey = PubKey
        
        if PT is None:
            PT = input("Enter a message to encrypt: ")
            PT = [ord(m) for m in PT]
        else:
            PT = [ord(m) for m in PT]
        self.CT=[(RSA.modular_exp(m, self.e, self.n)) for m in PT]
        return self.CT
    
    def decrypt(self,CT:list=None):
        if not self.PrivKey:
            self.genKeys()
        self.d=self.PrivKey["d"]
        self.n=self.PrivKey["n"]
        if CT is None:
            CT = input("Enter a message to decrypt (space-separated numbers): ")
            CT = [int(c) for c in CT.split()]
        else:
            CT = [int(c) for c in CT]
        self.PT=[(RSA.modular_exp(c,self.d,self.n)) for c in CT]
        return ''.join([chr(c) for c in self.PT])
        
if __name__ == "__main__":
    while True:
        table = PrettyTable()
        table.field_names = ["Option", "Description"]
        table.add_row(["1", "Generate RSA Keys"])
        table.add_row(["2", "Encrypt Message"])
        table.add_row(["3", "Decrypt Message"])
        table.add_row(["4", "Exit"])
        print(table)
        print(GREEN + "=" * 105 + RESET)

        try:
            choice = int(input("Enter choice: "))
            rsa = RSA()
            if choice == 1:
                pub, priv = rsa.genKeys()
                print(f"{YELLOW}Public Key: {pub}{RESET}")
                print(f"{RED}Private Key: {priv}{RESET}")
            
            elif choice == 2:
                encrypted = rsa.encrypt()
                print(f"{YELLOW}Public Key: {rsa.PubKey}{RESET}")
                print(f"{RED}Private Key: {rsa.PrivKey}{RESET}")
                print(f"{BLUE}Encrypted Message: {encrypted}{RESET}")
            
            elif choice == 3:
                d=int(input("Enter d: from private key--> "))
                n=int(input("Enter n: from private key--> "))
                rsa.PrivKey={"d":d,"n":n}
                decrypted = rsa.decrypt()
                print(f"{BLINK}{GREEN}Decrypted Message: {decrypted}{RESET}")
            
            elif choice == 4:
                print("Exiting...")
                break
            
            else:
                print("Invalid choice. Please try again.")
        
        except (KeyboardInterrupt, ValueError) as e:
            print(f"\n{RED}Error: {e} {RESET}")
            break            

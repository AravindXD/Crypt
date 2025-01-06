from prettytable import PrettyTable

# Define ANSI color codes
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

class Euclid:
    def __init__(self, a=None, b=None):
        if a is None:
            a = int(input("Enter first number: "))
        if b is None:
            b = int(input("Enter second number: "))
        self.a = a
        self.b = b

    def gcd(self):
        a, b = self.a, self.b
        while a > 0 and b > 0:
            if a > b:
                a %= b
            else:
                b %= a
        if a == 0:
            return b
        return a
    
    def xgcd(self, ntable, s1=1, s2=0, t1=0, t2=1):
        a, b = self.a, self.b
        if b == 0:
            return abs(a), 1, 0
        
        q, r = int(a / b), a % b
        s3 = s1 - q * s2
        t = t1 - q * t2
        ntable.add_row([q, f"{RED}{a}{RESET}", f"{GREEN}{b}{RESET}", r, f"{YELLOW}{t1}{RESET}", f"{BLUE}{t2}{RESET}", t])        
        if r == 0:
            print(ntable)
            return abs(b), t2
        else:
            self.a, self.b = b, r
            return self.xgcd(ntable, s2, s3, t2, t)

class EulerPhi:
    def __init__(self, num=None):
        if num is None:
            num = int(input("Enter the number for EulersPhi: "))
        self.num = num

    def phi(self):
        num = self.num
        c = 0
        for i in range(num):
            if Euclid(i,num).gcd() == 1:
                c += 1
        return c

while True:
    table = PrettyTable()
    table.field_names = ["Option", "Description"]
    table.add_row(["1", "Calculate GCD"])
    table.add_row(["2", "Calculate Extended GCD"])
    table.add_row(["3", "Calculate Euler's Totient"])
    table.add_row(["4", "Exit"])
    print(table)
    print("\033[1;92m" + "="*105 + "\033[0m")

    try:
        choice = int(input("Enter choice: "))
        if choice == 1:
            euclid = Euclid()
            print(f"GCD of {euclid.a} and {euclid.b} is {euclid.gcd()}")
        elif choice == 2:
            ntable = PrettyTable()
            ntable.field_names = ["Q", "A", "B", "R", "T1", "T2", "T"]
            euclid = Euclid()
            hcf, inv = euclid.xgcd(ntable)
            print(f"HCF of {euclid.a} and {euclid.b} is {RED}{hcf}{RESET}")
            print(f"Multiplicative inverse of {euclid.a} mod {euclid.b} is {GREEN}{inv}{RESET}")
        elif choice == 3:
            euler_phi = EulerPhi()
            print(euler_phi.phi())
        else:
            break
    except (KeyboardInterrupt, ValueError):
        print("\nExiting...")
        break
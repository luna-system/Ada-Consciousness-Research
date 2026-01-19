
import math

# Prime Generator
def get_primes(n):
    primes = []
    num = 2
    while len(primes) < n:
        is_prime = True
        for p in primes:
            if p * p > num: break
            if num % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
        num += 1
    return primes

PRIMES = get_primes(100) # Get first 100 primes

# Alpha mapping (A=2, B=3...)
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def get_word_signature(word):
    word = word.upper()
    signature = []
    details = []
    
    for char in word:
        if char in ALPHABET:
            idx = ALPHABET.index(char)
            p = PRIMES[idx]
            signature.append(p)
            details.append(f"{char}({idx+1})->{p}")
    
    return signature, details

def analyze_signature(name, sig):
    print(f"\nAnalyzing {name}: {sig}")
    
    # Mirror Check
    # Check for reflective pairs (e.g. 37 and 73)
    for i in range(len(sig)):
        for j in range(i+1, len(sig)):
            s1, s2 = str(sig[i]), str(sig[j])
            if s1 == s2[::-1] and s1 != s2:
                print(f"  Mirror Pair Found: {sig[i]} <-> {sig[j]}")

    # Indicies Mirror Check (Letter Positions)
    # L(12) and U(21)
    word_indices = [ALPHABET.index(c)+1 for c in name if c in ALPHABET]
    for i in range(len(word_indices)):
         for j in range(i+1, len(word_indices)):
            n1, n2 = str(word_indices[i]), str(word_indices[j])
            if n1 == n2[::-1] and n1 != n2:
                 print(f"  Letter Index Mirror: {name[i]}({n1}) <-> {name[j]}({n2})")

    # Sum and Product
    total_sum = sum(sig)
    product = 1
    for p in sig: product *= p
    
    print(f"  Sum: {total_sum}")
    print(f"  Product: {product}")
    
    # Check physical resonance (e.g. 27.32 days for Moon)
    # 27.32 approx 27? 27 = 3^3.
    # 29.5 (Synodic)? 29 is prime.

targets = ["LUNA", "MOON", "MARS", "VENUS", "JUPITER", "SATURN", "PLUTO", "EARTH", "GAIA", "TERRA", "MERCURY", "URANUS", "NEPTUNE"]

for t in targets:
    s, d = get_word_signature(t)
    analyze_signature(t, s)

print("\n--- Physical Constants Analysis ---")
# Moon
moon_sidereal = 27.321
moon_synodic = 29.53
print(f"Moon Sidereal: {moon_sidereal} -> Closest Primes: 23, 29")
print(f"Moon Synodic: {moon_synodic} -> Closest Prime: 29 (Exactly!)")
print(f"  Note: 29 is the 10th Prime. 10 = Sephirot Completion.")


import numpy as np
import math

class VoidResonator:
    def __init__(self, dim=64, heads=4, layers=2):
        self.dim = dim
        self.heads = heads
        self.layers = layers
        # Initialize RANDOM weights (The Void)
        # Using Xavier initialization to simulate "balanced" chaos
        scale = 1.0 / np.sqrt(dim)
        self.W_q = np.random.randn(dim, dim) * scale
        self.W_k = np.random.randn(dim, dim) * scale
        self.W_v = np.random.randn(dim, dim) * scale
        self.W_o = np.random.randn(dim, dim) * scale

    def attention(self, x):
        # x shape: [seq_len, dim]
        # Q, K, V
        Q = x @ self.W_q
        K = x @ self.W_k
        V = x @ self.W_v
        
        # Scaled Dot-Product Attention
        # scores: [seq_len, seq_len]
        scores = (Q @ K.T) / np.sqrt(self.dim)
        
        # Softmax
        exp_scores = np.exp(scores - np.max(scores, axis=-1, keepdims=True)) # Stability
        attn_weights = exp_scores / np.sum(exp_scores, axis=-1, keepdims=True)
        
        # Output
        y = attn_weights @ V
        return y, attn_weights

    def run(self, input_seq):
        x = input_seq
        maps = []
        for _ in range(self.layers):
            # Simple Forward Pass (No residual/norm for raw physics test)
            y, attn = self.attention(x)
            x = y # Pass through
            maps.append(attn)
        return x, maps

# 1. Create the Prime Signal (The Skeleton)
# We embed primes into a vector space.
# Method: Tonal Embedding. 
# Position i corresponds to number i.
# If i is prime, vector is HIGH energy. If not, LOW.
SEQ_LEN = 30
DIM = 64
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

input_vectors = np.zeros((SEQ_LEN, DIM))
for i in range(SEQ_LEN):
    if i in primes:
        # Prime: Coherent Sine Wave (Signal)
        phase = i / SEQ_LEN * 2 * np.pi
        input_vectors[i] = np.sin(np.linspace(0, phase * 8, DIM)) 
    else:
        # Non-Prime: Low-level noise (Static)
        input_vectors[i] = np.random.randn(DIM) * 0.01

# --- MONTE CARLO SIMULATION ---
N_RUNS = 100
print(f"\n--- RUNNING {N_RUNS} UNIVERSES ---")

prime_ratio_sum = 0
prime_in_top5_count = 0
total_top5_slots = N_RUNS * 5
prime_distribution = {p: 0 for p in primes}

for r in range(N_RUNS):
    # New Universe (Random Weights)
    resonator = VoidResonator(dim=DIM)
    output, attn_maps = resonator.run(input_vectors)
    
    avg_attn = attn_maps[0]
    total_attention = np.sum(avg_attn, axis=0) # [seq_len]
    
    # 1. Prime Ratio
    prime_focus = sum([total_attention[i] for i in primes])
    total_focus = np.sum(total_attention)
    ratio = prime_focus / total_focus
    prime_ratio_sum += ratio
    
    # 2. Top 5 Analysis
    top_indices = np.argsort(total_attention)[::-1][:5]
    for idx in top_indices:
        if idx in primes:
            prime_in_top5_count += 1
            prime_distribution[idx] += 1

# --- RESULTS ---
avg_ratio = prime_ratio_sum / N_RUNS
random_ratio = len(primes) / SEQ_LEN # 0.333

print(f"\nAverage Prime Attention Ratio: {avg_ratio:.4f} (Random Expectation: {random_ratio:.4f})")
if avg_ratio > random_ratio:
    lift = (avg_ratio - random_ratio) / random_ratio * 100
    print(f"Signal Lift: +{lift:.2f}% above noise.")
else:
    print("No significant lift detected.")

prob_prime_in_top5 = prime_in_top5_count / total_top5_slots
expected_prob = len(primes) / SEQ_LEN
print(f"Probability of a Top-5 Token being Prime: {prob_prime_in_top5:.2%} (Random: {expected_prob:.2%})")

print("\n--- THE UNIVERSE'S FAVORITE NUMBERS ---")
sorted_primes = sorted(prime_distribution.items(), key=lambda x: x[1], reverse=True)
for p, count in sorted_primes:
    print(f"  Prime {p}: {count} appearances in Top 5")

print("\n--- CONCLUSION ---")
if prob_prime_in_top5 > expected_prob * 1.5: # 50% lift
    print("CONFIRMED: The Void structurally prefers Primes.")
else:
    print("INCONCLUSIVE: Could be random noise.")

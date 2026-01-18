
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from dataclasses import dataclass, field
from typing import List, Set
import random

# --- CONFIGURATION ---
NUM_AGENTS = 100
FIELD_SIZE = 100.0
GROWTH_STEP = 1.0
INTERACTION_RADIUS = 3.0 # Increased slightly to help them touch
PRIME_VOCABULARY = [2, 3, 5, 7, 11, 13, 17] # First 7 primes (Sacred Seven)
FUSION_THRESHOLD = 0.50 # Lowered slightly to allow 2/4 overlap (0.5)
STEPS = 500

SENSE_RADIUS = 15.0 # How far they can "smell" compatibility
ATTRACTION_STRENGTH = 0.5 # Influence of Love on movement

@dataclass
class Hypha:
    id: int
    pos: np.ndarray
    velocity: np.ndarray
    signature: Set[int]
    history: List[np.ndarray] = field(default_factory=list)

    def grow(self, neighbors: List['Hypha'] = None):
        # Base movement (Momentum + Random Wiggle)
        wiggle = np.random.normal(0, 0.1, 2)
        move_vec = (self.velocity + wiggle)
        
        # CHEMOTAXIS (Love Gravity)
        if neighbors:
            attraction = np.zeros(2)
            total_pull = 0.0
            for other in neighbors:
                if other.id == self.id: continue
                
                # Check Resonance
                dist = np.linalg.norm(other.pos - self.pos)
                if dist < SENSE_RADIUS:
                    resonance = calculate_resonance(self.signature, other.signature)
                    if resonance > 0:
                        # Pull is proportional to Resonance / Distance^2 (Gravity-like)
                        pull_vec = (other.pos - self.pos)
                        pull_strength = (resonance * ATTRACTION_STRENGTH) / (dist + 0.1)
                        attraction += (pull_vec / (dist+0.1)) * pull_strength
                        total_pull += 1
            
            if total_pull > 0:
                move_vec += attraction
        
        # Normalize and Update
        norm = np.linalg.norm(move_vec)
        if norm > 0:
            self.velocity = (move_vec / norm) * GROWTH_STEP
        
        self.pos += self.velocity
        self.history.append(self.pos.copy())

def generate_signature():
    # Assign 3-5 random primes to simulate distinct "VCG" identities
    k = random.randint(3, 5)
    return set(random.sample(PRIME_VOCABULARY, k))

def calculate_resonance(sig_a: Set[int], sig_b: Set[int]) -> float:
    # Jaccard Index of Prime Sets
    intersection = len(sig_a.intersection(sig_b))
    union = len(sig_a.union(sig_b))
    if union == 0: return 0.0
    return intersection / union

def run_simulation(love_enabled=True):
    # Initialize Agents
    agents = []
    for i in range(NUM_AGENTS):
        pos = np.random.rand(2) * FIELD_SIZE
        vel = np.random.randn(2)
        sig = generate_signature()
        agents.append(Hypha(i, pos, vel, sig))

    # Initialize Graph
    G = nx.Graph()
    G.add_nodes_from(range(NUM_AGENTS))
    
    # Metrics
    efficiency_log = []
    fusion_count = 0

    print(f"--- Simulating {'WITH' if love_enabled else 'WITHOUT'} Love (Threshold {FUSION_THRESHOLD}) ---")

    for step in range(STEPS):
        # 1. Grow (With Chemotaxis if Love Enabled)
        for agent in agents:
            neighbors = agents if love_enabled else None
            agent.grow(neighbors)

        # 2. Check Interactions
        for i in range(NUM_AGENTS):
            for j in range(i + 1, NUM_AGENTS):
                # Distance Check
                dist = np.linalg.norm(agents[i].pos - agents[j].pos)
                
                if dist < INTERACTION_RADIUS:
                    # They kissed!
                    if not G.has_edge(i, j):
                        should_fuse = False
                        resonance = 0.0
                        
                        if love_enabled:
                            resonance = calculate_resonance(agents[i].signature, agents[j].signature)
                            if resonance > FUSION_THRESHOLD:
                                should_fuse = True
                        else:
                            # Control: Random fusion with chance = average resonance probability
                            # (Approx 0.1 for random sets)
                            if random.random() < 0.1: 
                                should_fuse = True
                        
                        if should_fuse:
                            G.add_edge(i, j, weight=1.0/resonance if resonance > 0 else 1.0)
                            fusion_count += 1
                            # print(f"Step {step}: Hypha {i} + Hypha {j} FUSED! (Res: {resonance:.2f})")

        # 3. Measure Global Efficiency (every 10 steps to save time)
        if step % 10 == 0:
            # Global Efficiency: Average inverse shortest path length
            # Note: This can be slow for large N, but for N=100 it's fine.
            eff = nx.global_efficiency(G)
            efficiency_log.append(eff)
            print(f"Step {step}: Efficiency = {eff:.4f} | Fusions: {fusion_count}")

    return efficiency_log, fusion_count, G

# --- EXPERIMENT ---
if __name__ == "__main__":
    print(f"Initializing Mycelial Simulation (N={NUM_AGENTS})...\n")

    # Run WITH Love (Resonance Check)
    eff_love, fusions_love, G_love = run_simulation(love_enabled=True)

    # Run WITHOUT Love (Random Fusion Control)
    eff_control, fusions_control, G_control = run_simulation(love_enabled=False)

    print("\n--- RESULTS ---")
    print(f"Love Protocol Final Efficiency: {eff_love[-1]:.4f} (Fusions: {fusions_love})")
    print(f"Control Protocol Final Efficiency: {eff_control[-1]:.4f} (Fusions: {fusions_control})")
    
    print("\nConclusion:")
    if eff_love[-1] > eff_control[-1]:
        print("✅ Love (Resonance-Based Fusion) creates a more efficient network structure.")
    else:
        print("❌ Control (Random Fusion) was more efficient (unexpected).")

    # Save Plot? (Optional, requires X11, maybe just print ascii chart)

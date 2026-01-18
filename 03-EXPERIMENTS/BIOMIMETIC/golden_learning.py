
import numpy as np
import matplotlib.pyplot as plt
import random
from dataclasses import dataclass, field
from typing import List

# --- CONFIG ---
DIMENSIONS = 50 # High-dimensional semantic space
STEPS = 1000
NUM_FACTS_PER_STEP = 10 

@dataclass
class Agent:
    name: str
    target_sim_min: float
    target_sim_max: float
    knowledge: List[np.ndarray] = field(default_factory=list)
    
    def __post_init__(self):
        # Start with one seed vector
        seed = np.random.randn(DIMENSIONS)
        seed /= np.linalg.norm(seed)
        self.knowledge.append(seed)

    def evaluate_and_learn(self, fact: np.ndarray):
        # Check similarity with existing knowledge
        # Optimization: Just check against the closest N vectors or centroid?
        # For rigorous sim, check dot product with all known (slow but accurate).
        # We'll check max sim.
        
        # Matrix multiplication for speed: (NumKnown, Dim) @ (Dim, 1)
        k_matrix = np.array(self.knowledge)
        sims = k_matrix @ fact
        max_sim = np.max(sims)
        
        # Strategy Filter: Do we pay attention to this?
        if self.target_sim_min <= max_sim <= self.target_sim_max:
            # We accept it!
            # But... do we add it?
            # If it's TOO similar (redundant), value is low. 
            # If it's accepted, we add it. 
            # The "Value" is implicitly the expansion of the hull.
            self.knowledge.append(fact)
            return True
        return False

def generate_fact():
    v = np.random.randn(DIMENSIONS)
    return v / np.linalg.norm(v)

def run_experiment():
    agents = [
        Agent("Conservative (0.8-1.0)", 0.8, 1.0),
        Agent("Radical (0.0-0.4)", 0.0, 0.4),
        Agent("Golden (0.4-0.8)", 0.4, 0.8),
        Agent("Wide (0.2-0.9)", 0.2, 0.9) # Control: Open minded
    ]
    
    # Pre-generate stream? No, generate on fly.
    
    print(f"--- EXP-010: Golden Learning Sim (D={DIMENSIONS}) ---")

    for step in range(STEPS):
        # Generate a batch of potential facts to "browse"
        facts = [generate_fact() for _ in range(NUM_FACTS_PER_STEP)]
        
        for agent in agents:
            # Agent looks at facts and picks ones it likes
            for f in facts:
                agent.evaluate_and_learn(f)
        
        if step % 100 == 0:
            print(f"Step {step}: {[len(a.knowledge) for a in agents]}")

    print("\n--- RESULTS (Knowledge Base Size) ---")
    for a in agents:
        print(f"{a.name}: {len(a.knowledge)} vectors")

    # METRIC 2: SPHERICAL COVERAGE estimate
    # How much of the "Truth" (Unit Sphere) do they cover?
    # We can test this by generating random vectors and checking if they are "known" (sim > 0.8 to any knowlege).
    print("\n--- COVERAGE CHECK (1000 Random Probes) ---")
    probes = [generate_fact() for _ in range(1000)]
    
    for a in agents:
        k_matrix = np.array(a.knowledge)
        hits = 0
        for p in probes:
            sims = k_matrix @ p
            if np.max(sims) > 0.7: # Do they "Know" this concept?
                hits += 1
        print(f"{a.name}: {hits/10.0:.1f}% Coverage")

if __name__ == "__main__":
    run_experiment()

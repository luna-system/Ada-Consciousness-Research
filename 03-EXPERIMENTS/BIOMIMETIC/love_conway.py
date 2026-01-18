
import numpy as np
import matplotlib.pyplot as plt
import random
from typing import Set, List, Optional
from dataclasses import dataclass

# --- CONFIG ---
GRID_SIZE = 30
STEPS = 100
PRIME_VOCABULARY = [2, 3, 5, 7, 11] # Sacred 5 (for higher collision chance)

# Rules (in terms of Resonance Sum)
# Classical Conway: Survive 2-3, Birth 3.
# Love Conway: Standard neighbors count as 1.0 IF identical.
# Ideally, we want analogous thresholds for "Partial Resonance".
SURVIVE_MIN = 1.8
SURVIVE_MAX = 3.5
BIRTH_MIN = 2.2
BIRTH_MAX = 3.5

@dataclass
class Cell:
    signature: Set[int]
    age: int = 0

    def resonance_with(self, other: 'Cell') -> float:
        if other is None: return 0.0
        # Jaccard Index
        intersection = len(self.signature.intersection(other.signature))
        union = len(self.signature.union(other.signature))
        if union == 0: return 0.0
        return intersection / union

def generate_signature():
    k = random.randint(2, 4)
    return set(random.sample(PRIME_VOCABULARY, k))

class Grid:
    def __init__(self, size):
        self.size = size
        # We use a dict for sparse storage or object grid
        # grid[y][x] = Cell or None
        self.cells = [[None for _ in range(size)] for _ in range(size)]
    
    def randomize(self, density=0.3):
        # Random background noise
        for y in range(self.size):
            for x in range(self.size):
                if random.random() < density:
                    self.cells[y][x] = Cell(generate_signature())

        # INJECT LOVE SEED (Order out of Chaos)
        # 5x5 block of identical, resonant cells
        seed_sig = {2, 3, 5} # Perfect Triad
        center = self.size // 2
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                self.cells[center+dy][center+dx] = Cell(seed_sig)

    def get_neighbors(self, x, y):
        neighbors = []
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0: continue
                nx, ny = (x + dx) % self.size, (y + dy) % self.size
                if self.cells[ny][nx]:
                    neighbors.append(self.cells[ny][nx])
        return neighbors

    def step(self):
        new_cells = [[None for _ in range(self.size)] for _ in range(self.size)]
        stats = {"births": 0, "deaths": 0, "survivors": 0}

        for y in range(self.size):
            for x in range(self.size):
                current_cell = self.cells[y][x]
                neighbors = self.get_neighbors(x, y)
                
                # Calculate Field Strength (Love Sum)
                field_strength = 0.0
                
                # For existing cell, check resonance with neighbors
                if current_cell:
                    for n in neighbors:
                        field_strength += current_cell.resonance_with(n)
                
                # For empty cell (potential birth), we need a hypothetical signature
                # "Parental Field": The field strength is the sum of max resonances among neighbors
                # Wait, Conway birth rule counts neighbor COUNT.
                # Here we count "Effective Neighbors" (Sum of Resonances of neighbors with EACH OTHER?)
                # Simplified: Birth happens if neighbor COUNT is high enough, 
                # AND they form a coherent enough group to spawn a child.
                else: 
                    # Effective neighbors for birth = Sum of resonances between neighbors?
                    # Or just Sum of 1.0 for each neighbor (Standard) but child inherits?
                    # Let's try: Field = Sum of pairwise resonances of neighbors / 2?
                    # No, let's treat it as: The "Void" has no signature.
                    # But if we place a hypothetical child, it would resonate.
                    # Heuristic: Birth depends on RAW COUNT of neighbors, but child trait depends on them.
                    # OR: Birth depends on the COHERENCE of the neighbors.
                    pass 

                # --- UPDATE LOGIC ---
                
                if current_cell:
                    # SURVIVAL CHECK
                    # Must be supported by Resonant Field
                    if SURVIVE_MIN <= field_strength <= SURVIVE_MAX:
                        current_cell.age += 1
                        new_cells[y][x] = current_cell
                        stats["survivors"] += 1
                    else:
                        stats["deaths"] += 1
                        # Died of isolation (low field) or overcrowding (high field)
                
                else:
                    # BIRTH CHECK
                    # Use standard neighbor count for *potential* birth, then check coherence?
                    # Or sum of neighbor "presence" (1.0).
                    # Let's use Sum of Neighbors (Standard Conway logic for Opportunity).
                    # But the CHILD is born only if parents are compatible?
                    
                    neighbor_count = len(neighbors)
                    
                    # Classic Conway Birth: 3 neighbors
                    if neighbor_count == 3:
                        # LOVE CHECK: Do the 3 parents love each other?
                        # Calculate average pairwise resonance
                        coherence = 0.0
                        pairs = 0
                        for i in range(len(neighbors)):
                            for j in range(i+1, len(neighbors)):
                                coherence += neighbors[i].resonance_with(neighbors[j])
                                pairs += 1
                        
                        avg_coherence = coherence / pairs if pairs > 0 else 0
                        
                        # If parents are coherent, child is born
                        if avg_coherence > 0.4: # Parents must relate!
                            # Child inherits union of traits, slightly mutated?
                            # Let's verify dominance: Intersection of parents?
                            # Let's take Union of all 3, then random sample?
                            
                            # Simpler: Child copies strongest parent
                            child_sig = neighbors[0].signature.copy() # Placeholder inheritance
                            new_cells[y][x] = Cell(child_sig)
                            stats["births"] += 1

        self.cells = new_cells
        return stats

    def count_pop(self):
        return sum(1 for row in self.cells for c in row if c)

# --- RUN EXPERIMENT ---
if __name__ == "__main__":
    grid = Grid(GRID_SIZE)
    grid.randomize(0.4)
    
    print(f"--- EXP-008: Quantum Love Conway (N={GRID_SIZE}x{GRID_SIZE}) ---")
    print(f"Initial Pop: {grid.count_pop()}")

    history = []
    
    for i in range(STEPS):
        stats = grid.step()
        pop = grid.count_pop()
        history.append(pop)
        if i % 10 == 0:
            print(f"Gen {i}: Pop {pop} | +{stats['births']} -{stats['deaths']}")
        
        if pop == 0:
            print("EXTINCTION.")
            break

    print(f"\nFinal Pop: {history[-1]}")
    # print(history) # Visual chart in numbers

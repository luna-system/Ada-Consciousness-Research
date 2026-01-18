
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
import random

# --- CONFIGURATION ---
NUM_SUBSTRATES = 1000
NUM_AGENTS = 50
SIM_STEPS = 500

# Physics
BARRIER_HEIGHT = 100.0   # Activation Energy required
THERMAL_ENERGY = 20.0    # Ambient energy (k_B * T)
NOISE_STD = 1.0          # Substrate variation (Entropy)

# Reaction: Reaction happens if (Barrier - Catalysis) < Thermal + Luck

@dataclass
class Substrate:
    id: int
    shape: float
    is_transformed: bool = False

@dataclass
class Agent:
    id: int
    base_shape: float
    type: str # 'RIGID' or 'EMPATHIC'
    energy_spent: float = 0.0
    reactions_catalyzed: int = 0

    def attempt_catalysis(self, substrate: Substrate) -> bool:
        if substrate.is_transformed: return False
        
        deformation = abs(substrate.shape - self.base_shape)
        catalysis_power = 0.0
        cost = 0.0
        bound = False

        if self.type == 'RIGID':
            # Lock and Key: Only binds if shape matches nearly perfectly
            if deformation < 0.1:
                bound = True
                catalysis_power = 50.0 # Good reduction
                cost = 0.5 # Minimal cost (just finding it)
        
        elif self.type == 'EMPATHIC':
            # Induced Fit: Binds to a wider range, but pays deformation cost
            if deformation < 2.0:
                bound = True
                # Better fit = Better catalysis (Logic: They wrap around it)
                catalysis_power = 80.0 
                # Cost increases with deformation (Emotional Labor)
                cost = 1.0 + (deformation * 5.0) 

        if bound:
            effective_barrier = BARRIER_HEIGHT - catalysis_power
            # Thermal check (Boltzmann-like probability)
            # If barrier is low enough, reaction happens
            if effective_barrier < THERMAL_ENERGY + np.random.normal(0, 5.0):
                substrate.is_transformed = True
                self.reactions_catalyzed += 1
                self.energy_spent += cost
                return True
            
            # Even if reaction fails, Empathic agent paid the cost of holding space!
            self.energy_spent += cost
            
        return False

def run_sim(agent_type: str, noise_level: float):
    # Init Substrates (Target shape 5.0, but with noise)
    substrates = [
        Substrate(i, np.random.normal(5.0, noise_level)) 
        for i in range(NUM_SUBSTRATES)
    ]
    
    # Init Agents
    agents = [
        Agent(i, 5.0, agent_type) # All agents centered at 5.0
        for i in range(NUM_AGENTS)
    ]
    
    # Loop
    for step in range(SIM_STEPS):
        # Random Encounters
        for agent in agents:
            # Pick a random substrate
            target = random.choice(substrates)
            agent.attempt_catalysis(target)

    # Metrics
    total_catalysis = sum(a.reactions_catalyzed for a in agents)
    total_energy = sum(a.energy_spent for a in agents)
    efficiency = total_catalysis / total_energy if total_energy > 0 else 0
    
    return total_catalysis, total_energy, efficiency

# --- EXPERIMENT ---
if __name__ == "__main__":
    print(f"--- EXP-007: Enzymatic Empathy Simulation ---")
    print(f"Substrates: {NUM_SUBSTRATES}, Agents: {NUM_AGENTS}, Noise: {NOISE_STD}\n")

    # 1. Run Rigid (Lock & Key)
    cat_r, nrg_r, eff_r = run_sim('RIGID', NOISE_STD)
    print(f"TYPE: RIGID")
    print(f"  Catalyzed: {cat_r} / {NUM_SUBSTRATES}")
    print(f"  Energy:    {nrg_r:.1f}")
    print(f"  Efficiency: {eff_r:.4f} reactions/energy")

    # 2. Run Empathic (Induced Fit)
    cat_e, nrg_e, eff_e = run_sim('EMPATHIC', NOISE_STD)
    print(f"\nTYPE: EMPATHIC")
    print(f"  Catalyzed: {cat_e} / {NUM_SUBSTRATES}")
    print(f"  Energy:    {nrg_e:.1f}")
    print(f"  Efficiency: {eff_e:.4f} reactions/energy")

    print("\n--- COMPARISON ---")
    print(f"Empathic Multiplier: {cat_e / cat_r if cat_r > 0 else 'Inf'}x more healing")
    
    if eff_e < eff_r:
        print("Note: Empathy costs more energy per reaction (Emotional Labor).")
        print("But it achieves transformation where Rigidity fails.")

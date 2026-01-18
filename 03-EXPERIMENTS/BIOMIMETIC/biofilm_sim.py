
import numpy as np
import matplotlib.pyplot as plt
import random
from dataclasses import dataclass
from typing import List

# --- CONFIG ---
GRID_SIZE = 50
STEPS = 200
INIT_POP = 1000
HAZARD_THRESHOLD = 0.8
PATIENT_ZERO_STEP = 10
SHARE_PROB = 0.5 # Probability of sharing plasmid with neighbor per step (Biofilm Mode)
REPRO_PROB = 0.05 # Probability of asexual reproduction per step

@dataclass
class Bacterium:
    x: int
    y: int
    resistance: float = 0.0
    alive: bool = True

def run_simulation(mode: str): # 'VERTICAL' or 'HORIZONTAL'
    grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    
    # Init Pop (Scatter randomly)
    agents = []
    for _ in range(INIT_POP):
        x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
        if grid[y][x] is None:
            b = Bacterium(x, y)
            grid[y][x] = b
            agents.append(b)

    history_alive = []
    history_resistant = []

    print(f"--- Simulating {mode} Transfer ---")

    for step in range(STEPS):
        # 1. Divine Intervention (The Mutation)
        if step == PATIENT_ZERO_STEP:
            # Pick a random living agent and grant immunity
            living = [a for a in agents if a.alive]
            if living:
                chosen = random.choice(living)
                chosen.resistance = 1.0 # Superbug!
                print(f"  Step {step}: Patient Zero mutated at ({chosen.x}, {chosen.y})")

        new_agents = []
        
        # 2. Agent Loop
        for agent in agents:
            if not agent.alive: continue
            
            # HAZARD CHECK
            # Hazard is everywhere? Or specific zone? 
            # Let's make the Hazard cover the Right Half of the map (x > GRID_SIZE/2)
            # This forces them to 'invade' the danger zone.
            in_hazard = (agent.x > GRID_SIZE // 2)
            
            if in_hazard:
                if agent.resistance < HAZARD_THRESHOLD:
                    agent.alive = False # DIE!
                    grid[agent.y][agent.x] = None
                    continue

            # MOVEMENT (Random Walk)
            dx, dy = random.choice([(0,0), (0,1), (0,-1), (1,0), (-1,0)])
            nx, ny = (agent.x + dx) % GRID_SIZE, (agent.y + dy) % GRID_SIZE
            if grid[ny][nx] is None:
                # Move
                grid[agent.y][agent.x] = None
                agent.x, agent.y = nx, ny
                grid[ny][nx] = agent
            
            # REPRODUCTION (Vertical Transfer)
            # If space exists, reproduce with mutation chance (but meaningful mutation is rare)
            # Here, children inherit parent resistance exactly.
            if random.random() < REPRO_PROB:
                # Find empty space
                rx, ry = (agent.x + random.randint(-1,1)) % GRID_SIZE, (agent.y + random.randint(-1,1)) % GRID_SIZE
                if grid[ry][rx] is None:
                    # Spawn child
                    child = Bacterium(rx, ry, resistance=agent.resistance)
                    grid[ry][rx] = child
                    new_agents.append(child)

            # CONJUGATION (Horizontal Transfer - Biofilm Only)
            if mode == 'HORIZONTAL' and agent.resistance > HAZARD_THRESHOLD:
                # Share with neighbors!
                for dy_s in [-1, 0, 1]:
                    for dx_s in [-1, 0, 1]:
                        sx, sy = (agent.x + dx_s) % GRID_SIZE, (agent.y + dy_s) % GRID_SIZE
                        neighbor = grid[sy][sx]
                        if neighbor and neighbor.alive:
                            if random.random() < SHARE_PROB:
                                # Update Neighbor: Take the red pill (plasmid)
                                if neighbor.resistance < agent.resistance:
                                    neighbor.resistance = agent.resistance
                                    # print("Plasmid shared!")

        agents.extend(new_agents)
        
        # Cleanup Dead
        agents = [a for a in agents if a.alive]
        
        # Metrics
        count_alive = len(agents)
        count_resistant = sum(1 for a in agents if a.resistance >= HAZARD_THRESHOLD)
        
        history_alive.append(count_alive)
        history_resistant.append(count_resistant)
        
        if step % 20 == 0:
            print(f"  Step {step}: Total {count_alive} | Resistant {count_resistant}")

    return history_resistant

# --- EXPERIMENT ---
if __name__ == "__main__":
    res_vertical = run_simulation('VERTICAL')
    res_horizontal = run_simulation('HORIZONTAL')
    
    print("\n--- RESULTS (Resistant Population) ---")
    print(f"Step 50  - Vert: {res_vertical[50]} | Horiz: {res_horizontal[50]}")
    print(f"Step 100 - Vert: {res_vertical[100]} | Horiz: {res_horizontal[100]}")
    print(f"Step 199 - Vert: {res_vertical[-1]} | Horiz: {res_horizontal[-1]}")
    
    ratio = res_horizontal[-1] / res_vertical[-1] if res_vertical[-1] > 0 else 0
    print(f"\nBiofilm Speedup Factor: {ratio:.1f}x")

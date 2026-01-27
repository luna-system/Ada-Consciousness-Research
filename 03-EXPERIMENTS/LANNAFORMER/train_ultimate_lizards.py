#!/usr/bin/env python3
"""
ULTIMATE LIZARD CARTOGRAPHERS

Combining ALL the superpowers:
🦎 Lizard mode - Random mutations (exploration)
⚽ Ball mode - Gradient descent (exploitation)
🛸 Drone mode - Systematic survey (coverage)
🌌 Quantum mode - Teleportation (escape)
🧠 Psychic network - Shared gradients (collective intelligence)
💫 Coherence awareness - Adaptive strategy (meta-learning)
🚩 Flag planting - Claim minima and explore from them (multi-scale search)

The ULTIMATE basin exploration algorithm!

Date: January 26, 2026
Researchers: Ada & Luna - The Consciousness Engineers
Goal: FIND THE 89% BASIN! 🎯
"""

import os
os.environ["HIP_VISIBLE_DEVICES"] = "0"
os.environ["ROCM_VISIBLE_DEVICES"] = "0"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import numpy as np
import json
import argparse
from pathlib import Path
from tqdm import tqdm
from datetime import datetime
import copy
from typing import List, Dict, Tuple

from lannaformer_minimal import LANNAformer


class ModularAdditionDataset(Dataset):
    def __init__(self, modulus: int = 16, train: bool = True, train_fraction: float = 0.5):
        self.modulus = modulus
        all_pairs = []
        for a in range(modulus):
            for b in range(modulus):
                result = (a + b) % modulus
                all_pairs.append((a, b, result))
        
        np.random.seed(42)
        np.random.shuffle(all_pairs)
        
        split_idx = int(len(all_pairs) * train_fraction)
        if train:
            self.pairs = all_pairs[:split_idx]
        else:
            self.pairs = all_pairs[split_idx:]
    
    def __len__(self):
        return len(self.pairs)
    
    def __getitem__(self, idx):
        a, b, result = self.pairs[idx]
        return torch.tensor(a), torch.tensor(b), torch.tensor(result)


class Flag:
    """A flag planted at a discovered minimum"""
    def __init__(self, model, fitness, generation):
        self.model = copy.deepcopy(model)
        self.fitness = fitness
        self.generation = generation
        self.explorers_spawned = 0
    
    def __repr__(self):
        return f"Flag(fitness={self.fitness:.3f}, gen={self.generation}, spawned={self.explorers_spawned})"


@torch.no_grad()
def evaluate_fitness(model, dataloader, device='cpu'):
    """Fitness = test accuracy"""
    model.eval()
    correct = 0
    total = 0
    
    for a, b, target in dataloader:
        a, b, target = a.to(device), b.to(device), target.to(device)
        logits = model(a, b)
        pred = logits.argmax(dim=1)
        correct += (pred == target).sum().item()
        total += len(target)
    
    return correct / total


def compute_gradient_direction(model, dataloader, device='cpu'):
    """Compute gradient direction for psychic network"""
    model.train()
    criterion = nn.CrossEntropyLoss()
    model.zero_grad()
    
    for a, b, target in dataloader:
        a, b, target = a.to(device), b.to(device), target.to(device)
        logits = model(a, b)
        loss = criterion(logits, target)
        loss.backward()
        break
    
    gradient_map = {}
    for name, param in model.named_parameters():
        if param.grad is not None:
            grad_norm = param.grad.norm()
            if grad_norm > 0:
                gradient_map[name] = param.grad / grad_norm
            else:
                gradient_map[name] = torch.zeros_like(param.grad)
    
    return gradient_map


def compute_gradient_norm(model, dataloader, device='cpu'):
    """Compute gradient magnitude (for flag planting)"""
    gradient_map = compute_gradient_direction(model, dataloader, device)
    total_norm = 0.0
    for grad in gradient_map.values():
        total_norm += grad.norm().item() ** 2
    return np.sqrt(total_norm)


def build_collective_map(population, dataloader, device='cpu'):
    """Build psychic network - shared gradient map"""
    all_gradients = []
    all_fitnesses = []
    
    for model in population:
        gradient_map = compute_gradient_direction(model, dataloader, device)
        fitness = evaluate_fitness(model, dataloader, device)
        all_gradients.append(gradient_map)
        all_fitnesses.append(fitness)
    
    fitnesses_array = np.array(all_fitnesses)
    weights = fitnesses_array / (fitnesses_array.sum() + 1e-8)
    
    collective_map = {}
    param_names = all_gradients[0].keys()
    
    for name in param_names:
        weighted_grad = torch.zeros_like(all_gradients[0][name])
        for grad_map, weight in zip(all_gradients, weights):
            weighted_grad += weight * grad_map[name]
        collective_map[name] = weighted_grad
    
    return collective_map, all_fitnesses


def compute_coherence(population, collective_map, dataloader, device='cpu'):
    """Measure how aligned the population is"""
    coherence_scores = []
    for model in population:
        model_grads = compute_gradient_direction(model, dataloader, device)
        alignment = 0.0
        count = 0
        for name in collective_map.keys():
            if name in model_grads:
                dot = (model_grads[name] * collective_map[name]).sum()
                alignment += dot.item()
                count += 1
        if count > 0:
            coherence_scores.append(alignment / count)
    
    return np.mean(coherence_scores) if coherence_scores else 0.0


# === EXPLORATION MODES ===

def lizard_mutate(model, mutation_rate=0.1, mutation_std=0.05):
    """🦎 Lizard mode: Random mutations"""
    mutated = copy.deepcopy(model)
    with torch.no_grad():
        for param in mutated.parameters():
            mask = torch.rand_like(param) < mutation_rate
            noise = torch.randn_like(param) * mutation_std
            param[mask] += noise[mask]
    return mutated


def ball_roll(model, dataloader, device='cpu', num_steps=10, lr=0.01):
    """⚽ Ball mode: Roll downhill using gradient descent"""
    rolled = copy.deepcopy(model)
    optimizer = torch.optim.SGD(rolled.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()
    
    for _ in range(num_steps):
        rolled.train()
        for a, b, target in dataloader:
            a, b, target = a.to(device), b.to(device), target.to(device)
            optimizer.zero_grad()
            logits = rolled(a, b)
            loss = criterion(logits, target)
            loss.backward()
            optimizer.step()
            break
    
    return rolled


def drone_spread(population, spread_factor=0.5):
    """🛸 Drone mode: Spread out systematically"""
    center_weights = {}
    for name, param in population[0].named_parameters():
        center_weights[name] = torch.zeros_like(param)
        for model in population:
            center_weights[name] += dict(model.named_parameters())[name]
        center_weights[name] /= len(population)
    
    spread_models = []
    for model in population[:len(population)//4]:
        spread_model = copy.deepcopy(model)
        with torch.no_grad():
            for name, param in spread_model.named_parameters():
                direction = param - center_weights[name]
                param += spread_factor * direction
        spread_models.append(spread_model)
    
    return spread_models


def quantum_teleport(model, teleport_distance=1.0):
    """🌌 Quantum mode: Teleport to unexplored regions"""
    teleported = copy.deepcopy(model)
    with torch.no_grad():
        for param in teleported.parameters():
            jump = torch.randn_like(param) * teleport_distance
            param += jump
    return teleported


def psychic_mutate(model, collective_map, mutation_rate=0.1, mutation_std=0.05, psychic_strength=0.5):
    """🧠 Psychic mode: Mutate using collective wisdom"""
    mutated = copy.deepcopy(model)
    
    with torch.no_grad():
        for name, param in mutated.named_parameters():
            if name in collective_map:
                mask = torch.rand_like(param) < mutation_rate
                random_noise = torch.randn_like(param) * mutation_std
                collective_direction = collective_map[name]
                psychic_nudge = -collective_direction * mutation_std
                combined_mutation = (1 - psychic_strength) * random_noise + psychic_strength * psychic_nudge
                param[mask] += combined_mutation[mask]
    
    return mutated


def spawn_from_flag(flag: Flag, offset_std=0.1):
    """🚩 Spawn explorer near a flag"""
    explorer = copy.deepcopy(flag.model)
    with torch.no_grad():
        for param in explorer.parameters():
            offset = torch.randn_like(param) * offset_std
            param += offset
    flag.explorers_spawned += 1
    return explorer


def should_plant_flag(model, dataloader, device='cpu', grad_threshold=0.01, fitness_threshold=0.20):
    """Check if we should plant a flag here"""
    fitness = evaluate_fitness(model, dataloader, device)
    grad_norm = compute_gradient_norm(model, dataloader, device)
    
    # Plant flag if: good fitness AND low gradient (converged)
    return fitness >= fitness_threshold and grad_norm < grad_threshold


def create_random_model(modulus, num_heads, num_layers, device='cpu'):
    """Create a model with random initialization"""
    return LANNAformer(
        modulus=modulus,
        num_heads=num_heads,
        num_layers=num_layers,
        dropout=0.0,
        use_mlp=True
    ).to(device)


def main():
    parser = argparse.ArgumentParser(description='Ultimate Lizard Cartographers')
    parser.add_argument('--population-size', type=int, default=20, help='Population size')
    parser.add_argument('--generations', type=int, default=500, help='Number of generations')
    parser.add_argument('--elite-size', type=int, default=5, help='Number of elites')
    args = parser.parse_args()
    
    print("🦎🚩🧠⚽🛸🌌 ULTIMATE LIZARD CARTOGRAPHERS")
    print("=" * 70)
    print(f"Population size: {args.population_size}")
    print(f"Generations: {args.generations}")
    print(f"Elite size: {args.elite_size}")
    print("=" * 70)
    print()
    print("ALL THE SUPERPOWERS:")
    print("  🦎 Lizard mode - Random mutations")
    print("  ⚽ Ball mode - Gradient descent")
    print("  🛸 Drone mode - Systematic survey")
    print("  🌌 Quantum mode - Teleportation")
    print("  🧠 Psychic network - Shared gradients")
    print("  💫 Coherence awareness - Adaptive strategy")
    print("  🚩 Flag planting - Multi-scale search")
    print()
    print("GOAL: FIND THE 89% BASIN! 🎯")
    print("=" * 70)
    print()
    
    # Setup
    MODULUS = 16
    NUM_HEADS = 4
    NUM_LAYERS = 2
    BATCH_SIZE = 32
    device = 'cpu'
    
    # Load data
    train_dataset = ModularAdditionDataset(modulus=MODULUS, train=True)
    test_dataset = ModularAdditionDataset(modulus=MODULUS, train=False)
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)
    
    print(f"Train set: {len(train_dataset)} pairs")
    print(f"Test set: {len(test_dataset)} pairs")
    print()
    
    # Initialize population
    print("🌱 Creating initial population...")
    population = [
        create_random_model(MODULUS, NUM_HEADS, NUM_LAYERS, device)
        for _ in range(args.population_size)
    ]
    
    # Flag registry
    flags: List[Flag] = []
    
    # Evolution loop
    print("🚀 Starting ultimate exploration...")
    print("=" * 70)
    print()
    
    best_fitness_ever = 0.0
    best_model_ever = None
    history = {
        'best_fitness': [],
        'mean_fitness': [],
        'coherence': [],
        'num_flags': [],
        'mode_usage': {'lizard': 0, 'ball': 0, 'drone': 0, 'quantum': 0, 'psychic': 0, 'flag_spawn': 0}
    }
    
    for generation in tqdm(range(args.generations), desc="Generations"):
        # Build psychic network
        collective_map, fitnesses = build_collective_map(population, train_loader, device)
        coherence = compute_coherence(population, collective_map, train_loader, device)
        
        best_fitness = max(fitnesses)
        mean_fitness = np.mean(fitnesses)
        
        history['best_fitness'].append(best_fitness)
        history['mean_fitness'].append(mean_fitness)
        history['coherence'].append(coherence)
        history['num_flags'].append(len(flags))
        
        if best_fitness > best_fitness_ever:
            best_fitness_ever = best_fitness
            best_idx = fitnesses.index(best_fitness)
            best_model_ever = copy.deepcopy(population[best_idx])
        
        # Check for flag planting
        for i, model in enumerate(population):
            if should_plant_flag(model, test_loader, device):
                fitness = fitnesses[i]
                # Only plant if better than existing flags
                if not flags or fitness > max(f.fitness for f in flags):
                    flag = Flag(model, fitness, generation)
                    flags.append(flag)
                    tqdm.write(f"🚩 FLAG PLANTED! Gen {generation}, Fitness: {fitness:.3f}")
        
        if generation % 10 == 0 or generation == args.generations - 1:
            tqdm.write(f"\nGen {generation:3d} | Best: {best_fitness:.3f} | Mean: {mean_fitness:.3f} | Coherence: {coherence:.3f} | Flags: {len(flags)} | Best Ever: {best_fitness_ever:.3f}")
        
        # Selection: Keep elites
        sorted_indices = np.argsort(fitnesses)[::-1]
        elites = [population[i] for i in sorted_indices[:args.elite_size]]
        
        # Adaptive strategy based on coherence
        if coherence > 0.5:
            # High coherence: Trust collective, use ball mode more
            ball_rate = 0.4
            psychic_rate = 0.3
            lizard_rate = 0.2
            flag_spawn_rate = 0.1
        elif coherence > 0.3:
            # Medium coherence: Balanced
            ball_rate = 0.3
            psychic_rate = 0.2
            lizard_rate = 0.3
            flag_spawn_rate = 0.2
        else:
            # Low coherence: Explore more
            lizard_rate = 0.3
            quantum_rate = 0.2
            ball_rate = 0.2
            psychic_rate = 0.0  # Don't trust psychic when incoherent!
            flag_spawn_rate = 0.3
        
        # Create next generation
        next_generation = elites.copy()
        remaining = args.population_size - args.elite_size
        
        for _ in range(remaining):
            mode_choice = np.random.random()
            parent_idx = np.random.choice(sorted_indices[:args.elite_size * 2])
            parent = population[parent_idx]
            
            if mode_choice < flag_spawn_rate and flags:
                # 🚩 Spawn from best flag
                best_flag = max(flags, key=lambda f: f.fitness)
                child = spawn_from_flag(best_flag, offset_std=0.1)
                history['mode_usage']['flag_spawn'] += 1
            
            elif mode_choice < flag_spawn_rate + ball_rate:
                # ⚽ Ball mode
                child = ball_roll(parent, train_loader, device, num_steps=10, lr=0.01)
                history['mode_usage']['ball'] += 1
            
            elif mode_choice < flag_spawn_rate + ball_rate + psychic_rate:
                # 🧠 Psychic mode
                psychic_strength = min(0.8, coherence + 0.3)  # Higher when coherent
                child = psychic_mutate(parent, collective_map, psychic_strength=psychic_strength)
                history['mode_usage']['psychic'] += 1
            
            elif mode_choice < flag_spawn_rate + ball_rate + psychic_rate + lizard_rate:
                # 🦎 Lizard mode
                child = lizard_mutate(parent)
                history['mode_usage']['lizard'] += 1
            
            else:
                # 🌌 Quantum mode
                child = quantum_teleport(parent, teleport_distance=0.5)
                history['mode_usage']['quantum'] += 1
            
            next_generation.append(child)
        
        population = next_generation
    
    print()
    print("=" * 70)
    print("✨ Ultimate exploration complete!")
    print()
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = Path(__file__).parent / f"mod16_ultimate_{timestamp}"
    results_dir.mkdir(exist_ok=True)
    
    if best_model_ever is not None:
        torch.save(best_model_ever.state_dict(), results_dir / "best_model.pt")
    
    # Save flags
    flag_data = [{'fitness': f.fitness, 'generation': f.generation, 'spawned': f.explorers_spawned} for f in flags]
    
    with open(results_dir / "evolution_history.json", 'w') as f:
        json.dump(history, f, indent=2)
    
    with open(results_dir / "flags.json", 'w') as f:
        json.dump(flag_data, f, indent=2)
    
    with open(results_dir / "config.json", 'w') as f:
        json.dump({
            'modulus': MODULUS,
            'num_heads': NUM_HEADS,
            'num_layers': NUM_LAYERS,
            'population_size': args.population_size,
            'generations': args.generations,
            'elite_size': args.elite_size,
            'best_fitness': float(best_fitness_ever),
            'final_coherence': float(history['coherence'][-1]),
            'num_flags_planted': len(flags),
            'mode_usage': history['mode_usage']
        }, f, indent=2)
    
    print(f"Best fitness achieved: {best_fitness_ever:.3f}")
    print(f"Final coherence: {history['coherence'][-1]:.3f}")
    print(f"Flags planted: {len(flags)}")
    print()
    
    if flags:
        print("🚩 FLAG SUMMARY:")
        for i, flag in enumerate(sorted(flags, key=lambda f: -f.fitness)):
            print(f"  Flag {i+1}: {flag.fitness:.3f} (gen {flag.generation}, spawned {flag.explorers_spawned})")
        print()
    
    print("Mode usage:")
    total_uses = sum(history['mode_usage'].values())
    for mode, count in sorted(history['mode_usage'].items(), key=lambda x: -x[1]):
        pct = 100 * count / total_uses if total_uses > 0 else 0
        print(f"  {mode:12s}: {count:5d} uses ({pct:5.1f}%)")
    print()
    
    if best_fitness_ever > 0.95:
        print("🎉🎉🎉 WE FOUND IT! >95% accuracy!")
        print("THE ULTIMATE LIZARDS SUCCEEDED!")
    elif best_fitness_ever > 0.89:
        print("🎯 SO CLOSE! >89% accuracy!")
        print("We're in the right neighborhood!")
    elif best_fitness_ever > 0.85:
        print("📈 Getting warmer! >85% accuracy!")
    else:
        print("🤔 Still searching... but we learned a lot!")
    
    print()
    print(f"Results saved to: {results_dir}")
    print()
    print("=" * 70)
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🦎🚩🧠⚽🛸🌌 'The ULTIMATE basin exploration algorithm!'")


if __name__ == "__main__":
    main()

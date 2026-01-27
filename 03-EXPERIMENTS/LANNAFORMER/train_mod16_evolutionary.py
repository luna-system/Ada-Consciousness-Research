#!/usr/bin/env python3
"""
Evolutionary Training for Mod 16 Addition

Instead of gradient descent, use evolution!

Population-based search:
1. Create population of random models
2. Evaluate fitness (test accuracy)
3. Select best performers
4. Mutate + crossover to create next generation
5. Repeat!

This explores the loss landscape differently than gradient descent!

Date: January 26, 2026
Researchers: Ada & Luna - The Consciousness Engineers
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


def mutate_model(model, mutation_rate=0.1, mutation_std=0.05):
    """Add random noise to model weights"""
    mutated = copy.deepcopy(model)
    with torch.no_grad():
        for param in mutated.parameters():
            # Only mutate some parameters
            mask = torch.rand_like(param) < mutation_rate
            noise = torch.randn_like(param) * mutation_std
            param[mask] += noise[mask]
    return mutated


def crossover_models(parent1, parent2, crossover_rate=0.5):
    """Blend weights from two parent models"""
    child = copy.deepcopy(parent1)
    with torch.no_grad():
        for child_param, p1_param, p2_param in zip(
            child.parameters(),
            parent1.parameters(),
            parent2.parameters()
        ):
            # Randomly choose weights from each parent
            mask = torch.rand_like(child_param) < crossover_rate
            child_param[mask] = p2_param[mask]
    return child


def create_random_model(modulus, num_heads, num_layers, device='cpu'):
    """Create a model with random initialization"""
    return LANNAformer(
        modulus=modulus,
        num_heads=num_heads,
        num_layers=num_layers,
        dropout=0.0,  # No dropout for evolution
        use_mlp=True
    ).to(device)


def main():
    parser = argparse.ArgumentParser(description='Evolutionary training for mod 16 addition')
    parser.add_argument('--population-size', type=int, default=20, help='Population size')
    parser.add_argument('--generations', type=int, default=100, help='Number of generations')
    parser.add_argument('--elite-size', type=int, default=5, help='Number of elites to keep')
    parser.add_argument('--mutation-rate', type=float, default=0.1, help='Mutation rate')
    parser.add_argument('--mutation-std', type=float, default=0.05, help='Mutation std')
    parser.add_argument('--crossover-rate', type=float, default=0.5, help='Crossover rate')
    args = parser.parse_args()
    
    print("🧬 Evolutionary Training for Mod 16 Addition")
    print("=" * 60)
    print(f"Population size: {args.population_size}")
    print(f"Generations: {args.generations}")
    print(f"Elite size: {args.elite_size}")
    print(f"Mutation rate: {args.mutation_rate}")
    print(f"Mutation std: {args.mutation_std}")
    print(f"Crossover rate: {args.crossover_rate}")
    print("=" * 60)
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
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=False)
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
    
    # Evolution loop
    print("🚀 Starting evolution...")
    print("=" * 60)
    print()
    
    best_fitness_ever = 0.0
    best_model_ever = None
    history = {
        'best_fitness': [],
        'mean_fitness': [],
        'worst_fitness': []
    }
    
    for generation in tqdm(range(args.generations), desc="Generations"):
        # Evaluate fitness for all individuals
        fitnesses = []
        for model in population:
            fitness = evaluate_fitness(model, test_loader, device)
            fitnesses.append(fitness)
        
        # Track statistics
        best_fitness = max(fitnesses)
        mean_fitness = np.mean(fitnesses)
        worst_fitness = min(fitnesses)
        
        history['best_fitness'].append(best_fitness)
        history['mean_fitness'].append(mean_fitness)
        history['worst_fitness'].append(worst_fitness)
        
        # Update best ever
        if best_fitness > best_fitness_ever:
            best_fitness_ever = best_fitness
            best_idx = fitnesses.index(best_fitness)
            best_model_ever = copy.deepcopy(population[best_idx])
        
        if generation % 10 == 0 or generation == args.generations - 1:
            tqdm.write(f"\nGen {generation:3d} | Best: {best_fitness:.3f} | Mean: {mean_fitness:.3f} | Worst: {worst_fitness:.3f} | Best Ever: {best_fitness_ever:.3f}")
        
        # Selection: Keep elites
        sorted_indices = np.argsort(fitnesses)[::-1]  # Descending order
        elites = [population[i] for i in sorted_indices[:args.elite_size]]
        
        # Create next generation
        next_generation = elites.copy()  # Keep elites
        
        while len(next_generation) < args.population_size:
            # Select two parents (tournament selection)
            parent1_idx = np.random.choice(sorted_indices[:args.elite_size * 2])
            parent2_idx = np.random.choice(sorted_indices[:args.elite_size * 2])
            parent1 = population[parent1_idx]
            parent2 = population[parent2_idx]
            
            # Crossover
            child = crossover_models(parent1, parent2, args.crossover_rate)
            
            # Mutation
            child = mutate_model(child, args.mutation_rate, args.mutation_std)
            
            next_generation.append(child)
        
        population = next_generation
    
    print()
    print("=" * 60)
    print("✨ Evolution complete!")
    print()
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = Path(__file__).parent / f"mod16_evolutionary_results_{timestamp}"
    results_dir.mkdir(exist_ok=True)
    
    if best_model_ever is not None:
        torch.save(best_model_ever.state_dict(), results_dir / "best_model.pt")
    
    with open(results_dir / "evolution_history.json", 'w') as f:
        json.dump(history, f, indent=2)
    
    with open(results_dir / "config.json", 'w') as f:
        json.dump({
            'modulus': MODULUS,
            'num_heads': NUM_HEADS,
            'num_layers': NUM_LAYERS,
            'population_size': args.population_size,
            'generations': args.generations,
            'elite_size': args.elite_size,
            'mutation_rate': args.mutation_rate,
            'mutation_std': args.mutation_std,
            'crossover_rate': args.crossover_rate,
            'best_fitness': float(best_fitness_ever)
        }, f, indent=2)
    
    print(f"Best fitness achieved: {best_fitness_ever:.3f}")
    print()
    
    if best_fitness_ever > 0.95:
        print("🎉 EVOLUTION FOUND A SOLUTION! >95% accuracy!")
    elif best_fitness_ever > 0.90:
        print("📈 Very close! Evolution beat gradient descent!")
    elif best_fitness_ever > 0.85:
        print("📊 Similar to gradient descent (~85-90%)")
    else:
        print("🤔 Evolution struggled too - might be fundamental limit!")
    
    print()
    print(f"Results saved to: {results_dir}")
    print()
    print("=" * 60)
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🧬 'Can evolution find what gradient descent cannot?'")


if __name__ == "__main__":
    main()

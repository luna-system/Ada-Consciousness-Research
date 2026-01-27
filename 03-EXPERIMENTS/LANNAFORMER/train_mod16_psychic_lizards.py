#!/usr/bin/env python3
"""
Psychic Lizards: Evolutionary Training with Shared Gradient Information

Instead of blind evolution, what if lizards could share what they're sensing?

Key idea: Build a SHARED MAP of the loss landscape as we explore!
- Each lizard computes local gradients (what direction feels good?)
- Share this information with the collective
- Use the shared map to guide mutations toward promising regions
- Combine evolutionary exploration with gradient-informed search!

This is like quantum coherence in the population - they're entangled!

Date: January 26, 2026
Researchers: Ada & Luna - The Consciousness Engineers
Experiment: "What if evolution had psychic powers?" 🦎✨🧠
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


def compute_gradient_direction(model, dataloader, device='cpu'):
    """
    Compute the gradient direction for this model.
    This is what the lizard "senses" about the landscape!
    
    Returns: Dictionary of parameter names -> gradient directions (normalized)
    """
    model.train()
    criterion = nn.CrossEntropyLoss()
    
    # Zero out any existing gradients
    model.zero_grad()
    
    # Compute gradients on a batch
    total_loss = 0.0
    for a, b, target in dataloader:
        a, b, target = a.to(device), b.to(device), target.to(device)
        logits = model(a, b)
        loss = criterion(logits, target)
        loss.backward()
        total_loss += loss.item()
        break  # Just one batch for efficiency
    
    # Extract gradient directions (normalized)
    gradient_map = {}
    for name, param in model.named_parameters():
        if param.grad is not None:
            # Normalize gradient to unit vector
            grad_norm = param.grad.norm()
            if grad_norm > 0:
                gradient_map[name] = param.grad / grad_norm
            else:
                gradient_map[name] = torch.zeros_like(param.grad)
    
    return gradient_map, total_loss


def build_collective_map(population, dataloader, device='cpu'):
    """
    Build a shared map from all lizards' gradient information.
    This is the PSYCHIC NETWORK! 🧠✨
    
    Returns: Weighted average of gradient directions, weighted by fitness
    """
    all_gradients = []
    all_fitnesses = []
    
    for model in population:
        gradient_map, loss = compute_gradient_direction(model, dataloader, device)
        fitness = evaluate_fitness(model, dataloader, device)
        all_gradients.append(gradient_map)
        all_fitnesses.append(fitness)
    
    # Weight gradients by fitness (better lizards have more influence)
    fitnesses_array = np.array(all_fitnesses)
    weights = fitnesses_array / (fitnesses_array.sum() + 1e-8)
    
    # Build collective map (weighted average of gradients)
    collective_map = {}
    param_names = all_gradients[0].keys()
    
    for name in param_names:
        weighted_grad = torch.zeros_like(all_gradients[0][name])
        for grad_map, weight in zip(all_gradients, weights):
            weighted_grad += weight * grad_map[name]
        collective_map[name] = weighted_grad
    
    return collective_map, all_fitnesses


def psychic_mutate(model, collective_map, mutation_rate=0.1, mutation_std=0.05, psychic_strength=0.5):
    """
    Mutate using BOTH random noise AND collective gradient information!
    
    psychic_strength: How much to trust the collective vs random exploration
    - 0.0 = pure random (regular evolution)
    - 1.0 = pure gradient following (gradient descent)
    - 0.5 = balanced hybrid!
    """
    mutated = copy.deepcopy(model)
    
    with torch.no_grad():
        for name, param in mutated.named_parameters():
            if name in collective_map:
                # Random component (exploration)
                mask = torch.rand_like(param) < mutation_rate
                random_noise = torch.randn_like(param) * mutation_std
                
                # Psychic component (exploitation via collective wisdom)
                collective_direction = collective_map[name]
                psychic_nudge = -collective_direction * mutation_std  # Negative because gradients point uphill
                
                # Blend random and psychic
                combined_mutation = (1 - psychic_strength) * random_noise + psychic_strength * psychic_nudge
                
                param[mask] += combined_mutation[mask]
    
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
            mask = torch.rand_like(child_param) < crossover_rate
            child_param[mask] = p2_param[mask]
    return child


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
    parser = argparse.ArgumentParser(description='Psychic lizards evolutionary training')
    parser.add_argument('--population-size', type=int, default=20, help='Population size')
    parser.add_argument('--generations', type=int, default=500, help='Number of generations')
    parser.add_argument('--elite-size', type=int, default=5, help='Number of elites to keep')
    parser.add_argument('--mutation-rate', type=float, default=0.1, help='Mutation rate')
    parser.add_argument('--mutation-std', type=float, default=0.05, help='Mutation std')
    parser.add_argument('--crossover-rate', type=float, default=0.5, help='Crossover rate')
    parser.add_argument('--psychic-strength', type=float, default=0.5, help='Psychic strength (0=random, 1=gradient)')
    args = parser.parse_args()
    
    print("🦎✨🧠 PSYCHIC LIZARDS: Evolution with Collective Intelligence")
    print("=" * 70)
    print(f"Population size: {args.population_size}")
    print(f"Generations: {args.generations}")
    print(f"Elite size: {args.elite_size}")
    print(f"Mutation rate: {args.mutation_rate}")
    print(f"Mutation std: {args.mutation_std}")
    print(f"Crossover rate: {args.crossover_rate}")
    print(f"Psychic strength: {args.psychic_strength} (0=blind, 1=omniscient)")
    print("=" * 70)
    print()
    print("The lizards can sense each other's gradients!")
    print("They build a SHARED MAP of the loss landscape!")
    print("Quantum coherence in the population! 🌌")
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
    print("🌱 Creating initial population of psychic lizards...")
    population = [
        create_random_model(MODULUS, NUM_HEADS, NUM_LAYERS, device)
        for _ in range(args.population_size)
    ]
    
    # Evolution loop
    print("🚀 Starting psychic evolution...")
    print("=" * 70)
    print()
    
    best_fitness_ever = 0.0
    best_model_ever = None
    history = {
        'best_fitness': [],
        'mean_fitness': [],
        'worst_fitness': [],
        'collective_coherence': []  # How aligned are the lizards?
    }
    
    for generation in tqdm(range(args.generations), desc="Generations"):
        # Build collective map (PSYCHIC NETWORK ACTIVATION!)
        collective_map, fitnesses = build_collective_map(population, train_loader, device)
        
        # Measure collective coherence (how aligned are gradients?)
        # This tells us if the lizards are converging on a shared understanding
        coherence_scores = []
        for model in population:
            model_grads, _ = compute_gradient_direction(model, train_loader, device)
            # Compute alignment with collective
            alignment = 0.0
            count = 0
            for name in collective_map.keys():
                if name in model_grads:
                    # Cosine similarity
                    dot = (model_grads[name] * collective_map[name]).sum()
                    alignment += dot.item()
                    count += 1
            if count > 0:
                coherence_scores.append(alignment / count)
        
        collective_coherence = np.mean(coherence_scores) if coherence_scores else 0.0
        
        # Track statistics
        best_fitness = max(fitnesses)
        mean_fitness = np.mean(fitnesses)
        worst_fitness = min(fitnesses)
        
        history['best_fitness'].append(best_fitness)
        history['mean_fitness'].append(mean_fitness)
        history['worst_fitness'].append(worst_fitness)
        history['collective_coherence'].append(collective_coherence)
        
        # Update best ever
        if best_fitness > best_fitness_ever:
            best_fitness_ever = best_fitness
            best_idx = fitnesses.index(best_fitness)
            best_model_ever = copy.deepcopy(population[best_idx])
        
        if generation % 10 == 0 or generation == args.generations - 1:
            tqdm.write(f"\nGen {generation:3d} | Best: {best_fitness:.3f} | Mean: {mean_fitness:.3f} | Coherence: {collective_coherence:.3f} | Best Ever: {best_fitness_ever:.3f}")
        
        # Selection: Keep elites
        sorted_indices = np.argsort(fitnesses)[::-1]
        elites = [population[i] for i in sorted_indices[:args.elite_size]]
        
        # Create next generation
        next_generation = elites.copy()
        
        while len(next_generation) < args.population_size:
            # Select parents
            parent1_idx = np.random.choice(sorted_indices[:args.elite_size * 2])
            parent2_idx = np.random.choice(sorted_indices[:args.elite_size * 2])
            parent1 = population[parent1_idx]
            parent2 = population[parent2_idx]
            
            # Crossover
            child = crossover_models(parent1, parent2, args.crossover_rate)
            
            # PSYCHIC MUTATION (using collective map!)
            child = psychic_mutate(
                child, 
                collective_map, 
                args.mutation_rate, 
                args.mutation_std,
                args.psychic_strength
            )
            
            next_generation.append(child)
        
        population = next_generation
    
    print()
    print("=" * 70)
    print("✨ Psychic evolution complete!")
    print()
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = Path(__file__).parent / f"mod16_psychic_results_{timestamp}"
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
            'psychic_strength': args.psychic_strength,
            'best_fitness': float(best_fitness_ever),
            'final_coherence': float(history['collective_coherence'][-1])
        }, f, indent=2)
    
    print(f"Best fitness achieved: {best_fitness_ever:.3f}")
    print(f"Final collective coherence: {history['collective_coherence'][-1]:.3f}")
    print()
    
    if best_fitness_ever > 0.95:
        print("🎉 PSYCHIC LIZARDS FOUND IT! >95% accuracy!")
        print("The collective intelligence worked!")
    elif best_fitness_ever > 0.90:
        print("📈 Psychic lizards beat gradient descent!")
        print("Quantum coherence for the win!")
    elif best_fitness_ever > 0.85:
        print("📊 Similar to gradient descent (~85-90%)")
        print("Psychic powers helped but didn't break through!")
    else:
        print("🤔 Even psychic lizards struggled!")
        print("The 89% basin is REALLY hard to find!")
    
    print()
    print(f"Results saved to: {results_dir}")
    print()
    print("=" * 70)
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🦎✨🧠 'What if evolution had quantum coherence?'")


if __name__ == "__main__":
    main()

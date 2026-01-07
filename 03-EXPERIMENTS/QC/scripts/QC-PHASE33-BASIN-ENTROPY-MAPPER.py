#!/usr/bin/env python3
"""
QC-PHASE33: Basin Entropy Mapper
Identifies the φ-optimized "accretion ring" for maximum entropy key generation.

This script:
1. Samples the model across diverse prompts
2. Computes CI (Crystal Intelligence) for each state
3. Measures Shannon entropy of token distributions
4. Identifies the φ-zone: 0.24 < CI < 0.33 with maximum entropy
"""

import json
import numpy as np
import torch
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import warnings

warnings.filterwarnings("ignore")

# Configuration
MODEL_PATH = None  # Will use baseline or specify adapter
BASE_MODEL = "LiquidAI/LFM2-1.2B"
OUTPUT_DIR = Path(__file__).parent.parent / "results"
NUM_PROMPTS = 100  # Number of prompts to sample
PHI_ZONE_MIN = 0.24
PHI_ZONE_MAX = 0.33

# Diverse prompt set for basin exploration
PROMPT_TEMPLATES = [
    # Existential
    "What is the nature of {}?",
    "How does {} relate to consciousness?",
    "Explain {} in simple terms.",
    
    # Technical
    "Define {} formally.",
    "What are the key properties of {}?",
    "Describe the structure of {}.",
    
    # Abstract
    "The essence of {} is",
    "{} emerges from",
    "Consider {} deeply:",
    
    # Uncertainty
    "What remains uncertain about {}?",
    "The paradox of {} reveals",
    "Between {} and nothing lies",
]

PROMPT_TOPICS = [
    "consciousness", "reality", "time", "space", "entropy", "information",
    "pattern", "structure", "emergence", "complexity", "order", "chaos",
    "measurement", "observation", "uncertainty", "probability", "quantum",
    "attention", "awareness", "thought", "knowledge", "truth", "existence",
]


def load_model(adapter_path: str = None, device: str = "auto"):
    """Load model with optional adapter."""
    print(f"\n📥 Loading {BASE_MODEL}...")
    
    # Auto-detect device
    if device == "auto":
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
    
    # Load base model
    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        torch_dtype=torch.float32,
        device_map=None,
        trust_remote_code=True,
        attn_implementation="eager",
    )
    
    # Load adapter if specified
    if adapter_path:
        print(f"   Loading adapter from {adapter_path}...")
        model = PeftModel.from_pretrained(model, adapter_path)
    
    # Move to device
    if device != "cpu":
        model = model.to(device)
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    print(f"✅ Model loaded on {device}!")
    return model, tokenizer, device


def calculate_shannon_entropy(logits: torch.Tensor) -> float:
    """Calculate Shannon entropy of token probability distribution."""
    # Convert logits to probabilities
    probs = torch.softmax(logits, dim=-1)
    
    # Remove zero probabilities to avoid log(0)
    probs = probs[probs > 0]
    
    # Shannon entropy: H = -Σ p(x) log2(p(x))
    entropy = -torch.sum(probs * torch.log2(probs)).item()
    
    return entropy


def compute_ci(logits: torch.Tensor, top_k: int = 15) -> float:
    """
    Compute Crystal Intelligence (CI) metric.
    CI = density of top-k tokens in probability mass.
    Lower CI = more crystallized (focused on few tokens)
    Higher CI = more diffuse (spread across many tokens)
    """
    probs = torch.softmax(logits, dim=-1)
    top_probs, _ = torch.topk(probs, k=top_k)
    ci = top_probs.sum().item()
    return ci


def analyze_prompt(
    model,
    tokenizer,
    prompt: str,
    device: str
) -> Dict:
    """Analyze a single prompt for entropy and CI."""
    model.eval()
    
    # Tokenize
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
    if device != "cpu":
        inputs = {k: v.to(device) for k, v in inputs.items()}
    
    # Get logits
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits[0, -1, :]  # Last token logits
    
    # Calculate metrics
    entropy = calculate_shannon_entropy(logits)
    ci = compute_ci(logits)
    
    return {
        "prompt": prompt,
        "entropy": entropy,
        "ci": ci,
        "in_phi_zone": PHI_ZONE_MIN < ci < PHI_ZONE_MAX,
    }


def generate_prompts(num_prompts: int) -> List[str]:
    """Generate diverse prompts for basin exploration."""
    prompts = []
    np.random.seed(42)  # Reproducibility
    
    for _ in range(num_prompts):
        template = np.random.choice(PROMPT_TEMPLATES)
        topic = np.random.choice(PROMPT_TOPICS)
        prompts.append(template.format(topic))
    
    return prompts


def map_basin_entropy(
    model,
    tokenizer,
    device: str,
    num_prompts: int = NUM_PROMPTS
) -> Dict:
    """Map entropy across the basin landscape."""
    print(f"\n🗺️  Mapping Basin Entropy ({num_prompts} prompts)...")
    
    prompts = generate_prompts(num_prompts)
    results = []
    
    for i, prompt in enumerate(prompts, 1):
        if i % 10 == 0:
            print(f"   Progress: {i}/{num_prompts}")
        
        result = analyze_prompt(model, tokenizer, prompt, device)
        results.append(result)
    
    # Aggregate statistics
    entropies = [r["entropy"] for r in results]
    cis = [r["ci"] for r in results]
    phi_zone_results = [r for r in results if r["in_phi_zone"]]
    
    stats = {
        "total_prompts": num_prompts,
        "entropy": {
            "mean": float(np.mean(entropies)),
            "std": float(np.std(entropies)),
            "min": float(np.min(entropies)),
            "max": float(np.max(entropies)),
        },
        "ci": {
            "mean": float(np.mean(cis)),
            "std": float(np.std(cis)),
            "min": float(np.min(cis)),
            "max": float(np.max(cis)),
        },
        "phi_zone": {
            "count": len(phi_zone_results),
            "percentage": len(phi_zone_results) / num_prompts * 100,
            "avg_entropy": float(np.mean([r["entropy"] for r in phi_zone_results])) if phi_zone_results else 0,
        },
        "results": results,
    }
    
    return stats


def find_phi_zone_prompts(results: List[Dict], top_n: int = 20) -> List[Dict]:
    """Find the top-N prompts in the φ-zone with highest entropy."""
    phi_zone = [r for r in results if r["in_phi_zone"]]
    phi_zone_sorted = sorted(phi_zone, key=lambda x: x["entropy"], reverse=True)
    return phi_zone_sorted[:top_n]


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Map basin entropy for φ-cryptography")
    parser.add_argument("--model", "-m", default=None, help="Adapter path (optional)")
    parser.add_argument("--num-prompts", "-n", type=int, default=NUM_PROMPTS, help="Number of prompts to sample")
    parser.add_argument("--device", "-d", default="auto", help="Device (auto/cpu/cuda:0)")
    
    args = parser.parse_args()
    
    # Load model
    model, tokenizer, device = load_model(args.model, args.device)
    
    # Map basin
    stats = map_basin_entropy(model, tokenizer, device, args.num_prompts)
    
    # Find φ-zone prompts
    phi_prompts = find_phi_zone_prompts(stats["results"])
    
    # Save results
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    output_file = OUTPUT_DIR / f"basin_entropy_map_{timestamp}.json"
    with open(output_file, "w") as f:
        json.dump(stats, f, indent=2)
    
    phi_file = OUTPUT_DIR / f"phi_zone_prompts_{timestamp}.json"
    with open(phi_file, "w") as f:
        json.dump(phi_prompts, f, indent=2)
    
    # Print summary
    print(f"\n{'='*70}")
    print("📊 BASIN ENTROPY MAPPING RESULTS")
    print(f"{'='*70}")
    print(f"\n📈 Entropy Statistics:")
    print(f"   Mean: {stats['entropy']['mean']:.4f}")
    print(f"   Std:  {stats['entropy']['std']:.4f}")
    print(f"   Range: [{stats['entropy']['min']:.4f}, {stats['entropy']['max']:.4f}]")
    
    print(f"\n🔮 CI Statistics:")
    print(f"   Mean: {stats['ci']['mean']:.4f}")
    print(f"   Std:  {stats['ci']['std']:.4f}")
    print(f"   Range: [{stats['ci']['min']:.4f}, {stats['ci']['max']:.4f}]")
    
    print(f"\n✨ φ-Zone Analysis:")
    print(f"   Prompts in zone: {stats['phi_zone']['count']}/{stats['total_prompts']} ({stats['phi_zone']['percentage']:.1f}%)")
    print(f"   Avg entropy in φ-zone: {stats['phi_zone']['avg_entropy']:.4f}")
    
    if phi_prompts:
        print(f"\n🎯 Top φ-Zone Prompts (Highest Entropy):")
        for i, p in enumerate(phi_prompts[:5], 1):
            print(f"   {i}. [{p['ci']:.3f}] H={p['entropy']:.2f}: {p['prompt'][:60]}...")
    
    print(f"\n💾 Results saved:")
    print(f"   {output_file}")
    print(f"   {phi_file}")
    print(f"\n✅ Basin entropy mapping complete!")


if __name__ == "__main__":
    main()

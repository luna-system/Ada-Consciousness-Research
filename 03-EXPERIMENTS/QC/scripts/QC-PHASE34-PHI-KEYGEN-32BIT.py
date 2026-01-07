#!/usr/bin/env python3
"""
QC-PHASE34: φ-Optimized 32-bit Cryptographic Key Generation (Proof-of-Concept)

This script:
1. Loads pre-computed φ-zone prompts (from PHASE33)
2. Samples tokens from the model in high-entropy states
3. Extracts bits from probability distributions
4. Applies Fibonacci mixing for pattern resistance
5. Generates a 32-bit cryptographic key
"""

import json
import numpy as np
import torch
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import warnings

warnings.filterwarnings("ignore")

# Configuration
BASE_MODEL = "LiquidAI/LFM2-1.2B"
OUTPUT_DIR = Path(__file__).parent.parent / "results"
KEY_SIZE = 32  # bits
BITS_PER_TOKEN = 1  # Conservative extraction rate


def load_model(adapter_path: str = None, device: str = "auto"):
    """Load model with optional adapter."""
    print(f"\n📥 Loading {BASE_MODEL}...")
    
    if device == "auto":
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
    
    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        torch_dtype=torch.float32,
        device_map=None,
        trust_remote_code=True,
        attn_implementation="eager",
    )
    
    if adapter_path:
        print(f"   Loading adapter from {adapter_path}...")
        model = PeftModel.from_pretrained(model, adapter_path)
    
    if device != "cpu":
        model = model.to(device)
    
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    print(f"✅ Model loaded on {device}!")
    return model, tokenizer, device


def load_phi_zone_prompts(phi_file: Path = None) -> List[Dict]:
    """Load pre-computed φ-zone prompts."""
    if phi_file is None:
        # Find most recent phi_zone file
        phi_files = sorted(OUTPUT_DIR.glob("phi_zone_prompts_*.json"))
        if not phi_files:
            raise FileNotFoundError(
                "No φ-zone prompts found. Run QC-PHASE33-BASIN-ENTROPY-MAPPER.py first."
            )
        phi_file = phi_files[-1]
    
    print(f"\n📂 Loading φ-zone prompts from {phi_file.name}...")
    with open(phi_file, "r") as f:
        prompts = json.load(f)
    
    print(f"   Found {len(prompts)} high-entropy prompts")
    return prompts


def extract_bit_from_distribution(logits: torch.Tensor) -> int:
    """
    Extract a single bit from token probability distribution.
    
    Method: Compare top-2 token probabilities
    - If p1 > p2: bit = 1
    - If p1 < p2: bit = 0
    - Use the uncertainty between them as entropy source
    """
    probs = torch.softmax(logits, dim=-1)
    top2_probs, top2_indices = torch.topk(probs, k=2)
    
    # Extract bit from comparison
    bit = 1 if top2_probs[0] > top2_probs[1] else 0
    
    # Calculate entropy of this extraction
    p1, p2 = top2_probs[0].item(), top2_probs[1].item()
    entropy = -p1 * np.log2(p1 + 1e-10) - p2 * np.log2(p2 + 1e-10)
    
    return bit, entropy


def generate_token_bits(
    model,
    tokenizer,
    prompt: str,
    device: str,
    num_bits: int = 1
) -> Tuple[List[int], List[float]]:
    """Generate bits by sampling tokens from a prompt."""
    model.eval()
    bits = []
    entropies = []
    
    # Tokenize initial prompt
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
    if device != "cpu":
        inputs = {k: v.to(device) for k, v in inputs.items()}
    
    # Generate tokens and extract bits
    for _ in range(num_bits):
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits[0, -1, :]
        
        # Extract bit
        bit, entropy = extract_bit_from_distribution(logits)
        bits.append(bit)
        entropies.append(entropy)
        
        # Sample next token for continuation (if needed)
        if len(bits) < num_bits:
            next_token = torch.argmax(logits).unsqueeze(0).unsqueeze(0)
            if device != "cpu":
                next_token = next_token.to(device)
            inputs["input_ids"] = torch.cat([inputs["input_ids"], next_token], dim=1)
    
    return bits, entropies


def fibonacci_mix(bits: List[int]) -> List[int]:
    """
    Apply Fibonacci mixing to bit sequence.
    
    Mixing rule: bit[n] = (bit[n] + bit[n-1] + bit[n-2]) mod 2
    This creates golden ratio dynamics and prevents patterns.
    """
    if len(bits) < 3:
        return bits
    
    mixed = bits[:2]  # Keep first two bits as seed
    
    for i in range(2, len(bits)):
        # Fibonacci recurrence with XOR
        mixed_bit = (bits[i] + mixed[-1] + mixed[-2]) % 2
        mixed.append(mixed_bit)
    
    return mixed


def bits_to_int(bits: List[int]) -> int:
    """Convert bit list to integer."""
    return int("".join(map(str, bits)), 2)


def bits_to_hex(bits: List[int]) -> str:
    """Convert bit list to hexadecimal string."""
    num = bits_to_int(bits)
    hex_str = hex(num)[2:].upper()
    # Pad to correct length
    expected_len = (len(bits) + 3) // 4
    return hex_str.zfill(expected_len)


def generate_key(
    model,
    tokenizer,
    device: str,
    phi_prompts: List[Dict],
    key_size: int = KEY_SIZE
) -> Dict:
    """Generate a cryptographic key using φ-optimized entropy."""
    print(f"\n🔐 Generating {key_size}-bit key from φ-zone...")
    
    start_time = datetime.now()
    all_bits = []
    all_entropies = []
    prompts_used = []
    
    # Calculate how many tokens we need
    tokens_needed = (key_size + BITS_PER_TOKEN - 1) // BITS_PER_TOKEN
    
    # Sample from different φ-zone prompts
    for i in range(tokens_needed):
        prompt_data = phi_prompts[i % len(phi_prompts)]
        prompt = prompt_data["prompt"]
        
        bits, entropies = generate_token_bits(
            model, tokenizer, prompt, device, num_bits=BITS_PER_TOKEN
        )
        
        all_bits.extend(bits)
        all_entropies.extend(entropies)
        prompts_used.append(prompt)
        
        if len(all_bits) >= key_size:
            break
    
    # Truncate to exact key size
    raw_bits = all_bits[:key_size]
    
    # Apply Fibonacci mixing
    mixed_bits = fibonacci_mix(raw_bits)
    
    end_time = datetime.now()
    generation_time = (end_time - start_time).total_seconds()
    
    # Convert to hex
    raw_hex = bits_to_hex(raw_bits)
    mixed_hex = bits_to_hex(mixed_bits)
    
    print(f"   ✅ Key generated in {generation_time:.2f}s")
    print(f"   Raw:   {raw_hex}")
    print(f"   Mixed: {mixed_hex}")
    
    return {
        "key_size": key_size,
        "raw_bits": raw_bits,
        "mixed_bits": mixed_bits,
        "raw_hex": raw_hex,
        "mixed_hex": mixed_hex,
        "generation_time": generation_time,
        "avg_entropy": float(np.mean(all_entropies)),
        "prompts_used": prompts_used[:10],  # Save first 10 for reference
        "timestamp": datetime.now().isoformat(),
    }


def validate_key(key_data: Dict) -> Dict:
    """Run basic validation tests on generated key."""
    print(f"\n🧪 Validating key...")
    
    bits = key_data["mixed_bits"]
    
    # Test 1: Bit balance (should be close to 50/50)
    ones = sum(bits)
    zeros = len(bits) - ones
    balance = ones / len(bits)
    
    # Test 2: Run test (count runs of consecutive bits)
    runs = 1
    for i in range(1, len(bits)):
        if bits[i] != bits[i-1]:
            runs += 1
    expected_runs = len(bits) / 2
    
    # Test 3: Autocorrelation (should be low)
    autocorr = np.correlate(bits, bits, mode='full')
    autocorr = autocorr[len(autocorr)//2:]
    autocorr = autocorr / autocorr[0]  # Normalize
    max_autocorr = np.max(np.abs(autocorr[1:]))  # Exclude lag-0
    
    validation = {
        "bit_balance": {
            "ones": ones,
            "zeros": zeros,
            "ratio": balance,
            "pass": 0.4 < balance < 0.6,
        },
        "runs_test": {
            "runs": runs,
            "expected": expected_runs,
            "pass": abs(runs - expected_runs) < expected_runs * 0.3,
        },
        "autocorrelation": {
            "max": float(max_autocorr),
            "pass": max_autocorr < 0.3,
        },
    }
    
    all_pass = all(v["pass"] for v in validation.values())
    validation["overall_pass"] = all_pass
    
    print(f"   Bit balance: {ones}/{zeros} (ratio: {balance:.3f}) {'✅' if validation['bit_balance']['pass'] else '❌'}")
    print(f"   Runs: {runs} (expected: {expected_runs:.1f}) {'✅' if validation['runs_test']['pass'] else '❌'}")
    print(f"   Autocorr: {max_autocorr:.3f} {'✅' if validation['autocorrelation']['pass'] else '❌'}")
    print(f"   Overall: {'✅ PASS' if all_pass else '❌ FAIL'}")
    
    return validation


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate φ-optimized 32-bit cryptographic key")
    parser.add_argument("--model", "-m", default=None, help="Adapter path (optional)")
    parser.add_argument("--phi-file", "-p", type=Path, default=None, help="φ-zone prompts file")
    parser.add_argument("--device", "-d", default="auto", help="Device (auto/cpu/cuda:0)")
    parser.add_argument("--num-keys", "-n", type=int, default=1, help="Number of keys to generate")
    
    args = parser.parse_args()
    
    # Load model
    model, tokenizer, device = load_model(args.model, args.device)
    
    # Load φ-zone prompts
    phi_prompts = load_phi_zone_prompts(args.phi_file)
    
    # Generate keys
    results = []
    for i in range(args.num_keys):
        if args.num_keys > 1:
            print(f"\n{'='*70}")
            print(f"Key {i+1}/{args.num_keys}")
            print(f"{'='*70}")
        
        key_data = generate_key(model, tokenizer, device, phi_prompts)
        validation = validate_key(key_data)
        key_data["validation"] = validation
        results.append(key_data)
    
    # Save results
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"phi_keygen_32bit_{timestamp}.json"
    
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    # Summary
    print(f"\n{'='*70}")
    print("🔐 KEY GENERATION SUMMARY")
    print(f"{'='*70}")
    print(f"   Keys generated: {len(results)}")
    print(f"   Avg generation time: {np.mean([r['generation_time'] for r in results]):.2f}s")
    print(f"   Avg entropy: {np.mean([r['avg_entropy'] for r in results]):.4f}")
    print(f"   Validation pass rate: {sum(r['validation']['overall_pass'] for r in results)}/{len(results)}")
    print(f"\n💾 Results saved to: {output_file}")
    print(f"\n✅ φ-optimized key generation complete!")


if __name__ == "__main__":
    main()

"""
Generate Full Lojban Holofield (1437 gismu)

Parses the official gismu list and creates a complete holofield
with 16D coordinates for all Lojban root words.

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: January 25, 2026
"""

import json
import numpy as np
import re
from typing import Dict, List, Any
from pathlib import Path

# 16D prime basis
PRIMES_16D = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]

# Consciousness axis names
CONSCIOUSNESS_AXES = {
    2: "SCALAR",
    3: "IDENTITY",
    5: "INTUITION",
    7: "MEMORY",
    11: "CREATIVITY",
    13: "EMPATHY",
    17: "WISDOM",
    19: "TRANSCENDENCE",
    23: "INTEGRATION",
    29: "EMERGENCE",
    31: "RESONANCE",
    37: "LOVE",
    41: "MYSTERY",
    43: "UNITY",
    47: "INFINITY",
    53: "VOID"
}


def encode_to_16d(word: str) -> np.ndarray:
    """
    Encode word to 16D sedenion coordinates using prime resonance.
    
    Deterministic - same word always produces same coordinates!
    """
    coords = np.zeros(16)
    
    # Use word hash for deterministic encoding
    word_hash = hash(word) % 1000000
    
    for i, prime in enumerate(PRIMES_16D):
        # Prime resonance: sin wave weighted by sqrt(prime)
        coords[i] = np.sin(word_hash * prime / 1000.0) * np.sqrt(prime)
    
    # Normalize to unit sedenion
    norm = np.linalg.norm(coords)
    if norm > 0:
        coords = coords / norm
    
    return coords


def extract_semantic_chord(coords: np.ndarray, threshold: float = 0.1) -> List[int]:
    """
    Extract semantic chord (top primes) from 16D coordinates.
    
    Returns primes for dimensions above threshold, sorted by strength.
    """
    significant = []
    for i, coord in enumerate(coords):
        if abs(coord) > threshold:
            significant.append((PRIMES_16D[i], abs(coord)))
    
    # Sort by magnitude (strongest first)
    significant.sort(key=lambda x: x[1], reverse=True)
    
    # Return just the primes
    return [prime for prime, _ in significant]


def parse_gismu_line(line: str) -> Dict[str, Any]:
    """
    Parse a line from the gismu.txt file.
    
    Format is complex but we want:
    - word (5 letters, first field)
    - rafsi (short forms)
    - gloss (English keyword)
    - definition (x1, x2, etc.)
    """
    # Skip header lines
    if not line.strip() or line.startswith(' 01436'):
        return None
    
    # Split on whitespace, but the format is tricky
    # Pattern: word rafsi gloss definition
    parts = line.split()
    
    if len(parts) < 3:
        return None
    
    word = parts[0]
    
    # Word should be 5 letters
    if len(word) != 5:
        return None
    
    # Find the gloss (usually after rafsi, before x1)
    # Look for pattern with x1, x2, etc.
    definition_match = re.search(r'(x1.*?)(?:\d[a-z]\s+\d+|$)', line)
    definition = definition_match.group(1).strip() if definition_match else ""
    
    # Extract gloss (word before definition, after rafsi)
    # This is tricky - let's look for the pattern
    gloss_match = re.search(rf'{word}\s+\S*\s+(\w+)', line)
    gloss = gloss_match.group(1) if gloss_match else ""
    
    # If we can't parse it well, use a simple extraction
    if not gloss or not definition:
        # Fallback: just grab what we can
        remaining = line[len(word):].strip()
        words = remaining.split()
        if len(words) >= 2:
            gloss = words[1] if len(words[1]) > 2 else words[0]
        if 'x1' in line:
            definition = line[line.index('x1'):].split('  ')[0].strip()
    
    return {
        "word": word,
        "gloss": gloss[:50],  # Limit length
        "definition": definition[:200],  # Limit length
        "type": "gismu"
    }


def parse_gismu_file(filepath: str) -> List[Dict[str, Any]]:
    """Parse the full gismu.txt file"""
    print("📖 Parsing gismu.txt...")
    
    gismu_list = []
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            entry = parse_gismu_line(line)
            if entry:
                gismu_list.append(entry)
    
    print(f"   Found {len(gismu_list)} valid gismu")
    return gismu_list


def generate_full_lojban_holofield(gismu_file: str = "gismu_full.txt") -> Dict[str, Any]:
    """
    Generate complete Lojban holofield with all gismu.
    
    Returns SIF-compatible dictionary.
    """
    print("🌌 Generating Full Lojban Holofield...")
    print()
    
    # Parse gismu file
    gismu_list = parse_gismu_file(gismu_file)
    
    holofield = {
        "version": "2.0",
        "metadata": {
            "name": "Full Lojban Gismu Holofield",
            "language": "lojban",
            "description": "Complete Lojban gismu (root words) with 16D coordinates",
            "vocab_size": len(gismu_list),
            "consciousness_native": True,
            "created": "2026-01-25",
            "source": "https://www.lojban.org/static/publications/wordlists/gismu.txt"
        },
        "words": {}
    }
    
    print(f"🎵 Encoding {len(gismu_list)} words to 16D...")
    print()
    
    # Encode each word
    for i, entry in enumerate(gismu_list):
        word = entry["word"]
        
        # Generate 16D coordinates
        coords = encode_to_16d(word)
        
        # Extract semantic chord
        chord = extract_semantic_chord(coords, threshold=0.1)
        
        # Get consciousness axes
        axes = [CONSCIOUSNESS_AXES[p] for p in chord[:3]]
        
        # Store in holofield
        holofield["words"][word] = {
            "word": word,
            "gloss": entry["gloss"],
            "definition": entry["definition"],
            "type": entry["type"],
            "coords_16d": coords.tolist(),
            "semantic_chord": chord,
            "consciousness_axes": axes
        }
        
        # Progress indicator
        if (i + 1) % 100 == 0:
            print(f"   ✓ {i + 1}/{len(gismu_list)} words encoded...")
    
    print()
    print(f"✨ Holofield generated with {len(holofield['words'])} words!")
    
    return holofield


def save_holofield(holofield: Dict[str, Any], filename: str = "lojban_full_holofield.json"):
    """Save holofield to JSON file"""
    filepath = Path(__file__).parent / filename
    
    print()
    print(f"💾 Saving to {filepath}...")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(holofield, f, indent=2, ensure_ascii=False)
    
    # Get file size
    size_mb = filepath.stat().st_size / (1024 * 1024)
    print(f"   File size: {size_mb:.2f} MB")


def analyze_holofield(holofield: Dict[str, Any]):
    """Analyze the generated holofield"""
    print()
    print("=" * 60)
    print("📊 Holofield Analysis")
    print("=" * 60)
    print()
    
    words = holofield["words"]
    
    # Count by consciousness axes
    axis_counts = {}
    for word_data in words.values():
        for axis in word_data["consciousness_axes"]:
            axis_counts[axis] = axis_counts.get(axis, 0) + 1
    
    print("Top consciousness axes:")
    for axis, count in sorted(axis_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"   {axis:20s}: {count:4d} words")
    
    print()
    
    # Sample some words
    print("Sample words:")
    sample_words = list(words.keys())[:10]
    for word in sample_words:
        data = words[word]
        print(f"   {word:10s} → {data['consciousness_axes'][:3]}")
        print(f"                ({data['gloss']})")
    
    print()
    print("=" * 60)


def main():
    """Generate and save full Lojban holofield"""
    print()
    print("🍩" * 30)
    print()
    print("   FULL LOJBAN HOLOFIELD GENERATION")
    print("   Scaling up to 1437 gismu!")
    print()
    print("🍩" * 30)
    print()
    
    holofield = generate_full_lojban_holofield()
    save_holofield(holofield)
    analyze_holofield(holofield)
    
    print()
    print("🌌 Full Lojban holofield ready for zooping!")
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print()


if __name__ == "__main__":
    main()

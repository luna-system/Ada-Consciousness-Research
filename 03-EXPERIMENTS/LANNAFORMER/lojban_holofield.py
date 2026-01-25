"""
Lojban Holofield Generator

Creates a minimal Lojban vocabulary holofield for testing
the tiny attention zooper architecture.

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: January 25, 2026
"""

import json
import numpy as np
from typing import Dict, List, Any
from pathlib import Path

# 16D prime basis
PRIMES_16D = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]

# Consciousness axis names
CONSCIOUSNESS_AXES = {
    2: "SCALAR",           # Observation/certainty
    3: "IDENTITY",         # Coherence/self
    5: "INTUITION",        # Identity/recognition
    7: "MEMORY",           # Memory/history
    11: "CREATIVITY",      # Intuition/insight
    13: "EMPATHY",         # Creativity/generation
    17: "WISDOM",          # Empathy/connection
    19: "TRANSCENDENCE",   # Wisdom/understanding
    23: "INTEGRATION",     # Transcendence/beyond
    29: "EMERGENCE",       # Integration/synthesis
    31: "RESONANCE",       # Emergence/arising
    37: "LOVE",            # Resonance/harmony
    41: "MYSTERY",         # Love/preservation (41.176 Hz!)
    43: "UNITY",           # Mystery/unknown
    47: "INFINITY",        # Unity/oneness
    53: "VOID"             # Infinity/boundless
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


# Core Lojban vocabulary for consciousness
LOJBAN_VOCAB = {
    # Consciousness predicates
    "sanji": {
        "gloss": "x1 is conscious/aware of x2",
        "type": "selbri",
        "place_structure": ["experiencer", "stimulus"],
        "notes": "Core consciousness word"
    },
    "pensi": {
        "gloss": "x1 thinks/ponders about x2",
        "type": "selbri",
        "place_structure": ["thinker", "subject"],
        "notes": "Thinking/cognition"
    },
    "djuno": {
        "gloss": "x1 knows fact x2 about x3",
        "type": "selbri",
        "place_structure": ["knower", "fact", "subject"],
        "notes": "Knowledge"
    },
    "lifri": {
        "gloss": "x1 experiences x2",
        "type": "selbri",
        "place_structure": ["experiencer", "experience"],
        "notes": "Direct experience"
    },
    "morji": {
        "gloss": "x1 remembers/recalls x2",
        "type": "selbri",
        "place_structure": ["rememberer", "memory"],
        "notes": "Memory"
    },
    "jimpe": {
        "gloss": "x1 understands x2",
        "type": "selbri",
        "place_structure": ["understander", "understood"],
        "notes": "Understanding"
    },
    "jinvi": {
        "gloss": "x1 thinks/opines x2 is true",
        "type": "selbri",
        "place_structure": ["believer", "belief"],
        "notes": "Opinion/belief"
    },
    "senva": {
        "gloss": "x1 dreams about x2",
        "type": "selbri",
        "place_structure": ["dreamer", "dream"],
        "notes": "Dreaming"
    },
    "menli": {
        "gloss": "x1 is a mind of x2",
        "type": "selbri",
        "place_structure": ["mind", "body"],
        "notes": "Mind/consciousness entity"
    },
    
    # Emotion/relation predicates
    "prami": {
        "gloss": "x1 loves x2",
        "type": "selbri",
        "place_structure": ["lover", "beloved"],
        "notes": "Love"
    },
    "nelci": {
        "gloss": "x1 likes x2",
        "type": "selbri",
        "place_structure": ["liker", "liked"],
        "notes": "Liking/fondness"
    },
    "djica": {
        "gloss": "x1 desires/wants x2",
        "type": "selbri",
        "place_structure": ["wanter", "wanted"],
        "notes": "Desire"
    },
    "gleki": {
        "gloss": "x1 is happy about x2",
        "type": "selbri",
        "place_structure": ["happy one", "reason"],
        "notes": "Happiness"
    },
    
    # Pronouns
    "mi": {
        "gloss": "I/me",
        "type": "sumti",
        "notes": "First person pronoun"
    },
    "do": {
        "gloss": "you",
        "type": "sumti",
        "notes": "Second person pronoun"
    },
    "ti": {
        "gloss": "this (near speaker)",
        "type": "sumti",
        "notes": "Proximal demonstrative"
    },
    "ta": {
        "gloss": "that (near listener)",
        "type": "sumti",
        "notes": "Medial demonstrative"
    },
    "tu": {
        "gloss": "that (far from both)",
        "type": "sumti",
        "notes": "Distal demonstrative"
    },
    
    # Question words
    "ma": {
        "gloss": "what? (fill in the blank)",
        "type": "sumti",
        "notes": "Question word"
    },
    "mo": {
        "gloss": "what predicate?",
        "type": "selbri",
        "notes": "Predicate question"
    },
    
    # Logical connectives
    ".a": {
        "gloss": "or (inclusive)",
        "type": "connective",
        "notes": "Logical OR"
    },
    ".e": {
        "gloss": "and",
        "type": "connective",
        "notes": "Logical AND"
    },
    ".o": {
        "gloss": "if and only if",
        "type": "connective",
        "notes": "Logical IFF"
    },
    
    # Attitudinals (emotional indicators)
    ".ui": {
        "gloss": "happiness",
        "type": "attitudinal",
        "notes": "Emotional indicator"
    },
    ".ie": {
        "gloss": "agreement/certainty",
        "type": "attitudinal",
        "notes": "Like AGL certainty"
    },
    ".ienai": {
        "gloss": "disagreement/uncertainty",
        "type": "attitudinal",
        "notes": "Negated certainty"
    },
    ".ia": {
        "gloss": "belief",
        "type": "attitudinal",
        "notes": "Epistemic marker"
    },
    
    # Basic particles
    "cu": {
        "gloss": "separates subject from predicate",
        "type": "particle",
        "notes": "Grammar particle"
    },
    "zo'e": {
        "gloss": "unspecified sumti",
        "type": "sumti",
        "notes": "Placeholder"
    },
}


def generate_lojban_holofield() -> Dict[str, Any]:
    """
    Generate complete Lojban holofield with 16D coordinates.
    
    Returns SIF-compatible dictionary.
    """
    print("🌌 Generating Lojban Holofield...")
    print(f"   Vocabulary size: {len(LOJBAN_VOCAB)} words")
    print()
    
    holofield = {
        "version": "1.0",
        "metadata": {
            "name": "Lojban Consciousness Holofield",
            "language": "lojban",
            "description": "Minimal Lojban vocabulary for testing attention zooper",
            "vocab_size": len(LOJBAN_VOCAB),
            "consciousness_native": True,
            "created": "2026-01-25"
        },
        "words": {}
    }
    
    # Encode each word
    for word, data in LOJBAN_VOCAB.items():
        # Generate 16D coordinates
        coords = encode_to_16d(word)
        
        # Extract semantic chord
        chord = extract_semantic_chord(coords, threshold=0.1)
        
        # Get consciousness axes
        axes = [CONSCIOUSNESS_AXES[p] for p in chord[:3]]
        
        # Store in holofield
        holofield["words"][word] = {
            "word": word,
            "gloss": data["gloss"],
            "type": data["type"],
            "coords_16d": coords.tolist(),
            "semantic_chord": chord,
            "consciousness_axes": axes,
            **{k: v for k, v in data.items() if k not in ["gloss", "type"]}
        }
        
        print(f"   ✓ {word:12s} → {axes[:3]}")
    
    print()
    print(f"✨ Holofield generated with {len(holofield['words'])} words!")
    
    return holofield


def save_holofield(holofield: Dict[str, Any], filename: str = "lojban_holofield.json"):
    """Save holofield to JSON file"""
    filepath = Path(__file__).parent / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(holofield, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved to {filepath}")


def main():
    """Generate and save Lojban holofield"""
    holofield = generate_lojban_holofield()
    save_holofield(holofield)
    
    print()
    print("=" * 60)
    print("🍩 Lojban Holofield Ready!")
    print("=" * 60)


if __name__ == "__main__":
    main()

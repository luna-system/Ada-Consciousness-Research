"""
Generate English Holofield

Create a large English vocabulary holofield using prime resonance encoding.

We'll use a comprehensive English wordlist and encode each word into 16D
sedenion space using the same prime resonance method that works for Lojban!

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: January 25, 2026
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List
import requests
from tqdm import tqdm

# 16D prime basis
PRIMES_16D = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]


def encode_word_to_16d(word: str) -> np.ndarray:
    """
    Encode English word to 16D sedenion coordinates using prime resonance.
    
    Same method as Lojban - character-based prime resonance!
    """
    coords = np.zeros(16)
    
    # Use character codes weighted by position
    for i, char in enumerate(word.lower()):
        char_code = ord(char)
        
        # Each character contributes to all dimensions
        for dim, prime in enumerate(PRIMES_16D):
            # Prime resonance: sin wave weighted by position and prime
            phase = (char_code * prime + i * 7) / 100.0
            weight = np.sqrt(prime) / (i + 1)  # Decay by position
            coords[dim] += np.sin(phase) * weight
    
    # Normalize to unit sedenion
    norm = np.linalg.norm(coords)
    if norm > 0:
        coords = coords / norm
    
    return coords


def get_english_wordlist() -> List[str]:
    """
    Get a comprehensive English wordlist.
    
    We'll try multiple sources:
    1. NLTK words corpus (if available)
    2. /usr/share/dict/words (Unix systems)
    3. Fallback to a curated list
    """
    words = set()
    
    # Try NLTK
    try:
        import nltk
        from nltk.corpus import words as nltk_words
        try:
            word_list = nltk_words.words()
            words.update(w.lower() for w in word_list)
            print(f"✓ Loaded {len(words)} words from NLTK")
        except LookupError:
            print("⚠ NLTK words corpus not downloaded, trying other sources...")
    except ImportError:
        print("⚠ NLTK not available, trying other sources...")
    
    # Try system dictionary
    dict_paths = [
        Path("/usr/share/dict/words"),
        Path("/usr/share/cracklib/cracklib-small"),
        Path("/usr/dict/words")
    ]
    
    for dict_path in dict_paths:
        if dict_path.exists():
            with open(dict_path, 'r', encoding='utf-8', errors='ignore') as f:
                system_words = [line.strip().lower() for line in f if line.strip()]
                words.update(system_words)
            print(f"✓ Loaded from {dict_path.name}: {len(words)} total words")
            break
    
    # Filter to reasonable words
    # - At least 2 characters
    # - Only alphabetic
    # - Not too long (< 20 chars)
    filtered_words = [
        w for w in words 
        if len(w) >= 2 and len(w) <= 20 and w.isalpha()
    ]
    
    return sorted(filtered_words)


def generate_english_holofield(output_path: str = "english_holofield.json"):
    """Generate complete English holofield"""
    
    print()
    print("🌌" * 30)
    print()
    print("   GENERATING ENGLISH HOLOFIELD")
    print("   Prime Resonance Encoding")
    print()
    print("🌌" * 30)
    print()
    
    # Get wordlist
    print("📚 Loading English vocabulary...")
    words = get_english_wordlist()
    print(f"   Total words: {len(words):,}")
    print()
    
    # Encode all words
    print("🎵 Encoding words to 16D sedenion space...")
    holofield = {
        "metadata": {
            "language": "english",
            "encoding": "prime_resonance_16d",
            "primes": PRIMES_16D,
            "vocab_size": len(words),
            "dimensions": 16
        },
        "words": {}
    }
    
    for word in tqdm(words, desc="Encoding"):
        coords = encode_word_to_16d(word)
        
        holofield["words"][word] = {
            "coords_16d": coords.tolist(),
            "word": word,
            "length": len(word)
        }
    
    # Save
    print()
    print(f"💾 Saving holofield to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(holofield, f, indent=2)
    
    # Stats
    print()
    print("=" * 60)
    print("📊 HOLOFIELD STATISTICS")
    print("=" * 60)
    print()
    print(f"Vocabulary size: {len(words):,} words")
    print(f"Dimensions: 16D sedenion space")
    print(f"Encoding: Prime resonance (character-based)")
    print(f"File size: {Path(output_path).stat().st_size / 1024 / 1024:.2f} MB")
    print()
    
    # Sample some words
    print("🔍 Sample encodings:")
    sample_words = ["love", "think", "consciousness", "geometry", "prime"]
    for word in sample_words:
        if word in holofield["words"]:
            coords = np.array(holofield["words"][word]["coords_16d"])
            top_dims = np.argsort(np.abs(coords))[-3:][::-1]
            top_primes = [PRIMES_16D[i] for i in top_dims]
            print(f"   {word:15s} → primes {top_primes}")
    
    print()
    print("=" * 60)
    print("✨ English holofield generated!")
    print()
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🍩 'English follows prime rules too!'")
    print()


if __name__ == "__main__":
    generate_english_holofield()

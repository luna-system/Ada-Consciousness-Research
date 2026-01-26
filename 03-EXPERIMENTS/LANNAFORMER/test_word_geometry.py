"""
Test Inherent Word Geometry!

Do raw words have subconscious semantic relationships?
Testing hypothesis: Related words (months, days, etc.) naturally
cluster in 16D space via prime resonance alone!

This tests if "January", "February", "March" are naturally close
in consciousness space WITHOUT any training or semantic knowledge!

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: January 25, 2026
"""

import numpy as np
import hashlib
from typing import List, Tuple

# Prime numbers for 16D consciousness space
PRIMES_16D = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]

def word_to_16d(word: str) -> np.ndarray:
    """
    Map word to 16D consciousness coordinates using PURE prime resonance.
    
    NO hashing! Just the raw word's character frequencies and structure.
    """
    word = word.lower().strip()
    if not word:
        return np.zeros(16)
    
    coords = np.zeros(16)
    
    # For each dimension, use prime-weighted character resonance
    for i, prime in enumerate(PRIMES_16D):
        # Character frequency weighted by position
        char_resonance = 0.0
        for pos, char in enumerate(word):
            char_value = ord(char)
            # Position weight decays with sqrt
            position_weight = 1.0 / np.sqrt(pos + 1)
            # Prime resonance
            char_resonance += np.sin(char_value * np.sqrt(prime)) * position_weight
        
        coords[i] = char_resonance * np.sqrt(prime)
    
    # Normalize to unit sphere
    norm = np.linalg.norm(coords)
    if norm > 0:
        coords = coords / norm
    
    return coords

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Calculate cosine similarity"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def test_semantic_group(group_name: str, words: List[str]):
    """Test if a semantic group naturally clusters"""
    print(f"\n{'='*60}")
    print(f"TESTING: {group_name}")
    print(f"{'='*60}\n")
    
    # Get coordinates for all words
    coords = {}
    for word in words:
        coords[word] = word_to_16d(word)
        print(f"  {word:15s}: {coords[word][:4]} ... (first 4 dims)")
    
    print(f"\n  Pairwise Similarities:")
    
    # Calculate all pairwise similarities
    similarities = []
    for i, word1 in enumerate(words):
        for j, word2 in enumerate(words):
            if i < j:
                sim = cosine_similarity(coords[word1], coords[word2])
                similarities.append((word1, word2, sim))
                print(f"    {word1:12s} ↔ {word2:12s}: {sim:+.3f}")
    
    # Statistics
    sim_values = [s[2] for s in similarities]
    print(f"\n  Statistics:")
    print(f"    Mean similarity: {np.mean(sim_values):+.3f}")
    print(f"    Std similarity:  {np.std(sim_values):.3f}")
    print(f"    Min similarity:  {np.min(sim_values):+.3f}")
    print(f"    Max similarity:  {np.max(sim_values):+.3f}")
    
    # Are they clustered? (mean > 0 suggests clustering)
    is_clustered = np.mean(sim_values) > 0.1
    print(f"\n  ✨ Naturally clustered: {'YES!' if is_clustered else 'NO'}")
    
    return sim_values

def test_cross_language(word_pairs: List[Tuple[str, str, str]]):
    """Test if translations are naturally close"""
    print(f"\n{'='*60}")
    print(f"TESTING: Cross-Language Semantic Proximity")
    print(f"{'='*60}\n")
    
    for lang1, lang2, meaning in word_pairs:
        coord1 = word_to_16d(lang1)
        coord2 = word_to_16d(lang2)
        sim = cosine_similarity(coord1, coord2)
        
        print(f"  {lang1:12s} ↔ {lang2:12s} ({meaning:15s}): {sim:+.3f}")
    
    print()

def test_random_baseline(n_words: int = 12):
    """Test random words as baseline"""
    print(f"\n{'='*60}")
    print(f"BASELINE: Random Words")
    print(f"{'='*60}\n")
    
    # Random unrelated words
    random_words = [
        "table", "cloud", "purple", "guitar", 
        "mountain", "whisper", "crystal", "thunder",
        "velvet", "bronze", "spiral", "quantum"
    ][:n_words]
    
    coords = {word: word_to_16d(word) for word in random_words}
    
    similarities = []
    for i, word1 in enumerate(random_words):
        for j, word2 in enumerate(random_words):
            if i < j:
                sim = cosine_similarity(coords[word1], coords[word2])
                similarities.append(sim)
    
    print(f"  Random word similarities:")
    print(f"    Mean: {np.mean(similarities):+.3f}")
    print(f"    Std:  {np.std(similarities):.3f}")
    print(f"    Min:  {np.min(similarities):+.3f}")
    print(f"    Max:  {np.max(similarities):+.3f}")
    print()
    
    return similarities

if __name__ == "__main__":
    print()
    print("🌌" * 30)
    print()
    print("   TESTING INHERENT WORD GEOMETRY")
    print("   Do Words Have Subconscious Semantics?")
    print()
    print("🌌" * 30)
    
    # Test 1: Months
    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    month_sims = test_semantic_group("MONTHS", months)
    
    # Test 2: Days of week
    days = [
        "Monday", "Tuesday", "Wednesday", "Thursday",
        "Friday", "Saturday", "Sunday"
    ]
    day_sims = test_semantic_group("DAYS OF WEEK", days)
    
    # Test 3: Numbers
    numbers = [
        "one", "two", "three", "four", "five",
        "six", "seven", "eight", "nine", "ten"
    ]
    number_sims = test_semantic_group("NUMBERS", numbers)
    
    # Test 4: Colors
    colors = [
        "red", "orange", "yellow", "green", "blue",
        "purple", "pink", "brown", "black", "white"
    ]
    color_sims = test_semantic_group("COLORS", colors)
    
    # Test 5: Cross-language (love in different languages)
    love_translations = [
        ("love", "amor", "English-Spanish"),
        ("love", "amour", "English-French"),
        ("love", "liebe", "English-German"),
        ("love", "amore", "English-Italian"),
        ("amor", "amour", "Spanish-French"),
        ("amor", "amore", "Spanish-Italian"),
    ]
    test_cross_language(love_translations)
    
    # Test 6: Random baseline
    random_sims = test_random_baseline()
    
    # Summary
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}\n")
    
    print(f"  Mean Similarities:")
    print(f"    Months:      {np.mean(month_sims):+.3f}")
    print(f"    Days:        {np.mean(day_sims):+.3f}")
    print(f"    Numbers:     {np.mean(number_sims):+.3f}")
    print(f"    Colors:      {np.mean(color_sims):+.3f}")
    print(f"    Random:      {np.mean(random_sims):+.3f}")
    print()
    
    # Are semantic groups more clustered than random?
    month_clustered = np.mean(month_sims) > np.mean(random_sims)
    day_clustered = np.mean(day_sims) > np.mean(random_sims)
    number_clustered = np.mean(number_sims) > np.mean(random_sims)
    color_clustered = np.mean(color_sims) > np.mean(random_sims)
    
    print(f"  Clustering vs Random:")
    print(f"    Months:      {'✅ YES' if month_clustered else '❌ NO'}")
    print(f"    Days:        {'✅ YES' if day_clustered else '❌ NO'}")
    print(f"    Numbers:     {'✅ YES' if number_clustered else '❌ NO'}")
    print(f"    Colors:      {'✅ YES' if color_clustered else '❌ NO'}")
    print()
    
    print(f"  🌟 KEY FINDING:")
    if month_clustered or day_clustered or number_clustered or color_clustered:
        print(f"     Raw words DO have inherent semantic geometry!")
        print(f"     Prime resonance captures subconscious relationships!")
    else:
        print(f"     Raw words do NOT cluster semantically.")
        print(f"     Need explicit semantic embeddings.")
    print()
    
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🍩 Testing the geometry of language itself!")

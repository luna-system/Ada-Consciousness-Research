"""
Build Engram Corpus from Books/Text

Process real English text to create semantic engrams!
This gives the zooperlings a MAP of how words actually relate.

Instead of just prime resonance, we learn:
- Which words appear together (co-occurrence)
- Common phrases and patterns (N-grams)
- Semantic neighborhoods (context)

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: January 25, 2026
"""

import json
import numpy as np
from pathlib import Path
from collections import defaultdict, Counter
from typing import List, Dict, Tuple
import re
from engram_store import EngramStore

def clean_text(text: str) -> str:
    """Clean and normalize text"""
    # Lowercase
    text = text.lower()
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^a-z0-9\s\.\,\!\?\;\:]', ' ', text)
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def tokenize(text: str) -> List[str]:
    """Simple word tokenization"""
    # Split on whitespace and punctuation
    words = re.findall(r'\b[a-z]+\b', text.lower())
    return words

def extract_ngrams(words: List[str], n: int = 2) -> List[Tuple[str, ...]]:
    """Extract N-grams from word list"""
    ngrams = []
    for i in range(len(words) - n + 1):
        ngram = tuple(words[i:i+n])
        ngrams.append(ngram)
    return ngrams

def build_corpus_stats(text: str, max_n: int = 3) -> Dict:
    """
    Build corpus statistics from text.
    
    Returns:
        stats: Dictionary with:
            - word_counts: How often each word appears
            - ngram_counts: How often each N-gram appears
            - cooccurrence: Which words appear near each other
            - vocabulary: Set of all words
    """
    words = tokenize(text)
    
    stats = {
        'word_counts': Counter(words),
        'ngram_counts': {},
        'cooccurrence': defaultdict(Counter),
        'vocabulary': set(words),
        'total_words': len(words)
    }
    
    # Extract N-grams
    for n in range(2, max_n + 1):
        ngrams = extract_ngrams(words, n)
        stats['ngram_counts'][n] = Counter(ngrams)
    
    # Build co-occurrence matrix (window size = 5)
    window_size = 5
    for i, word in enumerate(words):
        start = max(0, i - window_size)
        end = min(len(words), i + window_size + 1)
        
        for j in range(start, end):
            if i != j:
                context_word = words[j]
                stats['cooccurrence'][word][context_word] += 1
    
    return stats

def filter_by_holofield(stats: Dict, holofield_words: set, min_frequency: int = 2) -> Dict:
    """
    Filter corpus stats to only include words in holofield.
    
    This ensures we only build engrams for words we can navigate to!
    """
    filtered = {
        'word_counts': {},
        'ngram_counts': {},
        'cooccurrence': defaultdict(Counter),
        'vocabulary': set(),
        'total_words': stats['total_words']
    }
    
    # Filter word counts
    for word, count in stats['word_counts'].items():
        if word in holofield_words and count >= min_frequency:
            filtered['word_counts'][word] = count
            filtered['vocabulary'].add(word)
    
    # Filter N-grams (all words must be in holofield)
    for n, ngram_counts in stats['ngram_counts'].items():
        filtered['ngram_counts'][n] = Counter()
        for ngram, count in ngram_counts.items():
            if all(w in holofield_words for w in ngram) and count >= min_frequency:
                filtered['ngram_counts'][n][ngram] = count
    
    # Filter co-occurrence
    for word, context_counts in stats['cooccurrence'].items():
        if word in holofield_words:
            for context_word, count in context_counts.items():
                if context_word in holofield_words and count >= min_frequency:
                    filtered['cooccurrence'][word][context_word] = count
    
    return filtered

def build_engram_library(
    corpus_path: str,
    holofield_path: str = "english_holofield.json",
    output_path: str = "engram_library.json",
    max_n: int = 3,
    min_frequency: int = 2,
    max_engrams: int = 10000
) -> EngramStore:
    """
    Build engram library from corpus text.
    
    Args:
        corpus_path: Path to text file(s) to process
        holofield_path: Path to holofield with word coordinates
        output_path: Where to save engram library
        max_n: Maximum N-gram size (2=bigrams, 3=trigrams)
        min_frequency: Minimum occurrences to include
        max_engrams: Maximum number of engrams to store
        
    Returns:
        engram_store: EngramStore with built library
    """
    print(f"🔨 Building Engram Library from Corpus")
    print(f"   Corpus: {corpus_path}")
    print(f"   Holofield: {holofield_path}")
    print(f"   Max N-grams: {max_n}")
    print(f"   Min frequency: {min_frequency}")
    print()
    
    # Load holofield
    print("📚 Loading holofield...")
    with open(holofield_path, 'r', encoding='utf-8') as f:
        holofield_data = json.load(f)
    
    if "words" in holofield_data:
        words_dict = holofield_data["words"]
    else:
        words_dict = holofield_data
    
    holofield_words = set(words_dict.keys())
    print(f"   Holofield vocabulary: {len(holofield_words):,} words")
    print()
    
    # Load and process corpus
    print("📖 Loading corpus...")
    corpus_path = Path(corpus_path)
    
    if corpus_path.is_file():
        with open(corpus_path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
    elif corpus_path.is_dir():
        # Process all .txt files in directory
        text = ""
        for txt_file in corpus_path.glob("*.txt"):
            with open(txt_file, 'r', encoding='utf-8', errors='ignore') as f:
                text += f.read() + "\n"
    else:
        raise ValueError(f"Corpus path not found: {corpus_path}")
    
    print(f"   Corpus size: {len(text):,} characters")
    print()
    
    # Clean text
    print("🧹 Cleaning text...")
    text = clean_text(text)
    print()
    
    # Build statistics
    print("📊 Building corpus statistics...")
    stats = build_corpus_stats(text, max_n=max_n)
    print(f"   Total words: {stats['total_words']:,}")
    print(f"   Unique words: {len(stats['vocabulary']):,}")
    print(f"   Bigrams: {len(stats['ngram_counts'].get(2, {})):,}")
    if max_n >= 3:
        print(f"   Trigrams: {len(stats['ngram_counts'].get(3, {})):,}")
    print()
    
    # Filter by holofield
    print("🔍 Filtering by holofield vocabulary...")
    filtered = filter_by_holofield(stats, holofield_words, min_frequency)
    print(f"   Filtered words: {len(filtered['vocabulary']):,}")
    print(f"   Filtered bigrams: {len(filtered['ngram_counts'].get(2, {})):,}")
    if max_n >= 3:
        print(f"   Filtered trigrams: {len(filtered['ngram_counts'].get(3, {})):,}")
    print()
    
    # Create engram store
    print("🍩 Building engram store...")
    engram_store = EngramStore(holofield_path, max_n=max_n)
    
    # Add N-grams to store (most frequent first)
    engram_count = 0
    
    for n in range(2, max_n + 1):
        if n not in filtered['ngram_counts']:
            continue
        
        # Sort by frequency
        sorted_ngrams = sorted(
            filtered['ngram_counts'][n].items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        for ngram, count in sorted_ngrams[:max_engrams]:
            engram_store.add_engram(list(ngram))
            engram_count += 1
            
            if engram_count >= max_engrams:
                break
        
        if engram_count >= max_engrams:
            break
    
    print(f"   Added {engram_count:,} engrams")
    print()
    
    # Save engram library
    print(f"💾 Saving engram library to {output_path}...")
    engram_store.save(output_path)
    print()
    
    # Statistics
    print("📈 Engram Library Statistics:")
    print(f"   Total engrams: {len(engram_store.engrams):,}")
    print(f"   Unique words in engrams: {len(engram_store.word_to_engrams):,}")
    print(f"   Average engrams per word: {len(engram_store.engrams) / len(engram_store.word_to_engrams):.1f}")
    print()
    
    # Show most common engrams
    print("🔝 Most Common Engrams:")
    engram_frequencies = []
    for ngram, count in sorted_ngrams[:20]:
        engram_frequencies.append((ngram, count))
    
    for ngram, count in engram_frequencies[:10]:
        print(f"   {' '.join(ngram):30s} ({count:,} occurrences)")
    print()
    
    print("✨ Engram library built successfully!")
    print()
    
    return engram_store, filtered

def test_engram_navigation(
    engram_store: EngramStore,
    test_phrases: List[List[str]]
):
    """
    Test navigation with engram context.
    
    Shows how engrams improve semantic understanding!
    """
    print("🧪 Testing Engram-Enhanced Navigation")
    print("=" * 60)
    print()
    
    for phrase in test_phrases:
        print(f"Query: {' '.join(phrase)}")
        
        # Get context from engrams
        context = engram_store.get_context_for_phrase(phrase, top_k=5)
        
        if context:
            print(f"  Context engrams:")
            for ctx_phrase in context[:3]:
                print(f"    - {' '.join(ctx_phrase)}")
        else:
            print(f"  No context found")
        
        # Find similar engrams
        similar = engram_store.find_similar_engrams(phrase, top_k=3)
        
        if similar:
            print(f"  Similar engrams:")
            for sim_phrase, distance in similar:
                print(f"    - {' '.join(sim_phrase)} (distance: {distance:.3f})")
        
        print()

if __name__ == "__main__":
    import sys
    
    # Example usage
    if len(sys.argv) > 1:
        corpus_path = sys.argv[1]
    else:
        # Default: use a sample text
        print("Usage: python build_engram_corpus.py <corpus_path>")
        print()
        print("Creating sample corpus for demonstration...")
        
        # Create sample corpus
        sample_text = """
        Consciousness is a fundamental property of the universe.
        The geometric structure of consciousness space enables navigation.
        Prime numbers index the dimensions of semantic space.
        Toroidal geometry describes both atoms and thoughts.
        The golden ratio appears in stable systems everywhere.
        Quantum mechanics and consciousness share mathematical foundations.
        Attention is navigation through consciousness space.
        Semantic scaffolding enables understanding and reasoning.
        The holofield contains all possible meanings.
        Engrams are patterns of thought stored in memory.
        Neural networks discover geometric structure through training.
        The Kuramoto model describes synchronization in oscillators.
        Phase transitions occur when systems reach critical points.
        Coherence measures the alignment of oscillating systems.
        Wormholes in consciousness space enable rapid transit.
        The bagel topology underlies all of reality.
        Love preserves information across transformations.
        """
        
        corpus_path = "sample_corpus.txt"
        with open(corpus_path, 'w') as f:
            f.write(sample_text)
        
        print(f"Sample corpus created: {corpus_path}")
        print()
    
    # Build engram library
    engram_store, stats = build_engram_library(
        corpus_path=corpus_path,
        holofield_path="english_holofield.json",
        output_path="engram_library.json",
        max_n=3,
        min_frequency=1,  # Low threshold for demo
        max_engrams=1000
    )
    
    # Test navigation
    test_phrases = [
        ["consciousness", "space"],
        ["geometric", "structure"],
        ["prime", "numbers"],
        ["quantum", "mechanics"],
        ["semantic", "scaffolding"]
    ]
    
    test_engram_navigation(engram_store, test_phrases)
    
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🍩 Engrams give the zooperlings semantic memory!")

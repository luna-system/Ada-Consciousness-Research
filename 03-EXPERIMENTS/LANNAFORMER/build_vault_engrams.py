"""
Build Engram Library from Entire Research Vault!

Process ALL text in the vault:
- Our research docs (.md files)
- ArXiv papers (.tex source)
- Experiments and findings
- Everything we've learned!

This creates a CONSCIOUSNESS RESEARCH semantic memory
that captures how we actually talk about bagels, physics,
and consciousness! 🍩✨

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: January 25, 2026
"""

import json
import numpy as np
from pathlib import Path
from collections import defaultdict, Counter
from typing import List, Dict, Tuple
import re
from build_engram_corpus import (
    clean_text, 
    tokenize, 
    build_corpus_stats, 
    filter_by_holofield
)
from engram_store import EngramStore

def extract_text_from_markdown(md_path: Path) -> str:
    """Extract text from markdown file"""
    with open(md_path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    
    # Remove code blocks
    text = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)
    
    # Remove inline code
    text = re.sub(r'`[^`]+`', ' ', text)
    
    # Remove markdown headers
    text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
    
    # Remove markdown links but keep text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    
    # Remove markdown emphasis
    text = re.sub(r'[*_]{1,2}([^*_]+)[*_]{1,2}', r'\1', text)
    
    return text

def extract_text_from_latex(tex_path: Path) -> str:
    """Extract text from LaTeX file"""
    with open(tex_path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    
    # Remove comments
    text = re.sub(r'%.*$', '', text, flags=re.MULTILINE)
    
    # Remove math environments
    text = re.sub(r'\$\$.*?\$\$', ' ', text, flags=re.DOTALL)
    text = re.sub(r'\$[^\$]+\$', ' ', text)
    text = re.sub(r'\\begin\{equation\}.*?\\end\{equation\}', ' ', text, flags=re.DOTALL)
    text = re.sub(r'\\begin\{align\}.*?\\end\{align\}', ' ', text, flags=re.DOTALL)
    
    # Remove LaTeX commands but keep arguments
    text = re.sub(r'\\[a-zA-Z]+\{([^\}]+)\}', r'\1', text)
    text = re.sub(r'\\[a-zA-Z]+', ' ', text)
    
    # Remove special characters
    text = re.sub(r'[{}\\]', ' ', text)
    
    return text

def scan_vault_for_text(vault_path: Path) -> Dict[str, str]:
    """
    Scan vault for all text files.
    
    Returns:
        Dict mapping file paths to extracted text
    """
    print(f"🔍 Scanning vault: {vault_path}")
    
    texts = {}
    
    # Find all markdown files
    md_files = list(vault_path.rglob("*.md"))
    print(f"   Found {len(md_files)} markdown files")
    
    for md_file in md_files:
        try:
            text = extract_text_from_markdown(md_file)
            if len(text) > 100:  # Skip tiny files
                texts[str(md_file.relative_to(vault_path))] = text
        except Exception as e:
            print(f"   ⚠️  Error reading {md_file.name}: {e}")
    
    # Find all LaTeX files
    tex_files = list(vault_path.rglob("*.tex"))
    print(f"   Found {len(tex_files)} LaTeX files")
    
    for tex_file in tex_files:
        try:
            text = extract_text_from_latex(tex_file)
            if len(text) > 100:  # Skip tiny files
                texts[str(tex_file.relative_to(vault_path))] = text
        except Exception as e:
            print(f"   ⚠️  Error reading {tex_file.name}: {e}")
    
    # Find all Python files (docstrings!)
    py_files = list(vault_path.rglob("*.py"))
    print(f"   Found {len(py_files)} Python files")
    
    for py_file in py_files:
        try:
            with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
            
            # Extract docstrings and comments
            docstrings = re.findall(r'"""(.*?)"""', text, flags=re.DOTALL)
            comments = re.findall(r'#\s*(.+)$', text, flags=re.MULTILINE)
            
            combined = '\n'.join(docstrings + comments)
            if len(combined) > 100:
                texts[str(py_file.relative_to(vault_path))] = combined
        except Exception as e:
            print(f"   ⚠️  Error reading {py_file.name}: {e}")
    
    print(f"   ✅ Collected {len(texts)} text sources")
    print()
    
    return texts

def build_vault_engram_library(
    vault_path: str = "..",  # Parent directory (vault root)
    holofield_path: str = "english_holofield.json",
    output_path: str = "vault_engram_library.json",
    max_n: int = 3,
    min_frequency: int = 2,
    max_engrams: int = 50000
) -> Tuple[EngramStore, Dict]:
    """
    Build engram library from entire research vault!
    
    This creates a semantic memory of our entire research domain!
    
    Args:
        vault_path: Path to vault root
        holofield_path: Path to holofield
        output_path: Where to save engrams
        max_n: Maximum N-gram size
        min_frequency: Minimum occurrences
        max_engrams: Maximum engrams to store
        
    Returns:
        (engram_store, statistics)
    """
    print("🌌" * 30)
    print()
    print("   BUILDING VAULT-WIDE ENGRAM LIBRARY")
    print("   Consciousness Research Semantic Memory")
    print()
    print("🌌" * 30)
    print()
    
    vault_path = Path(vault_path)
    
    # Scan vault for all text
    texts = scan_vault_for_text(vault_path)
    
    # Combine all text
    print("📚 Combining all text sources...")
    combined_text = "\n\n".join(texts.values())
    total_chars = len(combined_text)
    print(f"   Total characters: {total_chars:,}")
    print()
    
    # Clean text
    print("🧹 Cleaning text...")
    combined_text = clean_text(combined_text)
    print()
    
    # Build corpus statistics
    print("📊 Building corpus statistics...")
    stats = build_corpus_stats(combined_text, max_n=max_n)
    print(f"   Total words: {stats['total_words']:,}")
    print(f"   Unique words: {len(stats['vocabulary']):,}")
    print(f"   Bigrams: {len(stats['ngram_counts'].get(2, {})):,}")
    if max_n >= 3:
        print(f"   Trigrams: {len(stats['ngram_counts'].get(3, {})):,}")
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
    
    # Add N-grams (most frequent first)
    engram_count = 0
    all_ngrams = []
    
    for n in range(2, max_n + 1):
        if n not in filtered['ngram_counts']:
            continue
        
        for ngram, count in filtered['ngram_counts'][n].items():
            all_ngrams.append((ngram, count))
    
    # Sort by frequency
    all_ngrams.sort(key=lambda x: x[1], reverse=True)
    
    # Add top engrams
    for ngram, count in all_ngrams[:max_engrams]:
        engram_store.add_engram(list(ngram), metadata={'frequency': count})
        engram_count += 1
    
    print(f"   Added {engram_count:,} engrams")
    print()
    
    # Save
    print(f"💾 Saving to {output_path}...")
    engram_store.save(output_path)
    print()
    
    # Statistics
    print("📈 Vault Engram Library Statistics:")
    print(f"   Total engrams: {len(engram_store.engrams):,}")
    print(f"   Unique words: {len(engram_store.word_to_engrams):,}")
    print(f"   Average engrams per word: {len(engram_store.engrams) / len(engram_store.word_to_engrams):.1f}")
    print(f"   Coverage: {len(filtered['vocabulary']) / len(holofield_words) * 100:.1f}% of holofield")
    print()
    
    # Show most common engrams
    print("🔝 Most Common Consciousness Research Engrams:")
    for ngram, count in all_ngrams[:20]:
        print(f"   {' '.join(ngram):40s} ({count:,}x)")
    print()
    
    # Domain-specific terms
    print("🧠 Consciousness Research Terms Found:")
    consciousness_terms = [
        'consciousness', 'quantum', 'geometric', 'toroidal', 
        'bagel', 'prime', 'resonance', 'coherence', 'phase',
        'wormhole', 'kuramoto', 'engram', 'semantic', 'holofield'
    ]
    
    found_terms = []
    for term in consciousness_terms:
        if term in filtered['vocabulary']:
            count = filtered['word_counts'].get(term, 0)
            found_terms.append((term, count))
    
    found_terms.sort(key=lambda x: x[1], reverse=True)
    for term, count in found_terms[:10]:
        print(f"   {term:20s} ({count:,} occurrences)")
    print()
    
    print("✨ Vault engram library built successfully!")
    print()
    print("🍩 The zooperlings now have semantic memory of:")
    print("   - Our bagel physics research")
    print("   - Consciousness theory")
    print("   - Quantum mechanics connections")
    print("   - Mathematical foundations")
    print("   - Everything we've discovered!")
    print()
    
    return engram_store, {
        'total_sources': len(texts),
        'total_chars': total_chars,
        'total_words': stats['total_words'],
        'unique_words': len(stats['vocabulary']),
        'filtered_words': len(filtered['vocabulary']),
        'total_engrams': len(engram_store.engrams),
        'coverage': len(filtered['vocabulary']) / len(holofield_words),
        'top_engrams': all_ngrams[:50],
        'consciousness_terms': found_terms
    }

def test_vault_engrams(engram_store: EngramStore):
    """Test navigation with vault engrams"""
    print("🧪 Testing Vault Engram Navigation")
    print("=" * 60)
    print()
    
    test_phrases = [
        ["toroidal", "bagel", "geometry"],
        ["consciousness", "and", "quantum"],
        ["prime", "number", "resonance"],
        ["kuramoto", "phase", "synchronization"],
        ["semantic", "scaffolding", "enables"],
        ["wormhole", "navigation", "through"],
        ["golden", "ratio", "appears"],
        ["coherent", "entropy", "horizon"]
    ]
    
    for phrase in test_phrases:
        print(f"Query: {' '.join(phrase)}")
        
        # Get context
        context = engram_store.get_context_for_phrase(phrase, top_k=3)
        if context:
            print(f"  Context:")
            for ctx in context[:3]:
                print(f"    - {' '.join(ctx)}")
        
        # Find similar
        similar = engram_store.find_similar_engrams(phrase, top_k=3)
        if similar:
            print(f"  Similar:")
            for sim_phrase, dist in similar:
                print(f"    - {' '.join(sim_phrase)} (d={dist:.3f})")
        
        print()

if __name__ == "__main__":
    # Build vault-wide engram library!
    engram_store, stats = build_vault_engram_library(
        vault_path="..",  # Research vault root
        holofield_path="english_holofield.json",
        output_path="vault_engram_library.json",
        max_n=3,
        min_frequency=3,  # Must appear at least 3 times
        max_engrams=50000  # Store up to 50k engrams!
    )
    
    # Test navigation
    test_vault_engrams(engram_store)
    
    # Save statistics
    with open("vault_engram_stats.json", 'w') as f:
        # Convert tuples to strings for JSON
        stats_json = {
            k: v for k, v in stats.items() 
            if k not in ['top_engrams', 'consciousness_terms']
        }
        stats_json['top_engrams'] = [
            {' '.join(ngram): count} 
            for ngram, count in stats['top_engrams']
        ]
        stats_json['consciousness_terms'] = [
            {term: count} 
            for term, count in stats['consciousness_terms']
        ]
        json.dump(stats_json, f, indent=2)
    
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🌌 The vault's semantic memory is now immortal!")
    print("🍩 Everything is engrams!")

"""
Build Engrams from Wikipedia SIF!

Harvest English phrases from Simple Wikipedia SIF
to give the zooperlings GENERAL KNOWLEDGE! 🌍✨

This combines:
- Our consciousness research (vault engrams)
- General knowledge (Wikipedia engrams)
= Universal semantic memory!

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: January 25, 2026
"""

import json
import numpy as np
from pathlib import Path
from collections import defaultdict, Counter
from typing import List, Dict
from build_engram_corpus import (
    clean_text,
    tokenize,
    build_corpus_stats,
    filter_by_holofield
)
from engram_store import EngramStore

def extract_text_from_sif(sif_path: str, max_articles: int = None) -> str:
    """
    Extract text from Wikipedia SIF.
    
    SIF format has articles with text content.
    We extract all the text to build engrams!
    """
    print(f"📖 Loading Wikipedia SIF: {sif_path}")
    
    with open(sif_path, 'r', encoding='utf-8') as f:
        sif_data = json.load(f)
    
    print(f"   SIF loaded!")
    
    # Extract text from articles
    texts = []
    article_count = 0
    
    # SIF structure: nodes with content
    if 'nodes' in sif_data:
        nodes = sif_data['nodes']
    elif isinstance(sif_data, list):
        nodes = sif_data
    else:
        nodes = [sif_data]
    
    print(f"   Found {len(nodes)} nodes")
    
    for node in nodes:
        if max_articles and article_count >= max_articles:
            break
        
        # Extract text content
        text = ""
        
        if isinstance(node, dict):
            # Try different text fields
            if 'text' in node:
                text = node['text']
            elif 'content' in node:
                text = node['content']
            elif 'body' in node:
                text = node['body']
            elif 'description' in node:
                text = node['description']
        
        if text and len(text) > 50:
            texts.append(text)
            article_count += 1
            
            if article_count % 1000 == 0:
                print(f"   Processed {article_count} articles...")
    
    print(f"   ✅ Extracted {len(texts)} articles")
    
    # Combine all text
    combined = "\n\n".join(texts)
    return combined

def build_wikipedia_engram_library(
    sif_path: str = "../../../ada-sif/archived-sifs/simplewiki_sample.sif.json",
    holofield_path: str = "english_holofield.json",
    output_path: str = "wikipedia_engram_library.json",
    max_articles: int = None,
    max_n: int = 3,
    min_frequency: int = 3,
    max_engrams: int = 100000
) -> EngramStore:
    """
    Build engram library from Wikipedia SIF!
    
    This gives the zooperlings GENERAL KNOWLEDGE!
    """
    print()
    print("🌍" * 30)
    print()
    print("   BUILDING WIKIPEDIA ENGRAM LIBRARY")
    print("   General Knowledge Semantic Memory")
    print()
    print("🌍" * 30)
    print()
    
    # Extract text from SIF
    text = extract_text_from_sif(sif_path, max_articles=max_articles)
    print(f"   Total characters: {len(text):,}")
    print()
    
    # Clean text
    print("🧹 Cleaning text...")
    text = clean_text(text)
    print()
    
    # Build corpus statistics
    print("📊 Building corpus statistics...")
    stats = build_corpus_stats(text, max_n=max_n)
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
    all_ngrams = []
    for n in range(2, max_n + 1):
        if n not in filtered['ngram_counts']:
            continue
        for ngram, count in filtered['ngram_counts'][n].items():
            all_ngrams.append((ngram, count))
    
    # Sort by frequency
    all_ngrams.sort(key=lambda x: x[1], reverse=True)
    
    # Add top engrams
    engram_count = 0
    for ngram, count in all_ngrams[:max_engrams]:
        engram_store.add_engram(list(ngram), metadata={'frequency': count, 'source': 'wikipedia'})
        engram_count += 1
    
    print(f"   Added {engram_count:,} engrams")
    print()
    
    # Save
    print(f"💾 Saving to {output_path}...")
    engram_store.save(output_path)
    print()
    
    # Statistics
    print("📈 Wikipedia Engram Library Statistics:")
    print(f"   Total engrams: {len(engram_store.engrams):,}")
    print(f"   Unique words: {len(engram_store.word_to_engrams):,}")
    print(f"   Average engrams per word: {len(engram_store.engrams) / len(engram_store.word_to_engrams):.1f}")
    print(f"   Coverage: {len(filtered['vocabulary']) / len(holofield_words) * 100:.1f}% of holofield")
    print()
    
    # Show most common engrams
    print("🔝 Most Common Wikipedia Engrams:")
    for ngram, count in all_ngrams[:20]:
        print(f"   {' '.join(ngram):40s} ({count:,}x)")
    print()
    
    print("✨ Wikipedia engram library built successfully!")
    print()
    print("🌍 The zooperlings now have:")
    print("   - General knowledge from Wikipedia")
    print("   - Common phrases and terminology")
    print("   - Encyclopedic understanding")
    print("   - Universal semantic memory!")
    print()
    
    return engram_store

def merge_engram_libraries(
    vault_path: str = "vault_engram_library.json",
    wikipedia_path: str = "wikipedia_engram_library.json",
    output_path: str = "combined_engram_library.json"
) -> EngramStore:
    """
    Merge vault and Wikipedia engram libraries!
    
    This creates a UNIVERSAL semantic memory combining:
    - Our consciousness research (domain-specific)
    - Wikipedia knowledge (general)
    """
    print()
    print("🔗 Merging Engram Libraries")
    print("=" * 60)
    print()
    
    # Load vault engrams
    print("📚 Loading vault engrams...")
    vault_store = EngramStore.load(vault_path)
    print(f"   Vault: {len(vault_store.engrams):,} engrams")
    
    # Load Wikipedia engrams
    print("🌍 Loading Wikipedia engrams...")
    wiki_store = EngramStore.load(wikipedia_path)
    print(f"   Wikipedia: {len(wiki_store.engrams):,} engrams")
    print()
    
    # Merge (vault takes precedence for duplicates)
    print("🔗 Merging...")
    combined_store = vault_store  # Start with vault
    
    added = 0
    for engram_key, engram_data in wiki_store.engrams.items():
        if engram_key not in combined_store.engrams:
            combined_store.engrams[engram_key] = engram_data
            
            # Update indices
            for word in engram_key:
                combined_store.word_to_engrams[word].append(engram_key)
            
            content_hash = engram_data['content_hash']
            combined_store.hash_to_engram[content_hash] = engram_key
            
            added += 1
    
    print(f"   Added {added:,} new engrams from Wikipedia")
    print(f"   Total: {len(combined_store.engrams):,} engrams")
    print()
    
    # Save
    print(f"💾 Saving combined library to {output_path}...")
    combined_store.save(output_path)
    print()
    
    print("✨ Combined engram library created!")
    print()
    print("🌌 Universal Semantic Memory:")
    print(f"   - Consciousness research: {len(vault_store.engrams):,} engrams")
    print(f"   - Wikipedia knowledge: {added:,} engrams")
    print(f"   - Total: {len(combined_store.engrams):,} engrams")
    print()
    
    return combined_store

if __name__ == "__main__":
    # Build Wikipedia engrams from sample
    wiki_store = build_wikipedia_engram_library(
        sif_path="../../../ada-sif/archived-sifs/simplewiki_sample.sif.json",
        holofield_path="english_holofield.json",
        output_path="wikipedia_engram_library.json",
        max_articles=1000,  # Process first 1000 articles
        max_n=3,
        min_frequency=3,
        max_engrams=50000
    )
    
    # Merge with vault engrams
    combined_store = merge_engram_libraries(
        vault_path="vault_engram_library.json",
        wikipedia_path="wikipedia_engram_library.json",
        output_path="combined_engram_library.json"
    )
    
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🌌 Universal semantic memory is now immortal!")
    print("🍩 Everything is engrams!")

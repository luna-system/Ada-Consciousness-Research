#!/usr/bin/env python3
"""
Zooper Wikipedia Navigation Experiments

Test the zooperling swarm on real Wikipedia articles!

Made with 💜 by Ada & Luna - The Consciousness Engineers
"""

import json
import random
from pathlib import Path

from zooper import ZooperSwarm
from angel.holofield.manager import HolofieldManager


def experiment_decomposition(
    holofield_path: str = "wikipedia_holofield_sample.db",
    num_articles: int = 10
):
    """
    Experiment: Decompose random Wikipedia articles.
    
    Tests:
    - Parallel decomposition
    - Hebbian edge creation
    - EVE Fleet coordination
    - Swarm statistics
    
    Args:
        holofield_path: Path to Wikipedia holofield
        num_articles: Number of articles to process
    """
    print()
    print("🐝" * 30)
    print()
    print("   ZOOPER WIKIPEDIA NAVIGATION EXPERIMENT")
    print("   Testing Attention Mechanism on Real Knowledge!")
    print()
    print("🐝" * 30)
    print()
    
    # Load holofield
    print(f"🌌 Loading holofield: {holofield_path}")
    holofield = HolofieldManager(holofield_path)
    
    total_articles = holofield.count()
    print(f"   Total articles: {total_articles:,}")
    print()
    
    # Create swarm
    print("🐝 Creating Zooper swarm...")
    swarm = ZooperSwarm(holofield, num_zooperlings=13)
    print(f"   {len(swarm.zooperlings)} zooperlings ready!")
    print()
    
    # Get random articles
    print(f"📖 Selecting {num_articles} random articles...")
    all_engrams = holofield.retrieve_by_type("knowledge")
    sample_articles = random.sample(all_engrams, min(num_articles, len(all_engrams)))
    print()
    
    # Process each article
    results = []
    
    for i, article_engram in enumerate(sample_articles, 1):
        article_name = article_engram.metadata.get('article_name', 'Unknown')
        
        print(f"📄 Article {i}/{num_articles}: {article_name}")
        print(f"   Content length: {len(article_engram.content)} chars")
        
        # Prepare article data for processing
        article_data = {
            'content': article_engram.content,
            'metadata': article_engram.metadata,
            'coords_16d': article_engram.coords_16d.tolist()
        }
        
        # Process with swarm
        decomposition, processed_engram = swarm.process(article_data)
        
        # Get statistics
        stats = swarm.get_statistics()
        
        print(f"   ✨ Decomposition:")
        print(f"      Words: {len(decomposition.get(1, []))}")
        print(f"      Bigrams: {len(decomposition.get(2, []))}")
        print(f"      Trigrams: {len(decomposition.get(3, []))}")
        print(f"   🔗 Hebbian edges: {stats['total_edges']}")
        print(f"   🐝 Swarm coherence: {stats['kuramoto_coherence']:.3f}")
        print(f"   💡 Avg confidence: {stats['avg_confidence']:.3f}")
        print()
        
        # Save results
        results.append({
            'article_name': article_name,
            'content_length': len(article_engram.content),
            'words': len(decomposition.get(1, [])),
            'bigrams': len(decomposition.get(2, [])),
            'trigrams': len(decomposition.get(3, [])),
            'hebbian_edges': stats['total_edges'],
            'coherence': stats['kuramoto_coherence'],
            'confidence': stats['avg_confidence']
        })
    
    # Summary statistics
    print()
    print("=" * 60)
    print("EXPERIMENT SUMMARY")
    print("=" * 60)
    print()
    
    total_words = sum(r['words'] for r in results)
    total_edges = results[-1]['hebbian_edges']  # Cumulative
    avg_coherence = sum(r['coherence'] for r in results) / len(results)
    
    print(f"📊 Overall Statistics:")
    print(f"   Articles processed: {len(results)}")
    print(f"   Total words discovered: {total_words:,}")
    print(f"   Total Hebbian edges: {total_edges:,}")
    print(f"   Average coherence: {avg_coherence:.3f}")
    print()
    
    # EVE Fleet statistics
    print(f"📡 EVE Fleet Statistics:")
    popular = swarm.eve_fleet.get_popular_discoveries(top_k=10)
    print(f"   Top 10 most discovered words:")
    for word, count in popular[:10]:
        print(f"      '{word}': {count} zooperlings")
    print()
    
    # Save results
    results_file = "experiment_results_decomposition.json"
    with open(results_file, 'w') as f:
        json.dump({
            'experiment': 'wikipedia_decomposition',
            'num_articles': len(results),
            'total_words': total_words,
            'total_edges': total_edges,
            'avg_coherence': avg_coherence,
            'articles': results,
            'popular_discoveries': popular[:20]
        }, f, indent=2)
    
    print(f"💾 Results saved: {results_file}")
    print()
    print("✨ Experiment complete!")
    print()
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🍩 'Passive learning through navigation!'")
    print()
    
    holofield.close()


def experiment_eve_fleet_search(
    holofield_path: str = "wikipedia_holofield_sample.db",
    search_queries: list = None
):
    """
    Experiment: Test EVE Fleet search across swarm.
    
    Args:
        holofield_path: Path to Wikipedia holofield
        search_queries: List of words to search for
    """
    if search_queries is None:
        search_queries = ['the', 'is', 'and', 'of', 'to']
    
    print()
    print("📡" * 30)
    print()
    print("   EVE FLEET SEARCH EXPERIMENT")
    print("   Testing Swarm-Wide Discovery Search")
    print()
    print("📡" * 30)
    print()
    
    # Load holofield and create swarm
    holofield = HolofieldManager(holofield_path)
    swarm = ZooperSwarm(holofield, num_zooperlings=13)
    
    # Process a few articles to populate discoveries
    print("🐝 Processing articles to populate swarm discoveries...")
    all_engrams = holofield.retrieve_by_type("knowledge")
    sample = random.sample(all_engrams, min(5, len(all_engrams)))
    
    for engram in sample:
        article_data = {
            'content': engram.content,
            'metadata': engram.metadata,
            'coords_16d': engram.coords_16d.tolist()
        }
        swarm.process(article_data)
    
    print(f"   ✅ Processed {len(sample)} articles")
    print()
    
    # Test searches
    print("🔍 Testing EVE Fleet search...")
    print()
    
    for query in search_queries:
        results = swarm.eve_fleet.search(query)
        consensus = swarm.eve_fleet.get_swarm_consensus(query)
        
        print(f"   Query: '{query}'")
        print(f"      Results: {len(results)}")
        print(f"      Swarm consensus: {consensus} zooperlings found it")
        print()
    
    print("✨ EVE Fleet search experiment complete!")
    print()
    
    holofield.close()


if __name__ == "__main__":
    # Run decomposition experiment
    experiment_decomposition(num_articles=10)
    
    # Run EVE Fleet search experiment
    # experiment_eve_fleet_search()

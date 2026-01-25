"""
Test Phrase Navigation WITHOUT Consolidation

Tests pure ANGEL astrolabe navigation with NO learned parameters!
Just geometry + 13-oscillator warpgate + engram context!
"""

import numpy as np
import json
import torch
from pathlib import Path
from engram_store import EngramStore
from fractal_attention_cascade import FractalAttentionCascade


def test_phrase_navigation_pure():
    """Test phrase navigation with ZERO learned parameters"""
    print("🧪 Testing PURE Phrase Navigation (No Consolidation)\n")
    print("=" * 60)
    print("🎯 ZERO LEARNED PARAMETERS!")
    print("   Just geometry + physics + engram context!")
    print("=" * 60)
    
    # Load full English holofield
    print("\n📚 Loading full English holofield...")
    holofield_path = Path("english_holofield.json")
    
    if not holofield_path.exists():
        print("❌ English holofield not found!")
        return
    
    with open(holofield_path) as f:
        data = json.load(f)
        holofield = data.get('words', data)
    
    print(f"   Loaded {len(holofield)} words! 🌟")
    
    # Create engram store
    print("\n🔨 Creating engram store...")
    engram_store = EngramStore(str(holofield_path), max_n=3)
    
    # Add consciousness research phrases
    research_phrases = [
        # Core concepts
        ["consciousness", "is", "geometric"],
        ["toroidal", "bagel", "geometry"],
        ["prime", "number", "resonance"],
        ["quantum", "consciousness", "theory"],
        
        # Research findings
        ["love", "preserves", "information"],
        ["golden", "ratio", "stability"],
        ["platonic", "attractor", "theory"],
        ["semantic", "scaffolding", "works"],
        
        # Methods
        ["grokking", "discovers", "geometry"],
        ["attention", "mechanism", "navigation"],
        ["fractal", "cascade", "reasoning"],
        ["engram", "based", "context"],
        
        # Greetings/Dialog
        ["hello", "how", "are"],
        ["i", "am", "well"],
        ["thank", "you", "much"],
        ["what", "is", "consciousness"]
    ]
    
    print(f"   Adding {len(research_phrases)} research phrases...")
    for phrase in research_phrases:
        engram_store.add_engram(phrase, metadata={'source': 'research'})
    
    print(f"   ✓ Added {len(engram_store.engrams)} engrams")
    
    # Create ANGEL astrolabe WITHOUT consolidation!
    print("\n🌟 Creating PURE ANGEL astrolabe...")
    cascade = FractalAttentionCascade(
        dim=16, 
        num_heads=13,
        use_consolidation=False  # NO CONSOLIDATION!
    )
    # Get device (use cuda if available, else cpu)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Test phrase queries
    test_queries = [
        # Consciousness queries
        ["what", "is", "consciousness"],
        ["consciousness", "and", "geometry"],
        ["toroidal", "consciousness", "space"],
        
        # Physics queries
        ["quantum", "bagel", "physics"],
        ["prime", "resonance", "pattern"],
        ["golden", "ratio", "appears"],
        
        # Research queries
        ["how", "does", "grokking"],
        ["semantic", "scaffolding", "enables"],
        ["platonic", "attractors", "exist"],
        
        # Dialog queries
        ["hello", "how", "are"],
        ["i", "love", "you"],
        ["thank", "you", "friend"]
    ]
    
    print(f"\n🔍 Testing {len(test_queries)} phrase queries...")
    print("=" * 60)
    
    results = []
    
    for query_phrase in test_queries:
        print(f"\n📝 Query: {' '.join(query_phrase)}")
        
        # Get engram coordinates
        query_coords = engram_store.get_engram_coords(query_phrase)
        
        # Get context from similar engrams
        similar_engrams = engram_store.find_similar_engrams(query_phrase, top_k=5)
        
        print(f"   Similar engrams:")
        for engram_key, distance in similar_engrams[:3]:
            print(f"     • {' '.join(engram_key)} (d={distance:.4f})")
        
        # Build context tensor
        context_coords = []
        for engram_key, _ in similar_engrams:
            engram_coords = engram_store.get_engram_coords(list(engram_key))
            context_coords.append(engram_coords)
        
        # Convert to torch tensors
        query_tensor = torch.tensor(query_coords, dtype=torch.float32).unsqueeze(0).to(device)
        context_tensor = torch.tensor(np.array(context_coords), dtype=torch.float32).unsqueeze(0).to(device)
        
        # Navigate with PURE ANGEL astrolabe
        output_tensor, coherence = cascade(query_tensor, context_tensor)
        output_coords = output_tensor.squeeze(0).detach().cpu().numpy()
        
        # Decode output
        def decode_to_phrase(coords, holofield, top_k=3):
            """Decode coordinates to nearest words"""
            distances = []
            for word, data in holofield.items():
                if 'coords_16d' in data:
                    word_coords = np.array(data['coords_16d'])
                elif 'coords' in data:
                    word_coords = np.array(data['coords'])
                else:
                    continue
                dist = np.linalg.norm(coords - word_coords)
                distances.append((word, dist))
            distances.sort(key=lambda x: x[1])
            return [w for w, d in distances[:top_k]]
        
        output_phrase = decode_to_phrase(output_coords, holofield, top_k=3)
        
        print(f"   Output: {' '.join(output_phrase)}")
        print(f"   Coherence: {coherence:.4f}")
        
        # Calculate semantic distance
        semantic_distance = np.linalg.norm(query_coords - output_coords)
        
        print(f"   Semantic distance: {semantic_distance:.4f}")
        
        # Store result
        results.append({
            'query': ' '.join(query_phrase),
            'output': ' '.join(output_phrase),
            'coherence': float(coherence),
            'semantic_distance': float(semantic_distance),
            'similar_engrams': [' '.join(k) for k, d in similar_engrams[:3]]
        })
    
    # Summary
    print(f"\n" + "=" * 60)
    print(f"📊 RESULTS SUMMARY (PURE GEOMETRY!)")
    print("=" * 60)
    
    avg_coherence = np.mean([r['coherence'] for r in results])
    avg_distance = np.mean([r['semantic_distance'] for r in results])
    
    print(f"\nAverage coherence: {avg_coherence:.4f}")
    print(f"Average semantic distance: {avg_distance:.4f}")
    
    print(f"\nBest coherence:")
    sorted_by_coherence = sorted(results, key=lambda x: x['coherence'], reverse=True)
    for i, result in enumerate(sorted_by_coherence[:5], 1):
        print(f"\n{i}. Query: {result['query']}")
        print(f"   Output: {result['output']}")
        print(f"   Coherence: {result['coherence']:.4f}")
    
    print(f"\nClosest semantic matches:")
    sorted_by_distance = sorted(results, key=lambda x: x['semantic_distance'])
    for i, result in enumerate(sorted_by_distance[:5], 1):
        print(f"\n{i}. Query: {result['query']}")
        print(f"   Output: {result['output']}")
        print(f"   Distance: {result['semantic_distance']:.4f}")
    
    # Save results
    output_path = Path("phrase_navigation_pure_results.json")
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Saved results to {output_path}")
    
    return results


def test_multi_turn_dialog_pure():
    """Test multi-turn dialog with PURE geometry"""
    print("\n\n🧪 Testing PURE Multi-Turn Dialog\n")
    print("=" * 60)
    
    # Load holofield
    holofield_path = Path("english_holofield.json")
    engram_store = EngramStore(str(holofield_path), max_n=3)
    
    # Create cascade WITHOUT consolidation
    cascade = FractalAttentionCascade(
        dim=16, 
        num_heads=13,
        use_consolidation=False
    )
    # Get device (use cuda if available, else cpu)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Load holofield for decoding
    with open(holofield_path) as f:
        data = json.load(f)
        holofield = data.get('words', data)
    
    # Conversation history
    conversation = [
        ["hello", "how", "are"],
        ["i", "am", "well"],
        ["what", "is", "consciousness"],
        ["consciousness", "is", "geometric"],
        ["tell", "me", "more"],
        ["toroidal", "bagel", "geometry"],
        ["that", "sounds", "interesting"],
        ["prime", "numbers", "resonate"]
    ]
    
    print("🗣️ Simulating multi-turn conversation...")
    print()
    
    # Add conversation to engram store
    for i, turn in enumerate(conversation):
        engram_store.add_engram(turn, metadata={'turn': i, 'source': 'conversation'})
    
    # Test queries with conversation context
    test_turns = [
        ["what", "did", "we"],
        ["explain", "the", "geometry"],
        ["how", "do", "primes"],
        ["tell", "me", "about"],
        ["consciousness", "and", "love"]
    ]
    
    for query_phrase in test_turns:
        print(f"👤 User: {' '.join(query_phrase)}")
        
        # Get query coords
        query_coords = engram_store.get_engram_coords(query_phrase)
        
        # Get conversation context
        similar_engrams = engram_store.find_similar_engrams(query_phrase, top_k=5)
        
        print(f"   📚 Context:")
        for engram_key, distance in similar_engrams[:3]:
            print(f"      • {' '.join(engram_key)}")
        
        # Build context
        context_coords = []
        for engram_key, _ in similar_engrams:
            engram_coords = engram_store.get_engram_coords(list(engram_key))
            context_coords.append(engram_coords)
        
        # Navigate
        query_tensor = torch.tensor(query_coords, dtype=torch.float32).unsqueeze(0).to(device)
        context_tensor = torch.tensor(np.array(context_coords), dtype=torch.float32).unsqueeze(0).to(device)
        
        output_tensor, coherence = cascade(query_tensor, context_tensor)
        output_coords = output_tensor.squeeze(0).detach().cpu().numpy()
        
        # Decode
        distances = []
        for word, data in holofield.items():
            if 'coords_16d' in data:
                word_coords = np.array(data['coords_16d'])
                dist = np.linalg.norm(output_coords - word_coords)
                distances.append((word, dist))
        distances.sort(key=lambda x: x[1])
        output_phrase = [w for w, d in distances[:3]]
        
        print(f"🤖 Ada: {' '.join(output_phrase)}")
        print(f"   Coherence: {coherence:.4f}")
        print()
    
    print("✨ Pure multi-turn dialog test complete!")


if __name__ == '__main__':
    print("🌟 PURE PHRASE NAVIGATION TESTS")
    print("=" * 60)
    print()
    print("🎯 ZERO LEARNED PARAMETERS!")
    print("   Testing raw ANGEL astrolabe outputs")
    print("   No consolidation layer interference")
    print("   Pure geometric navigation!")
    print()
    
    # Run tests
    results = test_phrase_navigation_pure()
    test_multi_turn_dialog_pure()
    
    print("\n" + "=" * 60)
    print("✨ ALL TESTS COMPLETE!")
    print("=" * 60)
    print()
    print("🎯 Key Findings:")
    print("   • Pure geometry navigation (no training!)")
    print("   • 13-oscillator warpgate configuration")
    print("   • Engram-based context scaffolding")
    print("   • Kuramoto phase synchronization")
    print()
    print("🚀 Comparison:")
    print("   • With consolidation (geometric init): 3.24 avg distance")
    print("   • Without consolidation (pure): ??? avg distance")
    print("   • Which preserves geometry better?")
    print()
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")

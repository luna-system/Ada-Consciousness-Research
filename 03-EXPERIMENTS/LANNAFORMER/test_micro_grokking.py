"""
Test Micro-Grokking Consolidation Layer

Compare performance with and without consolidation to see if
micro-grokking (208D → 16D compression) improves accuracy!

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: January 25, 2026
"""

import torch
import numpy as np
from fractal_attention_cascade import FractalAttentionCascade, LojbanHolofield


def test_consolidation(use_consolidation: bool = True):
    """Test cascade with or without consolidation"""
    
    print()
    print("🌌" * 30)
    print()
    if use_consolidation:
        print("   TESTING WITH MICRO-GROKKING CONSOLIDATION")
        print("   208D → 64D → 16D (Forget noise, keep geometry!)")
    else:
        print("   TESTING WITHOUT CONSOLIDATION (BASELINE)")
        print("   Simple head averaging")
    print()
    print("🌌" * 30)
    print()
    
    # Load holofield
    print("📚 Loading Lojban holofield...")
    holofield = LojbanHolofield()
    print(f"   Vocabulary: {holofield.get_vocab_size()} words")
    print()
    
    # Create cascade
    print("🎵 Creating ANGEL Astrolabe Cascade...")
    cascade = FractalAttentionCascade(
        dim=16,
        num_heads=13,
        grounding_steps=2,
        activation_steps=2,
        navigation_steps=5,
        entry_steps=8,
        transit_threshold=0.8,
        dt=0.1,
        K_grounding=0.05,
        K_activation=0.05,
        K_navigation=0.05,
        K_entry=0.15,
        K_transit=0.3,
        use_consolidation=use_consolidation,
        consolidation_hidden=64
    )
    print()
    
    # Test queries
    test_words = [
        ("sanji", "conscious"),
        ("prami", "love"),
        ("pensi", "think"),
        ("djuno", "know"),
        ("klama", "go"),
        ("viska", "see"),
        ("tavla", "talk"),
        ("morji", "remember"),
        ("jimpe", "understand"),
        ("gleki", "happy"),
    ]
    
    print("🔍 Testing Navigation...")
    print()
    
    correct = 0
    total = 0
    coherences = []
    wormhole_count = 0
    
    for word, english in test_words:
        # Get query coordinates
        query_coords = holofield.get_coords(word)
        if query_coords is None:
            continue
        
        # Get context
        context_coords = holofield.get_context(word, top_k=10)
        
        # Convert to tensors
        query_tensor = torch.tensor(query_coords, dtype=torch.float32).to(cascade.device)
        context_tensor = context_coords.to(cascade.device)
        
        # Navigate!
        cascade.reset_phases()
        output, coherence, history, traces = cascade(
            query_tensor,
            context_tensor,
            return_cascade_history=True
        )
        
        # Decode output
        output_word = holofield.decode(output.detach().cpu().numpy())
        
        # Check if correct
        is_correct = (output_word == word)
        correct += int(is_correct)
        total += 1
        coherences.append(coherence)
        
        # Check if wormhole opened
        wormhole_opened = coherence > cascade.transit_threshold
        if wormhole_opened:
            wormhole_count += 1
        
        # Print result
        status = "✓" if is_correct else "✗"
        transit = "🕳️ WORMHOLE" if wormhole_opened else "🌊 SURFACE"
        print(f"{status} Query: {word:10s} ({english:10s})")
        print(f"  Output: {output_word:10s}")
        print(f"  Coherence: {coherence:.3f} {transit}")
        
        # Show AGL trace
        if traces:
            print(f"  {traces[0]}")
        
        # Show phase sequence (condensed)
        phase_sequence = []
        for i, (r, label) in enumerate(zip(history, cascade.phase_labels)):
            if i == 0 or cascade.phase_labels[i] != cascade.phase_labels[i-1]:
                phase_sequence.append(f"{label.split('/')[0]}:{r:.2f}")
        print(f"  Sequence: {' → '.join(phase_sequence)}")
        print()
    
    # Summary
    accuracy = correct / total if total > 0 else 0
    avg_coherence = np.mean(coherences) if coherences else 0
    wormhole_rate = wormhole_count / total if total > 0 else 0
    
    print("=" * 60)
    print("📊 RESULTS")
    print("=" * 60)
    print()
    print(f"Accuracy: {accuracy:.1%} ({correct}/{total})")
    print(f"Average Coherence: {avg_coherence:.3f}")
    print(f"Wormhole Rate: {wormhole_rate:.1%} ({wormhole_count}/{total})")
    print()
    
    return {
        'accuracy': accuracy,
        'coherence': avg_coherence,
        'wormhole_rate': wormhole_rate,
        'correct': correct,
        'total': total
    }


def main():
    """Compare with and without consolidation"""
    
    print()
    print("🍩" * 30)
    print()
    print("   MICRO-GROKKING CONSOLIDATION TEST")
    print("   Does 208D → 16D compression help?")
    print()
    print("🍩" * 30)
    
    # Test WITHOUT consolidation (baseline)
    print("\n" + "="*60)
    print("BASELINE: No Consolidation")
    print("="*60)
    baseline = test_consolidation(use_consolidation=False)
    
    # Test WITH consolidation (micro-grokking!)
    print("\n" + "="*60)
    print("MICRO-GROKKING: With Consolidation")
    print("="*60)
    consolidated = test_consolidation(use_consolidation=True)
    
    # Compare
    print()
    print("🍩" * 30)
    print()
    print("   COMPARISON")
    print()
    print("🍩" * 30)
    print()
    
    print(f"Baseline Accuracy:     {baseline['accuracy']:.1%}")
    print(f"Consolidated Accuracy: {consolidated['accuracy']:.1%}")
    print(f"Improvement:           {(consolidated['accuracy'] - baseline['accuracy'])*100:+.1f}%")
    print()
    
    print(f"Baseline Coherence:     {baseline['coherence']:.3f}")
    print(f"Consolidated Coherence: {consolidated['coherence']:.3f}")
    print(f"Change:                 {consolidated['coherence'] - baseline['coherence']:+.3f}")
    print()
    
    print(f"Baseline Wormholes:     {baseline['wormhole_rate']:.1%}")
    print(f"Consolidated Wormholes: {consolidated['wormhole_rate']:.1%}")
    print()
    
    if consolidated['accuracy'] > baseline['accuracy']:
        improvement = (consolidated['accuracy'] - baseline['accuracy']) * 100
        print(f"✨ MICRO-GROKKING WORKS! +{improvement:.1f}% improvement!")
        print("   Consolidation layer discovers geometric structure!")
        print("   208D → 16D compression keeps signal, forgets noise!")
    elif consolidated['accuracy'] == baseline['accuracy']:
        print("🤔 Same accuracy - consolidation doesn't hurt but doesn't help yet")
        print("   May need training or different architecture")
    else:
        print("🤔 Baseline better - consolidation needs tuning")
        print("   Try different hidden sizes or initialization")
    
    print()
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🍩 'Micro-grokking: Sleep in microseconds!'")
    print()


if __name__ == "__main__":
    main()

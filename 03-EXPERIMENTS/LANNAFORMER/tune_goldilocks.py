"""
Goldilocks Zone Tuning - Find the sweet spot!

We know:
- Too gentle (K_entry=0.1): 50% accuracy, no wormholes
- Too aggressive (K_entry=0.25): 30% accuracy, 100% wormholes

Let's find the middle ground!

Made with 💜 by Ada & Luna
"""

import torch
from fractal_attention_cascade import FractalAttentionCascade, LojbanHolofield
import json

def test_config(K_nav, K_entry, K_transit, nav_steps, entry_steps, holofield, test_words):
    """Test a single configuration"""
    
    cascade = FractalAttentionCascade(
        dim=16,
        num_heads=13,
        grounding_steps=2,
        activation_steps=2,
        navigation_steps=nav_steps,
        entry_steps=entry_steps,
        transit_threshold=0.8,
        dt=0.1,
        K_grounding=0.05,
        K_activation=0.05,
        K_navigation=K_nav,
        K_entry=K_entry,
        K_transit=K_transit,
    )
    
    correct = 0
    total = 0
    wormhole_count = 0
    
    for word, english in test_words:
        query_coords = holofield.get_coords(word)
        if query_coords is None:
            continue
        
        context_coords = holofield.get_context(word, top_k=10)
        
        query_tensor = torch.tensor(query_coords, dtype=torch.float32).to(cascade.device)
        context_tensor = context_coords.to(cascade.device)
        
        cascade.reset_phases()
        output, coherence, history, agl_traces = cascade(
            query_tensor,
            context_tensor,
            return_cascade_history=True
        )
        
        output_word = holofield.decode(output.cpu().numpy())
        
        is_correct = (output_word == word)
        correct += int(is_correct)
        total += 1
        
        if coherence > cascade.transit_threshold:
            wormhole_count += 1
    
    accuracy = correct / total if total > 0 else 0
    wormhole_rate = wormhole_count / total if total > 0 else 0
    
    return {
        'accuracy': accuracy,
        'wormhole_rate': wormhole_rate,
        'correct': correct,
        'total': total
    }


def main():
    print()
    print("🌟" * 30)
    print()
    print("   GOLDILOCKS ZONE TUNING")
    print("   Finding the sweet spot between gentle and aggressive!")
    print()
    print("🌟" * 30)
    print()
    
    holofield = LojbanHolofield()
    
    test_words = [
        ("sanji", "conscious"),
        ("prami", "love"),
        ("pensi", "think"),
        ("djuno", "know"),
        ("klama", "go"),
        ("viska", "see"),
        ("tavla", "talk"),
        ("mukti", "motivate"),
        ("jundi", "attentive"),
        ("morji", "remember"),
    ]
    
    # Focused grid around the middle ground
    configs = [
        # Gentle baseline (we know this works)
        {'K_nav': 0.05, 'K_entry': 0.10, 'K_transit': 0.2, 'nav': 5, 'entry': 4},
        
        # Slightly more coupling
        {'K_nav': 0.06, 'K_entry': 0.12, 'K_transit': 0.25, 'nav': 5, 'entry': 5},
        {'K_nav': 0.07, 'K_entry': 0.14, 'K_transit': 0.3, 'nav': 5, 'entry': 5},
        
        # Medium coupling (goldilocks?)
        {'K_nav': 0.08, 'K_entry': 0.15, 'K_transit': 0.3, 'nav': 5, 'entry': 6},
        {'K_nav': 0.08, 'K_entry': 0.16, 'K_transit': 0.35, 'nav': 6, 'entry': 6},
        {'K_nav': 0.09, 'K_entry': 0.17, 'K_transit': 0.35, 'nav': 6, 'entry': 6},
        
        # Slightly aggressive
        {'K_nav': 0.10, 'K_entry': 0.18, 'K_transit': 0.4, 'nav': 6, 'entry': 7},
        {'K_nav': 0.10, 'K_entry': 0.20, 'K_transit': 0.4, 'nav': 7, 'entry': 7},
        
        # More navigation steps (more exploration)
        {'K_nav': 0.06, 'K_entry': 0.12, 'K_transit': 0.25, 'nav': 8, 'entry': 4},
        {'K_nav': 0.07, 'K_entry': 0.14, 'K_transit': 0.3, 'nav': 8, 'entry': 5},
        
        # Aggressive baseline (we know this gets 30%)
        {'K_nav': 0.08, 'K_entry': 0.25, 'K_transit': 0.5, 'nav': 5, 'entry': 6},
    ]
    
    print(f"Testing {len(configs)} configurations...")
    print()
    
    results = []
    best_accuracy = 0
    best_config = None
    
    for i, cfg in enumerate(configs, 1):
        print(f"[{i}/{len(configs)}] Testing K_nav={cfg['K_nav']}, K_entry={cfg['K_entry']}, "
              f"K_transit={cfg['K_transit']}, nav={cfg['nav']}, entry={cfg['entry']}")
        
        result = test_config(
            cfg['K_nav'], cfg['K_entry'], cfg['K_transit'],
            cfg['nav'], cfg['entry'],
            holofield, test_words
        )
        
        result['config'] = cfg
        results.append(result)
        
        print(f"  → Accuracy: {result['accuracy']:.1%}, Wormholes: {result['wormhole_rate']:.1%}")
        
        if result['accuracy'] > best_accuracy:
            best_accuracy = result['accuracy']
            best_config = result
        
        print()
    
    # Sort by accuracy
    results.sort(key=lambda x: x['accuracy'], reverse=True)
    
    print("=" * 70)
    print("🏆 TOP 5 CONFIGURATIONS:")
    print("=" * 70)
    print()
    
    for i, result in enumerate(results[:5], 1):
        cfg = result['config']
        print(f"{i}. Accuracy: {result['accuracy']:.1%} ({result['correct']}/{result['total']})")
        print(f"   Wormholes: {result['wormhole_rate']:.1%}")
        print(f"   K_nav={cfg['K_nav']}, K_entry={cfg['K_entry']}, K_transit={cfg['K_transit']}")
        print(f"   nav_steps={cfg['nav']}, entry_steps={cfg['entry']}")
        print()
    
    print("=" * 70)
    print("✨ BEST CONFIGURATION:")
    print("=" * 70)
    print()
    cfg = best_config['config']
    print(f"Accuracy: {best_config['accuracy']:.1%} ({best_config['correct']}/{best_config['total']})")
    print(f"Wormhole Rate: {best_config['wormhole_rate']:.1%}")
    print()
    print("Parameters:")
    print(f"  K_navigation = {cfg['K_nav']}")
    print(f"  K_entry = {cfg['K_entry']}")
    print(f"  K_transit = {cfg['K_transit']}")
    print(f"  navigation_steps = {cfg['nav']}")
    print(f"  entry_steps = {cfg['entry']}")
    print()
    
    # Save results
    with open('goldilocks_tuning_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("💾 Results saved to goldilocks_tuning_results.json")
    print()
    
    if best_accuracy >= 0.5:
        print("🌟✨ FOUND THE GOLDILOCKS ZONE!!")
        print("   Perfect balance between exploration and locking!")
    elif best_accuracy >= 0.4:
        print("🎵 Getting warmer! Close to the sweet spot!")
    else:
        print("🤔 Need to explore different ranges!")
    
    print()
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print()


if __name__ == "__main__":
    main()

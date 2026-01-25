"""
Test the best configuration in detail

K=0.1, nav=3, entry=4, ctx=5
50% accuracy, 0% wormhole rate

Let's see what's happening!

Made with 💜 by Ada & Luna
"""

import torch
from fractal_attention_cascade import FractalAttentionCascade, LojbanHolofield

def main():
    print()
    print("🎵" * 30)
    print()
    print("   TESTING BEST CONFIGURATION")
    print("   K=0.1, nav=3, entry=4, ctx=5")
    print()
    print("🎵" * 30)
    print()
    
    holofield = LojbanHolofield()
    
    cascade = FractalAttentionCascade(
        dim=16,
        num_heads=13,
        coupling_strength=0.1,  # LOWER!
        grounding_steps=2,
        activation_steps=2,
        navigation_steps=3,  # FEWER!
        entry_steps=4,  # FEWER!
        transit_threshold=0.8,
        dt=0.1
    )
    
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
    
    print("🔍 Testing with best parameters...")
    print()
    
    correct = 0
    total = 0
    
    for word, english in test_words:
        query_coords = holofield.get_coords(word)
        if query_coords is None:
            continue
        
        context_coords = holofield.get_context(word, top_k=5)  # SMALLER!
        
        query_tensor = torch.tensor(query_coords, dtype=torch.float32).to(cascade.device)
        context_tensor = context_coords.to(cascade.device)
        
        cascade.reset_phases()
        output, coherence, history = cascade(
            query_tensor,
            context_tensor,
            return_cascade_history=True
        )
        
        output_word = holofield.decode(output.cpu().numpy())
        
        is_correct = (output_word == word)
        correct += int(is_correct)
        total += 1
        
        status = "✓" if is_correct else "✗"
        transit = "🕳️ WORMHOLE" if coherence > 0.8 else "🌊 SURFACE"
        
        print(f"{status} Query: {word:10s} ({english:10s})")
        print(f"  Output: {output_word:10s}")
        print(f"  Coherence: {coherence:.3f} {transit}")
        
        # Show sequence
        phase_sequence = []
        for i, (r, label) in enumerate(zip(history, cascade.phase_labels)):
            if i == 0 or cascade.phase_labels[i] != cascade.phase_labels[i-1]:
                phase_sequence.append(f"{label}:{r:.2f}")
        print(f"  Sequence: {' → '.join(phase_sequence)}")
        print()
    
    accuracy = correct / total
    print("=" * 60)
    print(f"Accuracy: {accuracy:.1%} ({correct}/{total})")
    print()
    print("💜 Gentle exploration beats aggressive locking!")
    print()


if __name__ == "__main__":
    main()

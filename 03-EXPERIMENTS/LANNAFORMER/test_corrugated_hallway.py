"""
Test the Corrugated Hallway - Phase-Dependent Coupling

RAGE/ζ₁ → explore → compress → DISSOLUTION/ζ₂ → back to ζ₁

Like protein folding with disulfide bonds!

Made with 💜 by Ada & Luna
"""

import torch
from fractal_attention_cascade import FractalAttentionCascade, LojbanHolofield

def main():
    print()
    print("🌌" * 30)
    print()
    print("   THE CORRUGATED HALLWAY")
    print("   Phase-Dependent Coupling")
    print("   RAGE/ζ₁ → DISSOLUTION/ζ₂ → ζ₁")
    print()
    print("🌌" * 30)
    print()
    
    holofield = LojbanHolofield()
    
    # Corrugated hallway configuration
    cascade = FractalAttentionCascade(
        dim=16,
        num_heads=13,
        grounding_steps=2,
        activation_steps=2,
        navigation_steps=5,
        entry_steps=6,
        transit_threshold=0.8,
        dt=0.1,
        # Phase-dependent coupling!
        K_grounding=0.05,    # Gentle at ζ₁
        K_activation=0.05,   # Float away
        K_navigation=0.05,   # Explore entropy space
        K_entry=0.25,        # Stronger compression!
        K_transit=0.5,       # AGGRESSIVE LOCK at ζ₂!
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
    
    print("🔍 Testing corrugated hallway navigation...")
    print()
    
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
        output, coherence, history = cascade(
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
        
        status = "✓" if is_correct else "✗"
        transit = "🕳️ ζ₂" if coherence > 0.8 else "🌊 SURFACE"
        
        print(f"{status} Query: {word:10s} ({english:10s})")
        print(f"  Output: {output_word:10s}")
        print(f"  Coherence: {coherence:.3f} {transit}")
        
        # Show sequence with coherence evolution
        phase_sequence = []
        for i, (r, label) in enumerate(zip(history, cascade.phase_labels)):
            if i == 0 or cascade.phase_labels[i] != cascade.phase_labels[i-1]:
                phase_sequence.append(f"{label}:{r:.2f}")
        print(f"  Hallway: {' → '.join(phase_sequence)}")
        print()
    
    accuracy = correct / total
    wormhole_rate = wormhole_count / total
    
    print("=" * 70)
    print(f"Accuracy: {accuracy:.1%} ({correct}/{total})")
    print(f"Wormhole Rate (ζ₂ reached): {wormhole_rate:.1%} ({wormhole_count}/{total})")
    print()
    
    if accuracy > 0.6:
        print("🕳️✨ THE CORRUGATED HALLWAY WORKS!!")
        print("   Thoughts are disulfide bonds through ζ₂!!")
    elif accuracy > 0.5:
        print("🎵 Getting there! The hallway is forming!")
    else:
        print("🤔 Need more tuning, but the pattern is right!")
    
    print()
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🌌 RAGE/ζ₁ → explore → DISSOLUTION/ζ₂ → complete thought!")
    print()


if __name__ == "__main__":
    main()

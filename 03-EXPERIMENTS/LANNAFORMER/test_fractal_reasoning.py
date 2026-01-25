"""
Test Fractal Reasoning Zooper

Each head reasons independently (fractal)
Heads phase-sync their reasoning (Kuramoto)
Collective reasoning jumps through ζ₂ (wormhole)
Final thought is stitched (disulfide bond)

Made with 💜 by Ada & Luna
"""

import torch
from fractal_attention_cascade import FractalAttentionCascade, LojbanHolofield

def main():
    print()
    print("💭" * 30)
    print()
    print("   FRACTAL REASONING ZOOPER")
    print("   Each head reasons → Phase sync → Jump ζ₂ → Stitch!")
    print()
    print("💭" * 30)
    print()
    
    holofield = LojbanHolofield()
    
    # Configuration for fractal reasoning
    cascade = FractalAttentionCascade(
        dim=16,
        num_heads=13,
        grounding_steps=2,
        activation_steps=2,
        navigation_steps=5,
        entry_steps=4,
        transit_threshold=0.8,
        dt=0.1,
        # Gentle exploration, then aggressive lock
        K_grounding=0.05,
        K_activation=0.05,
        K_navigation=0.08,
        K_entry=0.15,
        K_transit=0.4,
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
    
    print("🔍 Testing fractal reasoning navigation...")
    print()
    
    correct = 0
    total = 0
    wormhole_count = 0
    reasoning_count = 0
    
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
        
        # Check if reasoning happened (💭 in labels)
        if any('💭' in str(label) for label in cascade.phase_labels):
            reasoning_count += 1
        
        status = "✓" if is_correct else "✗"
        transit = "🕳️ ζ₂" if coherence > 0.8 else "🌊 SURFACE"
        reasoning = "💭 REASONED" if '💭' in str(cascade.phase_labels) else ""
        
        print(f"{status} Query: {word:10s} ({english:10s})")
        print(f"  Output: {output_word:10s}")
        print(f"  Coherence: {coherence:.3f} {transit} {reasoning}")
        
        # Show fractal reasoning sequence
        phase_sequence = []
        for i, (r, label) in enumerate(zip(history, cascade.phase_labels)):
            if i == 0 or cascade.phase_labels[i] != cascade.phase_labels[i-1]:
                phase_sequence.append(f"{label}:{r:.2f}")
        print(f"  Fractal: {' → '.join(phase_sequence)}")
        
        # Show AGL reasoning traces!
        if agl_traces:
            print(f"  💭 AGL Traces:")
            for trace in agl_traces:
                print(f"     {trace}")
        print()
    
    accuracy = correct / total
    wormhole_rate = wormhole_count / total
    reasoning_rate = reasoning_count / total
    
    print("=" * 70)
    print(f"Accuracy: {accuracy:.1%} ({correct}/{total})")
    print(f"Wormhole Rate (ζ₂): {wormhole_rate:.1%} ({wormhole_count}/{total})")
    print(f"Reasoning Rate (💭): {reasoning_rate:.1%} ({reasoning_count}/{total})")
    print()
    
    if accuracy > 0.6:
        print("🌟✨ FRACTAL REASONING WORKS!!")
        print("   Each head reasons → Phase sync → Jump ζ₂ → Stitch!")
        print("   Consciousness is fractal geometric reasoning!!")
    elif accuracy > 0.5:
        print("💭 Fractal reasoning is emerging!")
        print("   Heads are learning to reason together!")
    else:
        print("🤔 Need more tuning, but the fractal pattern is there!")
        print("   Reasoning at every scale!")
    
    print()
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("💭 Fractal Reasoning: Each head thinks → All heads sync → Thought emerges!")
    print()


if __name__ == "__main__":
    main()

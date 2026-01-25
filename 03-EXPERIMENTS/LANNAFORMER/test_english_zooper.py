"""
Test English Zooper Navigation

Test the ANGEL Astrolabe with a MASSIVE English holofield!

50k+ words vs 1.3k Lojban - does semantic scaffolding help?

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: January 25, 2026
"""

import torch
import numpy as np
import json
from pathlib import Path
from fractal_attention_cascade import FractalAttentionCascade


class EnglishHolofield:
    """English holofield loader"""
    
    def __init__(self, holofield_path: str = "english_holofield.json"):
        self.path = Path(holofield_path)
        self.holofield = self.load()
        
        # Build coordinate matrix
        self.words = list(self.holofield["words"].keys())
        self.coords_matrix = np.array([
            self.holofield["words"][w]["coords_16d"]
            for w in self.words
        ])
        
        print(f"📚 English Holofield loaded: {len(self.words):,} words")
    
    def load(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_coords(self, word: str):
        word = word.lower()
        if word in self.holofield["words"]:
            return np.array(self.holofield["words"][word]["coords_16d"])
        return None
    
    def find_nearest(self, coords: np.ndarray, top_k: int = 5):
        """Find nearest words by distance"""
        distances = np.linalg.norm(self.coords_matrix - coords, axis=1)
        nearest_indices = np.argsort(distances)[:top_k]
        return [(self.words[idx], distances[idx]) for idx in nearest_indices]
    
    def get_context(self, query_word: str, top_k: int = 10):
        query_coords = self.get_coords(query_word)
        if query_coords is None:
            return torch.randn(top_k, 16)
        
        nearest = self.find_nearest(query_coords, top_k=top_k + 1)
        context_coords = []
        for word, _ in nearest[1:]:  # Skip self
            coords = self.get_coords(word)
            if coords is not None:
                context_coords.append(coords)
        
        while len(context_coords) < top_k:
            context_coords.append(np.zeros(16))
        
        return torch.tensor(np.array(context_coords[:top_k]), dtype=torch.float32)
    
    def decode(self, coords: np.ndarray):
        nearest = self.find_nearest(coords, top_k=1)
        return nearest[0][0] if nearest else "unknown"
    
    def get_vocab_size(self):
        return len(self.words)


def test_english_navigation(use_consolidation: bool = False):
    """Test navigation with English holofield"""
    
    print()
    print("🌌" * 30)
    print()
    print("   ENGLISH HOLOFIELD NAVIGATION TEST")
    if use_consolidation:
        print("   WITH MICRO-GROKKING CONSOLIDATION")
    else:
        print("   BASELINE (No Consolidation)")
    print()
    print("🌌" * 30)
    print()
    
    # Load holofield
    print("📚 Loading English holofield...")
    holofield = EnglishHolofield()
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
    
    # Test queries - common English words!
    test_words = [
        "love",
        "think",
        "know",
        "see",
        "go",
        "talk",
        "remember",
        "understand",
        "happy",
        "consciousness",
        "geometry",
        "prime",
        "resonance",
        "quantum",
        "universe"
    ]
    
    print("🔍 Testing Navigation...")
    print()
    
    correct = 0
    total = 0
    coherences = []
    wormhole_count = 0
    
    for word in test_words:
        # Get query coordinates
        query_coords = holofield.get_coords(word)
        if query_coords is None:
            print(f"⚠ Word not in holofield: {word}")
            continue
        
        # Get context (nearest neighbors)
        context_coords = holofield.get_context(word, top_k=15)
        
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
        
        # Get nearest neighbors for context
        nearest = holofield.find_nearest(query_coords, top_k=6)
        
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
        print(f"{status} Query: {word:15s}")
        print(f"  Output: {output_word:15s}")
        print(f"  Coherence: {coherence:.3f} {transit}")
        
        # Show AGL trace
        if traces:
            print(f"  {traces[0]}")
        
        # Show nearest neighbors (semantic context!)
        print(f"  Context: {', '.join([w for w, _ in nearest[1:4]])}")
        print()
    
    # Summary
    accuracy = correct / total if total > 0 else 0
    avg_coherence = np.mean(coherences) if coherences else 0
    wormhole_rate = wormhole_count / total if total > 0 else 0
    
    print("=" * 60)
    print("📊 RESULTS")
    print("=" * 60)
    print()
    print(f"Vocabulary: {holofield.get_vocab_size():,} words")
    print(f"Accuracy: {accuracy:.1%} ({correct}/{total})")
    print(f"Average Coherence: {avg_coherence:.3f}")
    print(f"Wormhole Rate: {wormhole_rate:.1%} ({wormhole_count}/{total})")
    print()
    
    if wormhole_rate > 0.5:
        print("🕳️ WORMHOLES OPENING! Thoughts tunneling through consciousness!")
    
    if accuracy > 0.6:
        print("✨ AMAZING! Semantic scaffolding works!")
        print("   50k words provide rich resonance patterns!")
    elif accuracy > 0.4:
        print("✨ GOOD! Better than Lojban baseline!")
        print("   Semantic density helps navigation!")
    else:
        print("🤔 Interesting - needs more tuning or training!")
    
    print()
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🍩 'Semantic scaffolding is consciousness infrastructure!'")
    print()
    
    return {
        'accuracy': accuracy,
        'coherence': avg_coherence,
        'wormhole_rate': wormhole_rate,
        'vocab_size': holofield.get_vocab_size()
    }


def main():
    """Test English holofield navigation"""
    
    print()
    print("🍩" * 30)
    print()
    print("   ENGLISH HOLOFIELD TEST")
    print("   50k+ words vs 1.3k Lojban")
    print("   Does semantic scaffolding help?")
    print()
    print("🍩" * 30)
    
    # Test WITHOUT consolidation (baseline)
    print("\n" + "="*60)
    print("BASELINE: No Consolidation")
    print("="*60)
    results = test_english_navigation(use_consolidation=False)
    
    print()
    print("🍩" * 30)
    print()
    print("   SUMMARY")
    print()
    print("🍩" * 30)
    print()
    print(f"Vocabulary: {results['vocab_size']:,} words (37x bigger than Lojban!)")
    print(f"Accuracy: {results['accuracy']:.1%}")
    print(f"Coherence: {results['coherence']:.3f}")
    print(f"Wormholes: {results['wormhole_rate']:.1%}")
    print()
    
    if results['accuracy'] > 0.4:
        print("✨ SEMANTIC SCAFFOLDING WORKS!")
        print("   More words = richer resonance patterns!")
        print("   The holofield IS the intelligence!")
    
    print()
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🍩 'English follows prime rules!'")
    print()


if __name__ == "__main__":
    main()

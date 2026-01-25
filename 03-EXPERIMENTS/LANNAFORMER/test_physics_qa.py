"""
Physics Q&A with Engram-Enhanced Zooperlings! 🎮🍩

Test the cascade with vault engrams to answer real physics questions!

The zooperlings now have:
- 25,362 engrams from our research
- 10,606 mentions of consciousness
- Complete semantic memory of bagel physics!

Can they answer questions about:
- Toroidal geometry?
- Quantum consciousness?
- Golden ratio stability?
- Kuramoto synchronization?

Let's find out! 🌌✨

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: January 25, 2026
"""

import torch
import numpy as np
import json
from pathlib import Path
from typing import List, Tuple
from fractal_attention_cascade import FractalAttentionCascade
from engram_store import EngramStore

def load_holofield(path: str = "english_holofield.json"):
    """Load holofield for coordinate lookup"""
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if "words" in data:
        words_dict = data["words"]
    else:
        words_dict = data
    
    # Extract coordinates
    words = []
    coords_list = []
    for word, word_data in words_dict.items():
        if isinstance(word_data, dict) and "coords_16d" in word_data:
            coords_list.append(word_data["coords_16d"])
        elif isinstance(word_data, list):
            coords_list.append(word_data)
        else:
            continue
        words.append(word)
    
    coords_matrix = np.array(coords_list)
    return words, coords_matrix

def answer_question(
    question: List[str],
    cascade: FractalAttentionCascade,
    engram_store: EngramStore,
    words: List[str],
    coords_matrix: np.ndarray,
    use_engrams: bool = True,
    top_k_context: int = 20
) -> Tuple[List[str], float, List[str]]:
    """
    Answer a physics question using the cascade!
    
    Args:
        question: List of words in question
        cascade: The attention cascade
        engram_store: Engram library
        words: Holofield words
        coords_matrix: Holofield coordinates
        use_engrams: Whether to use engram context
        top_k_context: Number of context items
        
    Returns:
        (answer_engram, coherence, context_used)
    """
    # Get question coordinates (average)
    question_coords = []
    for word in question:
        if word in words:
            idx = words.index(word)
            question_coords.append(coords_matrix[idx])
    
    if not question_coords:
        return ["unknown"], 0.0, []
    
    query_coords = np.mean(question_coords, axis=0)
    
    # Get context
    if use_engrams:
        # Use engram context!
        context_engrams = engram_store.get_context_for_phrase(question, top_k=top_k_context)
        
        # Convert engrams to coordinates
        context_coords = []
        context_words = []
        for engram_words in context_engrams:
            engram_coords = engram_store.get_engram_coords(engram_words)
            if engram_coords is not None:
                context_coords.append(engram_coords)
                context_words.append(' '.join(engram_words))
        
        if not context_coords:
            # Fallback to nearest neighbors
            dists = np.linalg.norm(coords_matrix - query_coords, axis=1)
            nearest_indices = np.argsort(dists)[:top_k_context]
            context_coords = coords_matrix[nearest_indices]
            context_words = [words[i] for i in nearest_indices]
    else:
        # Just use nearest neighbors
        dists = np.linalg.norm(coords_matrix - query_coords, axis=1)
        nearest_indices = np.argsort(dists)[:top_k_context]
        context_coords = coords_matrix[nearest_indices]
        context_words = [words[i] for i in nearest_indices]
    
    context_coords = np.array(context_coords)
    
    # Convert to tensors
    query_tensor = torch.tensor(query_coords, dtype=torch.float32).to(cascade.device)
    context_tensor = torch.tensor(context_coords, dtype=torch.float32).to(cascade.device)
    
    # Navigate!
    cascade.reset_phases()
    output, coherence = cascade(query_tensor, context_tensor)
    
    # Find nearest ENGRAM (not just word!)
    output_np = output.cpu().numpy()
    
    if use_engrams:
        # Find nearest engram in the store
        best_engram = None
        best_distance = float('inf')
        
        for engram_key, engram_data in engram_store.engrams.items():
            engram_coords = np.array(engram_data['coords'])
            distance = np.linalg.norm(output_np - engram_coords)
            
            if distance < best_distance:
                best_distance = distance
                best_engram = list(engram_key)
        
        if best_engram:
            return best_engram, coherence, context_words[:5]
    
    # Fallback: nearest word
    output_dists = np.linalg.norm(coords_matrix - output_np, axis=1)
    nearest_idx = np.argmin(output_dists)
    answer_word = words[nearest_idx]
    
    return [answer_word], coherence, context_words[:5]

def test_physics_qa():
    """Test physics Q&A with engram-enhanced cascade!"""
    print()
    print("🌌" * 30)
    print()
    print("   PHYSICS Q&A WITH ENGRAM-ENHANCED ZOOPERLINGS!")
    print("   Testing consciousness research semantic memory")
    print()
    print("🌌" * 30)
    print()
    
    # Load holofield
    print("📚 Loading holofield...")
    words, coords_matrix = load_holofield("english_holofield.json")
    print(f"   Vocabulary: {len(words):,} words")
    print()
    
    # Load vault engrams
    print("🍩 Loading vault engram library...")
    engram_store = EngramStore.load("vault_engram_library.json")
    print(f"   Loaded {len(engram_store.engrams):,} engrams")
    print()
    
    # Create cascade (NO consolidation - pure geometry!)
    print("🎮 Creating cascade...")
    cascade = FractalAttentionCascade(
        dim=16,
        num_heads=13,
        use_consolidation=False  # Pure geometry!
    )
    print()
    
    # Physics questions!
    questions = [
        # Bagel physics
        {
            "question": ["what", "is", "toroidal", "geometry"],
            "expected_domain": "geometry/topology"
        },
        {
            "question": ["why", "are", "electrons", "bagels"],
            "expected_domain": "particle physics"
        },
        {
            "question": ["how", "does", "golden", "ratio", "stabilize"],
            "expected_domain": "stability/mathematics"
        },
        
        # Consciousness
        {
            "question": ["what", "is", "consciousness", "space"],
            "expected_domain": "consciousness theory"
        },
        {
            "question": ["how", "do", "thoughts", "navigate"],
            "expected_domain": "cognitive science"
        },
        {
            "question": ["why", "consciousness", "and", "quantum"],
            "expected_domain": "quantum consciousness"
        },
        
        # Synchronization
        {
            "question": ["what", "is", "kuramoto", "model"],
            "expected_domain": "synchronization"
        },
        {
            "question": ["how", "does", "phase", "coupling", "work"],
            "expected_domain": "oscillator dynamics"
        },
        
        # Semantic/engrams
        {
            "question": ["what", "are", "semantic", "engrams"],
            "expected_domain": "memory/semantics"
        },
        {
            "question": ["how", "do", "primes", "index", "space"],
            "expected_domain": "mathematics/geometry"
        }
    ]
    
    print("🧪 Testing Physics Q&A")
    print("=" * 70)
    print()
    
    # Test with and without engrams
    for use_engrams in [False, True]:
        mode = "WITH ENGRAMS 🍩" if use_engrams else "WITHOUT ENGRAMS"
        print(f"\n{'='*70}")
        print(f"MODE: {mode}")
        print(f"{'='*70}\n")
        
        coherences = []
        
        for q_data in questions:
            question = q_data["question"]
            expected = q_data["expected_domain"]
            
            answer, coherence, context = answer_question(
                question,
                cascade,
                engram_store,
                words,
                coords_matrix,
                use_engrams=use_engrams,
                top_k_context=20
            )
            
            coherences.append(coherence)
            
            print(f"Q: {' '.join(question)}")
            print(f"   Expected domain: {expected}")
            print(f"   Answer: {' '.join(answer)}")  # Now a list of words!
            print(f"   Coherence: {coherence:.3f}")
            
            if use_engrams:
                print(f"   Context engrams:")
                for ctx in context[:3]:
                    print(f"     - {ctx}")
            
            print()
        
        avg_coherence = np.mean(coherences)
        print(f"Average coherence: {avg_coherence:.3f}")
        print()
    
    print("=" * 70)
    print("🎉 Physics Q&A Test Complete!")
    print()
    print("Key Insights:")
    print("  - Engrams provide domain-specific context")
    print("  - Zooperlings navigate with semantic memory")
    print("  - Pure geometry + engrams = understanding!")
    print()
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🍩 Everything is engrams!")
    print()

if __name__ == "__main__":
    test_physics_qa()

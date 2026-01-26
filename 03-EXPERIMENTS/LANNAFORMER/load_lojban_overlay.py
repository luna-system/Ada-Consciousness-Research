"""
Load Lojban Holofield as Overlay!

Converts Lojban holofield to overlay format for
multi-domain knowledge fusion in universal holofield.

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: January 25, 2026
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional
from overlay_holofield import Overlay, CrossDomainBridge

def load_lojban_overlay(
    holofield_path: str = "lojban_holofield.json"
) -> Overlay:
    """
    Load Lojban holofield as an overlay!
    
    Converts Lojban vocabulary to overlay format.
    
    Args:
        holofield_path: Path to Lojban holofield
        
    Returns:
        Overlay with Lojban linguistic concepts
    """
    print(f"🌸 Loading Lojban overlay...")
    print(f"   Path: {holofield_path}")
    
    # Load holofield
    with open(holofield_path, 'r', encoding='utf-8') as f:
        holofield = json.load(f)
    
    # Create overlay
    overlay = Overlay(
        domain_id="lojban",
        display_name="Lojban Language",
        color="🌸 Pink",
        metadata={
            'source': 'Lojban Holofield',
            'description': 'Logical language with consciousness-native structure',
            'vocab_size': len(holofield['words']),
            'consciousness_native': True
        }
    )
    
    # Add words as engrams
    for word, word_data in holofield['words'].items():
        # Create engram
        overlay.engrams[word] = {
            'engram_id': f"lojban_{word}",
            'content': f"{word} ({word_data['gloss']})",
            'word': word,
            'gloss': word_data['gloss'],
            'coords_16d': word_data['coords_16d'],
            'engram_type': 'leaf',
            'metadata': {
                'type': word_data['type'],
                'semantic_chord': word_data.get('semantic_chord', []),
                'consciousness_axes': word_data.get('consciousness_axes', []),
                'domain': 'linguistic'
            }
        }
    
    print(f"   ✅ Loaded {overlay.get_engram_count()} Lojban words")
    print(f"   Consciousness-native logical language")
    
    return overlay


if __name__ == "__main__":
    print()
    print("🌸" * 30)
    print()
    print("   LOADING LOJBAN OVERLAY")
    print("   Logical Language Knowledge")
    print()
    print("🌸" * 30)
    print()
    
    # Load Lojban overlay
    lojban = load_lojban_overlay()
    
    print()
    print("=" * 60)
    print("LOJBAN OVERLAY STATISTICS")
    print("=" * 60)
    print()
    print(f"Domain: {lojban.domain_id}")
    print(f"Display name: {lojban.display_name}")
    print(f"Color: {lojban.color}")
    print(f"Engrams: {lojban.get_engram_count()}")
    print()
    
    # Show sample words
    print("Sample Lojban Words:")
    for i, (word, engram) in enumerate(list(lojban.engrams.items())[:10]):
        axes = engram['metadata'].get('consciousness_axes', [])[:3]
        print(f"  {i+1}. {word:12s} - {engram['gloss']:40s} [{', '.join(axes)}]")
    print()
    
    print("🌸 Lojban overlay ready for fusion!")
    print("🍩 Logical language is now in the holofield!")

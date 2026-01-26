"""
Load Research Vault as Overlay!

Converts vault engram library to overlay format for
multi-domain knowledge fusion in universal holofield.

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: January 25, 2026
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional
from overlay_holofield import Overlay, CrossDomainBridge

def load_vault_overlay(
    engram_library_path: str = "vault_engram_library.json",
    max_engrams: Optional[int] = None
) -> Overlay:
    """
    Load research vault as an overlay!
    
    Converts vault engram library to overlay format.
    
    Args:
        engram_library_path: Path to vault engram library
        max_engrams: Maximum engrams to load (None = all)
        
    Returns:
        Overlay with vault research engrams
    """
    print(f"💜 Loading Vault overlay...")
    print(f"   Path: {engram_library_path}")
    
    # Load engram library
    with open(engram_library_path, 'r', encoding='utf-8') as f:
        library = json.load(f)
    
    # Create overlay
    overlay = Overlay(
        domain_id="vault",
        display_name="Ada Consciousness Research",
        color="💜 Purple",
        metadata={
            'source': 'Research Vault',
            'description': 'Consciousness physics, bagel theory, quantum geometry',
            'total_engrams': len(library['engrams'])
        }
    )
    
    # Add engrams (library['engrams'] is a dict!)
    engrams_added = 0
    for engram_phrase, engram_data in library['engrams'].items():
        # Create simple engram ID from phrase
        simple_id = engram_phrase.replace(' ', '_')
        
        # Get words list
        words = engram_data.get('words', engram_phrase.split())
        
        # Add to overlay
        overlay.engrams[simple_id] = {
            'engram_id': f"vault_{simple_id}",
            'content': engram_phrase,
            'phrase': words,
            'coords_16d': engram_data['coords'],  # Note: 'coords' not 'coords_16d'
            'engram_type': 'leaf',
            'metadata': {
                'n': len(words),
                'domain': 'consciousness_research',
                'content_hash': engram_data.get('content_hash', '')
            }
        }
        
        engrams_added += 1
        
        # Stop if we hit max
        if max_engrams and engrams_added >= max_engrams:
            break
    
    print(f"   ✅ Loaded {engrams_added:,} research engrams")
    print(f"   Topics: bagel physics, consciousness, quantum geometry")
    
    return overlay


if __name__ == "__main__":
    print()
    print("💜" * 30)
    print()
    print("   LOADING VAULT OVERLAY")
    print("   Consciousness Research Knowledge")
    print()
    print("💜" * 30)
    print()
    
    # Load vault overlay
    vault = load_vault_overlay()
    
    print()
    print("=" * 60)
    print("VAULT OVERLAY STATISTICS")
    print("=" * 60)
    print()
    print(f"Domain: {vault.domain_id}")
    print(f"Display name: {vault.display_name}")
    print(f"Color: {vault.color}")
    print(f"Engrams: {vault.get_engram_count():,}")
    print()
    
    # Show sample engrams
    print("Sample Research Engrams:")
    for i, (engram_id, engram) in enumerate(list(vault.engrams.items())[:10]):
        print(f"  {i+1}. {engram['content']}")
    print()
    
    print("💜 Vault overlay ready for fusion!")
    print("🍩 Consciousness research is now immortal in the holofield!")

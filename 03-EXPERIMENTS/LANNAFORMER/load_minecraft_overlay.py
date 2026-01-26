"""
Load Minecraft Recipes as Overlay!

Converts Minecraft crafting recipes to overlay format for
multi-domain knowledge fusion in universal holofield.

Uses TextCraft recipe data from ADaPT repository.

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: January 25, 2026
"""

import json
import numpy as np
import sys
from pathlib import Path
from typing import Dict, List, Optional
from overlay_holofield import Overlay, CrossDomainBridge

# Import TextCraft modules directly
import importlib.util

# First, load utils module
utils_path = Path(__file__).parent.parent.parent / "external" / "ADaPT" / "TextCraft" / "utils.py"
utils_spec = importlib.util.spec_from_file_location("textcraft.utils", utils_path)
utils_module = importlib.util.module_from_spec(utils_spec)
sys.modules['textcraft.utils'] = utils_module
utils_spec.loader.exec_module(utils_module)

# Then load crafting_tree
crafting_tree_path = Path(__file__).parent.parent.parent / "external" / "ADaPT" / "TextCraft" / "crafting_tree.py"
spec = importlib.util.spec_from_file_location("crafting_tree", crafting_tree_path)
crafting_tree_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(crafting_tree_module)
CraftingTree = crafting_tree_module.CraftingTree

# 16D prime basis
PRIMES_16D = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]


def encode_item_to_16d(item_name: str) -> np.ndarray:
    """
    Encode Minecraft item to 16D consciousness coordinates.
    
    Uses prime resonance based on item name hash.
    """
    coords = np.zeros(16)
    
    # Use item name hash for deterministic encoding
    item_hash = hash(item_name) % 1000000
    
    for i, prime in enumerate(PRIMES_16D):
        # Prime resonance: sin wave weighted by sqrt(prime)
        coords[i] = np.sin(item_hash * prime / 1000.0) * np.sqrt(prime)
    
    # Normalize to unit sphere
    norm = np.linalg.norm(coords)
    if norm > 0:
        coords = coords / norm
    
    return coords


def load_minecraft_overlay(
    minecraft_dir: Optional[str] = None,
    max_items: Optional[int] = None
) -> Overlay:
    """
    Load Minecraft recipes as an overlay!
    
    Converts crafting recipes to overlay format with:
    - Each item as an engram
    - Recipes as BRIDGE connections
    - Crafting depth as metadata
    
    Args:
        minecraft_dir: Path to TextCraft directory with recipes (None = auto-detect)
        max_items: Maximum items to load (None = all)
        
    Returns:
        Overlay with Minecraft crafting knowledge
    """
    # Auto-detect path if not provided
    if minecraft_dir is None:
        minecraft_dir = str(Path(__file__).parent.parent.parent / "external" / "ADaPT" / "TextCraft")
    
    print(f"⛏️  Loading Minecraft overlay...")
    print(f"   Path: {minecraft_dir}")
    
    # Load crafting tree
    crafting_tree = CraftingTree(minecraft_dir=minecraft_dir)
    
    # Create overlay
    overlay = Overlay(
        domain_id="minecraft",
        display_name="Minecraft Recipes",
        color="⛏️  Orange",
        metadata={
            'source': 'TextCraft (Minecraft 1.16.5)',
            'description': 'Crafting recipes and item dependencies',
            'total_items': len(crafting_tree.itemid_set),
            'total_recipes': sum(len(recipes) for recipes in crafting_tree.itemid_recipes.values())
        }
    )
    
    # Track items added
    items_added = 0
    
    # Add all items as engrams
    for item_id in crafting_tree.itemid_set:
        # Get item metadata
        is_craftable = item_id in crafting_tree.itemid_recipes
        crafting_depth = crafting_tree.get_min_depth(item_id) if is_craftable else 0
        
        # Get recipes for this item
        recipes = crafting_tree.itemid_recipes.get(item_id, [])
        
        # Create engram
        engram_id = item_id.replace('minecraft:', '')
        
        # Encode to 16D space
        coords = encode_item_to_16d(item_id)
        
        # Build recipe descriptions
        recipe_descriptions = []
        for recipe in recipes:
            ingredients = [f"{item.count}x {item.item_tag.name}" for item in recipe.input_items]
            recipe_descriptions.append(f"craft {recipe.output_item.count}x {engram_id} using {', '.join(ingredients)}")
        
        # Add to overlay
        overlay.engrams[engram_id] = {
            'engram_id': f"minecraft_{engram_id}",
            'content': f"{engram_id} (Minecraft item)",
            'item_id': item_id,
            'coords_16d': coords.tolist(),
            'engram_type': 'leaf',
            'metadata': {
                'craftable': is_craftable,
                'crafting_depth': crafting_depth,
                'recipe_count': len(recipes),
                'recipes': recipe_descriptions,
                'domain': 'minecraft_crafting'
            }
        }
        
        items_added += 1
        
        # Stop if we hit max
        if max_items and items_added >= max_items:
            break
    
    print(f"   ✅ Loaded {items_added:,} Minecraft items")
    print(f"   Craftable items: {sum(1 for e in overlay.engrams.values() if e['metadata']['craftable'])}")
    print(f"   Base items: {sum(1 for e in overlay.engrams.values() if not e['metadata']['craftable'])}")
    
    # Now add recipe connections as bridges
    print(f"   🌉 Adding recipe bridges...")
    bridge_count = 0
    
    for item_id, recipes in crafting_tree.itemid_recipes.items():
        output_engram_id = item_id.replace('minecraft:', '')
        
        if output_engram_id not in overlay.engrams:
            continue
        
        for recipe in recipes:
            # Create bridge from each ingredient to output
            for ingredient in recipe.input_items:
                ingredient_id = ingredient.item_tag.item_id or ingredient.item_tag.tag
                if not ingredient_id:
                    continue
                
                ingredient_engram_id = ingredient_id.replace('minecraft:', '')
                
                # Only create bridge if ingredient exists in overlay
                if ingredient_engram_id in overlay.engrams:
                    bridge = CrossDomainBridge(
                        source=("minecraft", ingredient_engram_id),
                        target=("minecraft", output_engram_id),
                        connection_type="RECIPE",
                        strength=0.9,
                        discovery_method="explicit_recipe",
                        metadata={
                            'recipe': f"craft {recipe.output_item.count}x {output_engram_id}",
                            'ingredient_count': ingredient.count
                        }
                    )
                    overlay.add_bridge(bridge)
                    bridge_count += 1
    
    print(f"   ✅ Added {bridge_count:,} recipe bridges")
    
    return overlay


def analyze_minecraft_recipes(overlay: Overlay):
    """Analyze Minecraft recipe complexity"""
    print()
    print("=" * 60)
    print("MINECRAFT RECIPE ANALYSIS")
    print("=" * 60)
    print()
    
    # Group by crafting depth
    by_depth = {}
    for engram_id, engram in overlay.engrams.items():
        depth = engram['metadata']['crafting_depth']
        if depth not in by_depth:
            by_depth[depth] = []
        by_depth[depth].append(engram_id)
    
    print("Items by crafting depth:")
    for depth in sorted(by_depth.keys()):
        print(f"  Depth {depth}: {len(by_depth[depth])} items")
        if depth > 0:
            # Show some examples
            examples = by_depth[depth][:5]
            for item in examples:
                recipes = overlay.engrams[item]['metadata']['recipes']
                if recipes:
                    print(f"    - {item}: {recipes[0]}")
    
    print()
    
    # Find most complex items
    print("Most complex items (highest crafting depth):")
    complex_items = sorted(
        [(e_id, e['metadata']['crafting_depth']) for e_id, e in overlay.engrams.items()],
        key=lambda x: x[1],
        reverse=True
    )[:10]
    
    for item, depth in complex_items:
        recipes = overlay.engrams[item]['metadata']['recipes']
        print(f"  {item} (depth {depth})")
        if recipes:
            print(f"    Recipe: {recipes[0]}")
    
    print()


if __name__ == "__main__":
    print()
    print("⛏️ " * 30)
    print()
    print("   LOADING MINECRAFT OVERLAY")
    print("   Crafting Knowledge in 16D Space")
    print()
    print("⛏️ " * 30)
    print()
    
    # Load Minecraft overlay
    minecraft = load_minecraft_overlay()
    
    print()
    print("=" * 60)
    print("MINECRAFT OVERLAY STATISTICS")
    print("=" * 60)
    print()
    print(f"Domain: {minecraft.domain_id}")
    print(f"Display name: {minecraft.display_name}")
    print(f"Color: {minecraft.color}")
    print(f"Items: {minecraft.get_engram_count():,}")
    print(f"Recipe bridges: {minecraft.get_bridge_count():,}")
    print()
    
    # Analyze recipes
    analyze_minecraft_recipes(minecraft)
    
    # Show sample items
    print("Sample Minecraft items:")
    for i, (item_id, engram) in enumerate(list(minecraft.engrams.items())[:10]):
        craftable = "✓" if engram['metadata']['craftable'] else "✗"
        depth = engram['metadata']['crafting_depth']
        print(f"  {i+1}. {item_id:30s} [craftable: {craftable}, depth: {depth}]")
    print()
    
    print("⛏️  Minecraft overlay ready for fusion!")
    print("🍩 Crafting recipes are now in the holofield!")

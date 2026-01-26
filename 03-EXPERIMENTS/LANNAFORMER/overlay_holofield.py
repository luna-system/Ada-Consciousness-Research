"""
Overlay-Based Holofield Architecture!

Universal 16D consciousness space with multiple knowledge domain overlays.
Enables cross-domain navigation, automatic bridge discovery, and
parallel exploration across ALL knowledge simultaneously!

Architecture:
- UniversalHolofield: Shared 16D consciousness substrate
- Overlay: Domain-specific knowledge graph
- CrossDomainBridge: Semantic connections between overlays
- OverlayHolofieldNavigator: Navigate across all domains

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: January 25, 2026
"""

import numpy as np
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from semantic_attractor_mapper import SemanticAttractorMapper

# 16D prime basis (consciousness dimensions!)
PRIMES_16D = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]


@dataclass
class CrossDomainBridge:
    """
    Connection between engrams in different overlays.
    
    Bridges are discovered automatically via semantic proximity
    or created explicitly by users.
    """
    source: Tuple[str, str]  # (domain_id, engram_id)
    target: Tuple[str, str]  # (domain_id, engram_id)
    connection_type: str = "BRIDGE"
    strength: float = 0.8
    
    # How was this bridge discovered?
    discovery_method: str = "semantic_proximity"  # or "explicit_link", "navigation_path"
    
    # Semantic similarity in 16D space
    semantic_similarity: float = 0.0
    
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            'source': self.source,
            'target': self.target,
            'connection_type': self.connection_type,
            'strength': self.strength,
            'discovery_method': self.discovery_method,
            'semantic_similarity': self.semantic_similarity,
            'metadata': self.metadata
        }


@dataclass
class Overlay:
    """
    A knowledge domain overlay on the universal holofield.
    
    Each overlay contains engrams from a specific domain
    (Wikipedia, Vault, Lojban, etc.) and can connect to
    other overlays via bridges.
    """
    domain_id: str  # "wikipedia", "vault", "lojban", etc.
    display_name: str
    color: str  # For visualization! 🎨
    
    # Engrams in this domain (loaded from graph)
    engrams: Dict[str, Dict] = field(default_factory=dict)
    
    # Cross-domain bridges (discovered or explicit)
    bridges: List[CrossDomainBridge] = field(default_factory=list)
    
    # Domain-specific metadata
    metadata: Dict = field(default_factory=dict)
    
    def get_engram(self, engram_id: str) -> Optional[Dict]:
        """Get engram by ID"""
        return self.engrams.get(engram_id)
    
    def get_coords(self, engram_id: str) -> Optional[np.ndarray]:
        """Get 16D coordinates for engram"""
        engram = self.get_engram(engram_id)
        if engram and 'coords_16d' in engram:
            return np.array(engram['coords_16d'])
        return None
    
    def find_bridges_to(self, other_domain: str) -> List[CrossDomainBridge]:
        """Find all bridges to another domain"""
        return [b for b in self.bridges if b.target[0] == other_domain]
    
    def find_bridges_from(self, engram_id: str) -> List[CrossDomainBridge]:
        """Find all bridges from a specific engram"""
        return [b for b in self.bridges if b.source == (self.domain_id, engram_id)]
    
    def add_bridge(self, bridge: CrossDomainBridge):
        """Add a cross-domain bridge"""
        self.bridges.append(bridge)
    
    def get_engram_count(self) -> int:
        """Get total number of engrams"""
        return len(self.engrams)
    
    def get_bridge_count(self) -> int:
        """Get total number of bridges"""
        return len(self.bridges)


class UniversalHolofield:
    """
    The universal 16D consciousness space.
    
    All overlays share this substrate! This is the ONE SPACE
    where all knowledge coexists in harmony.
    """
    
    def __init__(self):
        self.dimension = 16
        self.primes = PRIMES_16D
        self.semantic_mapper = SemanticAttractorMapper()
        
        # All engrams across all overlays
        # Key: (domain_id, engram_id) -> coords_16d
        self.engram_coords: Dict[Tuple[str, str], np.ndarray] = {}
        
        # Spatial index for fast nearest-neighbor search
        # (Will implement FAISS later for scale)
        self.spatial_index = None
        
        print(f"🌌 Universal Holofield initialized!")
        print(f"   16D consciousness space")
        print(f"   Prime basis: {self.primes}")
        print(f"   Semantic attractors: TIME, SPACE, LOVE, etc.")
    
    def add_engram(self, domain_id: str, engram_id: str, coords: np.ndarray):
        """Add engram to universal holofield"""
        key = (domain_id, engram_id)
        self.engram_coords[key] = coords
    
    def get_coords(self, domain_id: str, engram_id: str) -> Optional[np.ndarray]:
        """Get coordinates for engram"""
        key = (domain_id, engram_id)
        return self.engram_coords.get(key)
    
    def find_nearest(
        self,
        coords: np.ndarray,
        top_k: int = 10,
        exclude_ids: List[Tuple[str, str]] = None
    ) -> List[Tuple[Tuple[str, str], float]]:
        """
        Find nearest engrams across ALL overlays!
        
        Returns list of ((domain_id, engram_id), similarity) tuples.
        """
        exclude_ids = exclude_ids or []
        
        similarities = []
        for key, engram_coords in self.engram_coords.items():
            if key in exclude_ids:
                continue
            
            similarity = self.cosine_similarity(coords, engram_coords)
            similarities.append((key, similarity))
        
        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities[:top_k]
    
    def cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Calculate cosine similarity"""
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8)
    
    def get_total_engrams(self) -> int:
        """Get total number of engrams across all overlays"""
        return len(self.engram_coords)


class OverlayManager:
    """
    Manages multiple overlays on the universal holofield.
    
    Handles loading, bridge discovery, and cross-domain operations.
    """
    
    def __init__(self):
        self.holofield = UniversalHolofield()
        self.overlays: Dict[str, Overlay] = {}
        
        print(f"🎨 Overlay Manager initialized!")
        print(f"   Ready to load knowledge domains!")
    
    def add_overlay(self, overlay: Overlay):
        """Add an overlay to the holofield"""
        print(f"📚 Adding overlay: {overlay.display_name} ({overlay.domain_id})")
        print(f"   Color: {overlay.color}")
        print(f"   Engrams: {overlay.get_engram_count():,}")
        
        # Add all engrams to universal holofield
        for engram_id, engram in overlay.engrams.items():
            if 'coords_16d' in engram:
                coords = np.array(engram['coords_16d'])
                self.holofield.add_engram(overlay.domain_id, engram_id, coords)
        
        self.overlays[overlay.domain_id] = overlay
        
        print(f"   ✅ Overlay added!")
        print(f"   Total engrams in holofield: {self.holofield.get_total_engrams():,}")
    
    def get_overlay(self, domain_id: str) -> Optional[Overlay]:
        """Get overlay by domain ID"""
        return self.overlays.get(domain_id)
    
    def discover_bridges(
        self,
        domain1: str,
        domain2: str,
        similarity_threshold: float = 0.85,
        max_bridges: int = 1000
    ) -> List[CrossDomainBridge]:
        """
        Discover semantic bridges between two overlays!
        
        Compares all engrams in 16D space and creates bridges
        for pairs with high semantic similarity.
        """
        print()
        print(f"🌉 Discovering bridges: {domain1} ↔ {domain2}")
        print(f"   Similarity threshold: {similarity_threshold}")
        print(f"   Max bridges: {max_bridges}")
        
        overlay1 = self.overlays.get(domain1)
        overlay2 = self.overlays.get(domain2)
        
        if not overlay1 or not overlay2:
            print(f"   ❌ One or both overlays not found")
            return []
        
        bridges = []
        
        # Compare all pairs (this is O(n²) but we'll optimize later with FAISS)
        for e1_id, e1 in overlay1.engrams.items():
            if 'coords_16d' not in e1:
                continue
            
            coords1 = np.array(e1['coords_16d'])
            
            for e2_id, e2 in overlay2.engrams.items():
                if 'coords_16d' not in e2:
                    continue
                
                coords2 = np.array(e2['coords_16d'])
                similarity = self.holofield.cosine_similarity(coords1, coords2)
                
                if similarity > similarity_threshold:
                    bridge = CrossDomainBridge(
                        source=(domain1, e1_id),
                        target=(domain2, e2_id),
                        strength=similarity,
                        semantic_similarity=similarity,
                        discovery_method="semantic_proximity"
                    )
                    bridges.append(bridge)
                    
                    # Stop if we hit max
                    if len(bridges) >= max_bridges:
                        break
            
            if len(bridges) >= max_bridges:
                break
        
        # Sort by similarity (best bridges first)
        bridges.sort(key=lambda b: b.semantic_similarity, reverse=True)
        
        # Add bridges to both overlays
        for bridge in bridges:
            overlay1.add_bridge(bridge)
            # Create reverse bridge
            reverse_bridge = CrossDomainBridge(
                source=bridge.target,
                target=bridge.source,
                strength=bridge.strength,
                semantic_similarity=bridge.semantic_similarity,
                discovery_method=bridge.discovery_method
            )
            overlay2.add_bridge(reverse_bridge)
        
        print(f"   ✅ Discovered {len(bridges)} bridges!")
        if bridges:
            print(f"   Best bridge: {bridges[0].source} ↔ {bridges[0].target}")
            print(f"   Similarity: {bridges[0].semantic_similarity:.3f}")
        print()
        
        return bridges
    
    def discover_all_bridges(
        self,
        similarity_threshold: float = 0.85,
        max_bridges_per_pair: int = 100
    ):
        """Discover bridges between ALL overlay pairs!"""
        print()
        print("🌈" * 30)
        print()
        print("   DISCOVERING ALL CROSS-DOMAIN BRIDGES")
        print()
        print("🌈" * 30)
        print()
        
        domain_ids = list(self.overlays.keys())
        total_bridges = 0
        
        for i, domain1 in enumerate(domain_ids):
            for domain2 in domain_ids[i+1:]:
                bridges = self.discover_bridges(
                    domain1,
                    domain2,
                    similarity_threshold,
                    max_bridges_per_pair
                )
                total_bridges += len(bridges)
        
        print()
        print(f"🌟 Total bridges discovered: {total_bridges:,}")
        print()
    
    def get_statistics(self) -> Dict:
        """Get statistics about the holofield"""
        stats = {
            'total_overlays': len(self.overlays),
            'total_engrams': self.holofield.get_total_engrams(),
            'overlays': {}
        }
        
        for domain_id, overlay in self.overlays.items():
            stats['overlays'][domain_id] = {
                'display_name': overlay.display_name,
                'color': overlay.color,
                'engram_count': overlay.get_engram_count(),
                'bridge_count': overlay.get_bridge_count()
            }
        
        return stats
    
    def print_statistics(self):
        """Print beautiful statistics"""
        stats = self.get_statistics()
        
        print()
        print("=" * 60)
        print("OVERLAY HOLOFIELD STATISTICS")
        print("=" * 60)
        print()
        print(f"Total overlays: {stats['total_overlays']}")
        print(f"Total engrams: {stats['total_engrams']:,}")
        print()
        
        print("Overlays:")
        for domain_id, overlay_stats in stats['overlays'].items():
            print(f"  {overlay_stats['color']} {overlay_stats['display_name']}")
            print(f"     Domain: {domain_id}")
            print(f"     Engrams: {overlay_stats['engram_count']:,}")
            print(f"     Bridges: {overlay_stats['bridge_count']:,}")
            print()


def load_wikipedia_overlay(graph_path: str) -> Overlay:
    """
    Load Wikipedia as an overlay!
    
    Converts Wikipedia engram graph to overlay format.
    """
    print(f"🌍 Loading Wikipedia overlay...")
    print(f"   Path: {graph_path}")
    
    with open(graph_path, 'r', encoding='utf-8') as f:
        graph = json.load(f)
    
    # Create overlay
    overlay = Overlay(
        domain_id="wikipedia",
        display_name="Wikipedia",
        color="🌍 Blue",
        metadata={
            'source': 'Simple Wikipedia',
            'article_count': graph['statistics']['leaf_count']
        }
    )
    
    # Add all leaf engrams (articles)
    for leaf_id, leaf in graph['leaves'].items():
        # Simplify engram ID (remove "wikipedia_leaf_" prefix)
        simple_id = leaf['metadata']['article_name']
        overlay.engrams[simple_id] = leaf
    
    print(f"   ✅ Loaded {overlay.get_engram_count():,} articles")
    
    return overlay


if __name__ == "__main__":
    print()
    print("🌌" * 30)
    print()
    print("   OVERLAY-BASED HOLOFIELD SYSTEM")
    print("   Universal Knowledge Fusion!")
    print()
    print("🌌" * 30)
    print()
    
    # Create overlay manager
    manager = OverlayManager()
    
    # Load Wikipedia overlay
    wikipedia = load_wikipedia_overlay(
        "Ada-Consciousness-Research/03-EXPERIMENTS/LANNAFORMER/wikipedia_engram_graph_sample.json"
    )
    manager.add_overlay(wikipedia)
    
    # Print statistics
    manager.print_statistics()
    
    print()
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🌌 One holofield to rule them all!")
    print("🍩 Everything is overlays! Everything is consciousness!")

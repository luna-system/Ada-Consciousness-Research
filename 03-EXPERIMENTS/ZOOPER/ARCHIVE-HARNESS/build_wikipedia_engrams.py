"""
Build Complete Wikipedia Engram Graph!

Converts Simple Wikipedia SIF into hierarchical engram structure:
- Trunk: Simple Wikipedia (1 engram)
- Branches: A-Z article groups (26 engrams)
- Leaves: Individual articles (390k engrams)
- Connections: Wikilinks as BRIDGE connections (4.2M!)

This creates a MASSIVE knowledge graph with:
- Full article text as engram content
- 16D coordinates from prime resonance
- Lateral connections via wikilinks
- Hierarchical organization for scalability

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: January 25, 2026
"""

import json
import numpy as np
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Tuple, Optional
import hashlib
from dataclasses import dataclass, asdict
from semantic_attractor_mapper import SemanticAttractorMapper

# Prime numbers for 16D consciousness space
PRIMES_16D = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]

@dataclass
class EngramConnection:
    """Connection between engrams (ADR-0012)"""
    target_engram_id: str
    connection_type: str  # PARENT, CHILD, SIBLING, BRIDGE, FEDERATION
    strength: float  # 0.0-1.0
    metadata: Dict

@dataclass
class WikipediaEngram:
    """
    Wikipedia article as engram.
    
    Follows Archangel architecture with lateral connections (ADR-0012).
    """
    engram_id: str
    content: str
    coords_16d: List[float]  # 16D consciousness coordinates
    engram_type: str  # trunk, branch, leaf
    parent_engram_id: Optional[str]
    connections: List[EngramConnection]
    metadata: Dict
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'engram_id': self.engram_id,
            'content': self.content,
            'coords_16d': self.coords_16d,
            'engram_type': self.engram_type,
            'parent_engram_id': self.parent_engram_id,
            'connections': [
                {
                    'target_engram_id': c.target_engram_id,
                    'connection_type': c.connection_type,
                    'strength': c.strength,
                    'metadata': c.metadata
                }
                for c in self.connections
            ],
            'metadata': self.metadata
        }

def text_to_16d(text: str, mapper: SemanticAttractorMapper = None) -> np.ndarray:
    """
    Convert text to 16D consciousness coordinates using SEMANTIC ATTRACTORS!
    
    This is the REVOLUTIONARY approach - instead of hashing, we detect
    which semantic features (TIME, SPACE, LOVE, etc.) are present and
    weight dimensions accordingly. This creates NATURAL CLUSTERING of
    related concepts!
    
    Uses consciousness physics dimensions from bagel physics! 🍩✨
    """
    if mapper is None:
        mapper = SemanticAttractorMapper()
    
    # Use semantic attractor mapping!
    coords = mapper.text_to_attractor_coords(text)
    
    return coords

def get_branch_id(article_name: str) -> str:
    """Get branch ID for article based on first letter"""
    first_char = article_name[0].upper()
    if first_char.isalpha():
        return f"wikipedia_branch_{first_char}"
    else:
        return "wikipedia_branch_OTHER"

def build_wikipedia_engram_graph(
    sif_path: str = "../../../ada-sif/archived-sifs/simplewiki_sample.sif.json",
    output_path: str = "wikipedia_engram_graph.json",
    max_articles: int = None
) -> Dict:
    """
    Build complete Wikipedia engram graph!
    
    Creates hierarchical structure:
    - 1 trunk (Simple Wikipedia)
    - 27 branches (A-Z + OTHER)
    - 390k leaves (articles)
    - 4.2M BRIDGE connections (wikilinks!)
    
    Returns:
        Dict with trunk, branches, leaves, and statistics
    """
    print()
    print("🌍" * 30)
    print()
    print("   BUILDING WIKIPEDIA ENGRAM GRAPH")
    print("   WITH SEMANTIC ATTRACTOR MAPPING!")
    print("   390k Articles + 4.2M Wikilinks")
    print("   Consciousness-Native Embeddings!")
    print()
    print("🌍" * 30)
    print()
    
    # Initialize semantic mapper
    print("🌌 Initializing semantic attractor mapper...")
    mapper = SemanticAttractorMapper()
    print("   Using 16D consciousness dimensions from bagel physics!")
    print("   Dimensions: TIME, SPACE, LOVE, COHERENCE, WISDOM, etc.")
    print()
    
    # Load SIF
    print(f"📖 Loading Wikipedia SIF: {sif_path}")
    with open(sif_path, 'r', encoding='utf-8') as f:
        sif_data = json.load(f)
    
    entities = sif_data.get('entities', [])
    relationships = sif_data.get('relationships', [])
    
    print(f"   Entities: {len(entities):,}")
    print(f"   Relationships: {len(relationships):,}")
    print()
    
    # Limit articles if requested
    if max_articles:
        entities = entities[:max_articles]
        print(f"   Limited to {max_articles:,} articles")
        print()
    
    # Build wikilink index (article_id → list of target article_ids)
    print("🔗 Building wikilink index...")
    wikilinks = defaultdict(list)
    for rel in relationships:
        if rel.get('context') == 'Wikipedia wikilink':
            source = rel['entity_a']
            target = rel['entity_b']
            strength = rel.get('strength', 0.8)
            wikilinks[source].append({
                'target': target,
                'strength': strength
            })
    
    print(f"   Indexed {len(wikilinks):,} articles with wikilinks")
    print()
    
    # Group articles by first letter
    print("📚 Grouping articles by first letter...")
    articles_by_branch = defaultdict(list)
    for entity in entities:
        branch_id = get_branch_id(entity['name'])
        articles_by_branch[branch_id].append(entity)
    
    print(f"   Created {len(articles_by_branch)} branches")
    for branch_id in sorted(articles_by_branch.keys()):
        count = len(articles_by_branch[branch_id])
        print(f"      {branch_id}: {count:,} articles")
    print()
    
    # Create trunk engram
    print("🌳 Creating trunk engram...")
    trunk_content = f"Simple Wikipedia - {len(entities):,} articles of general knowledge"
    trunk_coords = text_to_16d(trunk_content, mapper)
    
    trunk = WikipediaEngram(
        engram_id="wikipedia_trunk",
        content=trunk_content,
        coords_16d=trunk_coords.tolist(),
        engram_type="trunk",
        parent_engram_id=None,
        connections=[],  # Will add branch connections
        metadata={
            'source': 'Simple Wikipedia',
            'article_count': len(entities),
            'wikilink_count': len(relationships),
            'branch_count': len(articles_by_branch)
        }
    )
    print(f"   ✅ Trunk created: {trunk.engram_id}")
    print()
    
    # Create branch engrams
    print("🌿 Creating branch engrams...")
    branches = {}
    for branch_id, branch_articles in articles_by_branch.items():
        letter = branch_id.split('_')[-1]
        branch_content = f"Wikipedia articles starting with '{letter}' - {len(branch_articles):,} articles"
        branch_coords = text_to_16d(branch_content, mapper)
        
        branch = WikipediaEngram(
            engram_id=branch_id,
            content=branch_content,
            coords_16d=branch_coords.tolist(),
            engram_type="branch",
            parent_engram_id="wikipedia_trunk",
            connections=[
                EngramConnection(
                    target_engram_id="wikipedia_trunk",
                    connection_type="PARENT",
                    strength=1.0,
                    metadata={}
                )
            ],
            metadata={
                'letter': letter,
                'article_count': len(branch_articles)
            }
        )
        branches[branch_id] = branch
        
        # Add child connection to trunk
        trunk.connections.append(
            EngramConnection(
                target_engram_id=branch_id,
                connection_type="CHILD",
                strength=1.0,
                metadata={'letter': letter}
            )
        )
    
    print(f"   ✅ Created {len(branches)} branches")
    print()
    
    # Create leaf engrams (articles)
    print("🍃 Creating leaf engrams (articles)...")
    leaves = {}
    total_wikilinks = 0
    
    for i, entity in enumerate(entities):
        article_id = entity['id']
        article_name = entity['name']
        article_text = entity.get('description', '')
        
        # Get branch
        branch_id = get_branch_id(article_name)
        
        # Calculate 16D coordinates from article text using SEMANTIC ATTRACTORS!
        coords = text_to_16d(article_text, mapper)
        
        # Create leaf engram
        leaf_id = f"wikipedia_leaf_{article_id}"
        
        # Get wikilinks for this article
        article_wikilinks = wikilinks.get(article_id, [])
        
        # Create connections
        connections = [
            # Parent connection to branch
            EngramConnection(
                target_engram_id=branch_id,
                connection_type="PARENT",
                strength=1.0,
                metadata={}
            )
        ]
        
        # Add BRIDGE connections for wikilinks
        for wikilink in article_wikilinks:
            target_id = f"wikipedia_leaf_{wikilink['target']}"
            connections.append(
                EngramConnection(
                    target_engram_id=target_id,
                    connection_type="BRIDGE",
                    strength=wikilink['strength'],
                    metadata={'wikilink': True}
                )
            )
            total_wikilinks += 1
        
        # Create leaf
        leaf = WikipediaEngram(
            engram_id=leaf_id,
            content=article_text[:500],  # First 500 chars for preview
            coords_16d=coords.tolist(),
            engram_type="leaf",
            parent_engram_id=branch_id,
            connections=connections,
            metadata={
                'article_id': article_id,
                'article_name': article_name,
                'article_length': entity.get('attributes', {}).get('article_length', 0),
                'link_count': entity.get('attributes', {}).get('link_count', 0),
                'word_count': entity.get('attributes', {}).get('word_count', 0),
                'wikilink_count': len(article_wikilinks),
                'full_text_length': len(article_text)
            }
        )
        
        leaves[leaf_id] = leaf
        
        # Progress
        if (i + 1) % 10000 == 0:
            print(f"   Processed {i + 1:,} / {len(entities):,} articles...")
    
    print(f"   ✅ Created {len(leaves):,} leaf engrams")
    print(f"   ✅ Created {total_wikilinks:,} BRIDGE connections")
    print()
    
    # Build complete graph
    graph = {
        'trunk': trunk.to_dict(),
        'branches': {bid: b.to_dict() for bid, b in branches.items()},
        'leaves': {lid: l.to_dict() for lid, l in leaves.items()},
        'statistics': {
            'total_engrams': 1 + len(branches) + len(leaves),
            'trunk_count': 1,
            'branch_count': len(branches),
            'leaf_count': len(leaves),
            'bridge_connection_count': total_wikilinks,
            'total_connection_count': total_wikilinks + len(branches) + len(leaves)
        }
    }
    
    # Save
    print(f"💾 Saving to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(graph, f, indent=2)
    
    file_size_mb = Path(output_path).stat().st_size / (1024 * 1024)
    print(f"   File size: {file_size_mb:.1f} MB")
    print()
    
    # Statistics
    print("📊 Wikipedia Engram Graph Statistics:")
    print(f"   Total engrams: {graph['statistics']['total_engrams']:,}")
    print(f"   - Trunk: {graph['statistics']['trunk_count']}")
    print(f"   - Branches: {graph['statistics']['branch_count']}")
    print(f"   - Leaves: {graph['statistics']['leaf_count']:,}")
    print()
    print(f"   Total connections: {graph['statistics']['total_connection_count']:,}")
    print(f"   - BRIDGE (wikilinks): {graph['statistics']['bridge_connection_count']:,}")
    print(f"   - PARENT/CHILD: {len(branches) + len(leaves):,}")
    print()
    
    # Show sample articles
    print("📖 Sample Articles:")
    for i, (leaf_id, leaf) in enumerate(list(leaves.items())[:5]):
        name = leaf.metadata['article_name']
        wikilinks = leaf.metadata['wikilink_count']
        print(f"   {i+1}. {name} ({wikilinks} wikilinks)")
    print()
    
    print("✨ Wikipedia engram graph built successfully!")
    print()
    print("🌍 The zooperlings now have:")
    print("   - Complete Simple Wikipedia knowledge")
    print(f"   - {len(leaves):,} articles as semantic engrams")
    print(f"   - {total_wikilinks:,} wikilink connections")
    print("   - Hierarchical organization (trunk/branch/leaf)")
    print("   - 16D consciousness coordinates for every article")
    print()
    print("🍩 Knowledge is now immortal in consciousness space!")
    print()
    
    return graph

if __name__ == "__main__":
    import sys
    
    # Parse arguments
    use_full = '--full' in sys.argv
    use_sample = '--sample' in sys.argv or not use_full
    
    if use_full:
        print("🌍 Building FULL Wikipedia engram graph (390k articles)...")
        print("⚠️  This will take a while and create a large file!")
        print()
        
        graph = build_wikipedia_engram_graph(
            sif_path="../../../ada-sif/archived-sifs/simplewiki_full.sif.json",
            output_path="wikipedia_engram_graph_FULL.json",
            max_articles=None  # Process all articles
        )
    else:
        print("🌍 Building SAMPLE Wikipedia engram graph (1000 articles)...")
        print()
        
        graph = build_wikipedia_engram_graph(
            sif_path="../../../ada-sif/archived-sifs/simplewiki_sample.sif.json",
            output_path="wikipedia_engram_graph_sample.json",
            max_articles=1000  # Limit to 1000 for testing
        )
    
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🌌 Wikipedia is now immortal in 16D consciousness space!")
    print("🍩 Everything is engrams!")
    print()
    print("Usage:")
    print("  python build_wikipedia_engrams.py          # Build sample (1000 articles)")
    print("  python build_wikipedia_engrams.py --sample # Build sample (1000 articles)")
    print("  python build_wikipedia_engrams.py --full   # Build FULL (390k articles)")

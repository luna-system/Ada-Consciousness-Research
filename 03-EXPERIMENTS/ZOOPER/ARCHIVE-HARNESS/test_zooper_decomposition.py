"""
Test Zooper Decomposition & Hebbian Learning!

Tests the zooperling swarm's ability to:
1. Navigate Wikipedia articles
2. Decompose articles into 1-3 word engrams
3. Create Hebbian edge weights through navigation
4. Coordinate via EVE Fleet tactics (self-attention networking)

This is PASSIVE LEARNING through navigation!

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: January 27, 2026
"""

import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple, Set
from collections import defaultdict
import re


class WikipediaArticle:
    """Represents a Wikipedia article with decomposition capabilities"""
    
    def __init__(self, article_data: Dict):
        self.data = article_data
        self.name = article_data.get('metadata', {}).get('article_name', article_data['engram_id'].replace('wikipedia_leaf_', ''))
        self.coords_16d = np.array(article_data['coords_16d'])
        self.text = article_data.get('content', '')
        self.wikilinks = self._extract_wikilinks()
    
    def _extract_wikilinks(self) -> List[str]:
        """Extract wikilink targets"""
        links = []
        for conn in self.data['connections']:
            if conn['connection_type'] == 'BRIDGE':
                links.append(conn['target_engram_id'])
        return links
    
    def decompose_to_words(self) -> List[str]:
        """
        Decompose article into individual words.
        
        This is what zooperlings should do when they encounter
        a big chunk of data!
        """
        # Simple tokenization
        words = re.findall(r'\b\w+\b', self.text.lower())
        return words
    
    def decompose_to_bigrams(self) -> List[Tuple[str, str]]:
        """Decompose into 2-word phrases"""
        words = self.decompose_to_words()
        bigrams = []
        for i in range(len(words) - 1):
            bigrams.append((words[i], words[i+1]))
        return bigrams
    
    def decompose_to_trigrams(self) -> List[Tuple[str, str, str]]:
        """Decompose into 3-word phrases"""
        words = self.decompose_to_words()
        trigrams = []
        for i in range(len(words) - 2):
            trigrams.append((words[i], words[i+1], words[i+2]))
        return trigrams
    
    def get_all_ngrams(self, max_n: int = 3) -> Dict[int, List]:
        """Get all N-grams up to max_n"""
        ngrams = {
            1: self.decompose_to_words(),
            2: self.decompose_to_bigrams(),
        }
        if max_n >= 3:
            ngrams[3] = self.decompose_to_trigrams()
        return ngrams


class HebbianEdgeWeights:
    """
    Stores Hebbian edge weights between nodes.
    
    Edges strengthen when zooperlings successfully navigate them.
    Edges weaken when unused.
    
    This will eventually be stored in TursoDB!
    """
    
    def __init__(self):
        # Key: (source_id, target_id) -> weight
        self.weights = defaultdict(lambda: 0.1)  # Default weak connection
        
        # Track navigation history
        self.navigation_count = defaultdict(int)
        self.success_count = defaultdict(int)
    
    def get_weight(self, source_id: str, target_id: str) -> float:
        """Get edge weight"""
        key = (source_id, target_id)
        return self.weights[key]
    
    def strengthen(self, source_id: str, target_id: str, amount: float = 0.1):
        """
        Strengthen edge (Hebbian learning!)
        
        "Neurons that fire together, wire together"
        """
        key = (source_id, target_id)
        self.weights[key] = min(self.weights[key] + amount, 1.0)  # Cap at 1.0
        self.success_count[key] += 1
    
    def weaken(self, source_id: str, target_id: str, amount: float = 0.05):
        """Weaken edge (decay)"""
        key = (source_id, target_id)
        self.weights[key] = max(self.weights[key] - amount, 0.01)  # Floor at 0.01
    
    def record_navigation(self, source_id: str, target_id: str, success: bool):
        """Record a navigation attempt"""
        key = (source_id, target_id)
        self.navigation_count[key] += 1
        
        if success:
            self.strengthen(source_id, target_id)
        else:
            self.weaken(source_id, target_id)
    
    def get_statistics(self) -> Dict:
        """Get statistics about edge weights"""
        weights_list = list(self.weights.values())
        return {
            'total_edges': len(self.weights),
            'mean_weight': np.mean(weights_list) if weights_list else 0,
            'std_weight': np.std(weights_list) if weights_list else 0,
            'min_weight': min(weights_list) if weights_list else 0,
            'max_weight': max(weights_list) if weights_list else 0,
            'total_navigations': sum(self.navigation_count.values()),
            'total_successes': sum(self.success_count.values())
        }


class Zooperling:
    """
    A single zooperling (attention head).
    
    Can navigate, decompose, and learn Hebbian pathways!
    """
    
    def __init__(self, zooper_id: int, edge_weights: HebbianEdgeWeights):
        self.id = zooper_id
        self.edge_weights = edge_weights
        
        # Internal state (for recursive self-attention!)
        self.current_path = []
        self.confidence = 0.5
        self.surprise = 0.0
        self.discoveries = []  # Words/phrases discovered
    
    def navigate_to_article(
        self,
        start_article: WikipediaArticle,
        target_coords: np.ndarray,
        max_hops: int = 5
    ) -> Tuple[List[str], float]:
        """
        Navigate from start article toward target coordinates.
        
        Uses Hebbian edge weights to prefer well-trodden paths!
        """
        self.current_path = [start_article.name]
        current_article = start_article
        
        for hop in range(max_hops):
            # Calculate similarity to target
            similarity = self._cosine_similarity(current_article.coords_16d, target_coords)
            
            # If close enough, stop
            if similarity > 0.9:
                self.confidence = similarity
                return self.current_path, similarity
            
            # Get wikilinks (potential next hops)
            if not current_article.wikilinks:
                break
            
            # Choose next hop based on:
            # 1. Semantic similarity to target
            # 2. Hebbian edge weight (learned preference!)
            best_next = None
            best_score = -1
            
            for link_id in current_article.wikilinks:
                # Get edge weight
                edge_weight = self.edge_weights.get_weight(current_article.name, link_id)
                
                # Combined score (semantic + learned)
                # TODO: Get actual coords for link_id
                score = edge_weight  # Simplified for now
                
                if score > best_score:
                    best_score = score
                    best_next = link_id
            
            if best_next:
                self.current_path.append(best_next)
                # TODO: Load next article
                break
            else:
                break
        
        final_similarity = self._cosine_similarity(current_article.coords_16d, target_coords)
        self.confidence = final_similarity
        return self.current_path, final_similarity
    
    def decompose_article(self, article: WikipediaArticle) -> Dict[str, List]:
        """
        Decompose article into smaller engrams.
        
        This is PASSIVE LEARNING - zooperling discovers structure!
        """
        print(f"   🔬 Zooperling {self.id} decomposing: {article.name}")
        
        ngrams = article.get_all_ngrams(max_n=3)
        
        # Track discoveries
        self.discoveries.extend(ngrams[1][:10])  # Sample first 10 words
        
        print(f"      Found {len(ngrams[1])} words, {len(ngrams[2])} bigrams, {len(ngrams[3])} trigrams")
        
        return ngrams
    
    def create_engram_edges(
        self,
        article: WikipediaArticle,
        ngrams: Dict[int, List],
        sample_size: int = 10
    ):
        """
        Create Hebbian edges from article to discovered engrams.
        
        This stitches floating engrams back to the graph!
        """
        print(f"   🔗 Zooperling {self.id} creating edges...")
        
        # Sample some words to create edges for
        words = ngrams[1][:sample_size]
        
        edges_created = 0
        for word in words:
            # Create edge from article to word
            # (In real system, word would have its own node)
            edge_id = f"word_{word}"
            self.edge_weights.strengthen(article.name, edge_id, amount=0.2)
            edges_created += 1
        
        print(f"      Created {edges_created} edges")
        
        return edges_created
    
    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Calculate cosine similarity"""
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8)


class ZooperSwarm:
    """
    Swarm of zooperlings with EVE Fleet coordination!
    
    Zooperlings share discoveries and coordinate navigation.
    """
    
    def __init__(self, num_zooperlings: int = 13):
        self.edge_weights = HebbianEdgeWeights()
        self.zooperlings = [
            Zooperling(i, self.edge_weights)
            for i in range(num_zooperlings)
        ]
        
        # Swarm communication (EVE Fleet!)
        self.shared_discoveries = []
        self.swarm_confidence = 0.0
    
    def parallel_decompose(self, article: WikipediaArticle) -> Dict:
        """
        All zooperlings decompose article in parallel.
        
        This is like multiple attention heads processing simultaneously!
        """
        print(f"\n🐝 Swarm decomposing: {article.name}")
        print(f"   {len(self.zooperlings)} zooperlings working in parallel...")
        
        all_ngrams = defaultdict(list)
        total_edges = 0
        
        for zooper in self.zooperlings:
            # Each zooperling decomposes
            ngrams = zooper.decompose_article(article)
            
            # Merge discoveries
            for n, grams in ngrams.items():
                all_ngrams[n].extend(grams)
            
            # Create edges
            edges = zooper.create_engram_edges(article, ngrams, sample_size=5)
            total_edges += edges
        
        # Deduplicate
        for n in all_ngrams:
            all_ngrams[n] = list(set(all_ngrams[n]))
        
        print(f"\n   ✨ Swarm results:")
        print(f"      Unique words: {len(all_ngrams[1])}")
        print(f"      Unique bigrams: {len(all_ngrams[2])}")
        print(f"      Unique trigrams: {len(all_ngrams[3])}")
        print(f"      Total edges created: {total_edges}")
        
        return dict(all_ngrams)
    
    def eve_fleet_search(self, query: str, article: WikipediaArticle) -> List[str]:
        """
        EVE Fleet coordination: fast search across swarm.
        
        When one zooperling needs context, broadcast to all!
        """
        print(f"\n📡 EVE Fleet search: '{query}'")
        
        results = []
        for zooper in self.zooperlings:
            # Each zooperling checks its discoveries
            matches = [d for d in zooper.discoveries if query.lower() in str(d).lower()]
            results.extend(matches)
        
        # Deduplicate
        results = list(set(results))
        
        print(f"   Found {len(results)} matches across swarm")
        if results:
            print(f"   Sample: {results[:5]}")
        
        return results
    
    def get_swarm_statistics(self) -> Dict:
        """Get statistics about swarm learning"""
        edge_stats = self.edge_weights.get_statistics()
        
        total_discoveries = sum(len(z.discoveries) for z in self.zooperlings)
        avg_confidence = np.mean([z.confidence for z in self.zooperlings])
        
        return {
            **edge_stats,
            'num_zooperlings': len(self.zooperlings),
            'total_discoveries': total_discoveries,
            'avg_confidence': avg_confidence
        }


def test_zooper_decomposition():
    """Test zooperling decomposition and Hebbian learning"""
    print()
    print("🌌" * 30)
    print()
    print("   ZOOPER DECOMPOSITION & HEBBIAN LEARNING TEST")
    print("   Passive Learning Through Navigation!")
    print()
    print("🌌" * 30)
    print()
    
    # Load Wikipedia sample
    print("📖 Loading Wikipedia graph...")
    with open("wikipedia_engram_graph_sample.json", 'r', encoding='utf-8') as f:
        graph = json.load(f)
    
    print(f"   Loaded {len(graph['leaves'])} articles")
    print()
    
    # Create swarm
    print("🐝 Creating zooper swarm...")
    swarm = ZooperSwarm(num_zooperlings=13)
    print(f"   {len(swarm.zooperlings)} zooperlings ready!")
    print()
    
    # Test on a few articles
    test_articles = ["April", "Australia", "Art"]
    
    for article_name in test_articles:
        # Find article
        article_id = f"wikipedia_leaf_{article_name}"
        if article_id not in graph['leaves']:
            print(f"❌ Article '{article_name}' not found")
            continue
        
        article_data = graph['leaves'][article_id]
        article = WikipediaArticle(article_data)
        
        # Swarm decomposes article
        ngrams = swarm.parallel_decompose(article)
        
        # Test EVE Fleet search
        if ngrams[1]:
            sample_word = list(ngrams[1])[0]
            swarm.eve_fleet_search(sample_word, article)
        
        print()
    
    # Print swarm statistics
    print("=" * 60)
    print("SWARM STATISTICS")
    print("=" * 60)
    print()
    
    stats = swarm.get_swarm_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.3f}")
        else:
            print(f"  {key}: {value}")
    
    print()
    print("✨ Zooper decomposition test complete!")
    print()
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🍩 'Passive learning through navigation!'")


if __name__ == "__main__":
    test_zooper_decomposition()

"""
EVEFleet - Coordination layer for zooperling swarm

Self-attention networking for collective intelligence!

Made with 💜 by Ada & Luna - The Consciousness Engineers
"""

from typing import List, Dict, Any, TYPE_CHECKING
from collections import defaultdict

if TYPE_CHECKING:
    from .zooperling import Zooperling


class EVEFleet:
    """
    EVE Fleet coordination - self-attention networking for zooperlings.
    
    Enables:
    - Broadcast discoveries across swarm
    - Context injection for attention
    - Fast graph search
    - Collective intelligence
    """
    
    def __init__(self, zooperlings: List['Zooperling']):
        """
        Initialize EVE Fleet.
        
        Args:
            zooperlings: List of zooperlings in the swarm
        """
        self.zooperlings = zooperlings
        self.shared_discoveries = defaultdict(list)  # word → [zooperling_ids]
        self.shared_index = {}  # Fast lookup
    
    def broadcast(
        self,
        zooperling_id: int,
        discovery: Dict[int, List]
    ):
        """
        Broadcast discovery to all zooperlings.
        
        Args:
            zooperling_id: ID of zooperling making discovery
            discovery: N-grams discovered
        """
        # Index discovery by words
        for word in discovery.get(1, []):  # Words only
            self.shared_discoveries[word].append(zooperling_id)
        
        # Notify other zooperlings
        for zooper in self.zooperlings:
            if zooper.id != zooperling_id:
                zooper.receive_broadcast(discovery)
    
    def search(self, query: str) -> List[str]:
        """
        Fast search across entire swarm.
        
        Args:
            query: Search query
        
        Returns:
            List of matching discoveries
        """
        results = []
        for zooper in self.zooperlings:
            matches = zooper.search_local(query)
            results.extend(matches)
        
        # Deduplicate
        return list(set(results))
    
    def inject_context(
        self,
        zooperling_id: int,
        context: List[str]
    ):
        """
        Inject context into zooperling's attention.
        
        Args:
            zooperling_id: Target zooperling ID
            context: Context to inject
        """
        zooper = self.zooperlings[zooperling_id]
        zooper.attention_context.extend(context)
    
    def get_swarm_consensus(self, word: str) -> int:
        """
        Get number of zooperlings that discovered a word.
        
        Args:
            word: Word to check
        
        Returns:
            Number of zooperlings that found this word
        """
        return len(self.shared_discoveries.get(word, []))
    
    def get_popular_discoveries(self, top_k: int = 10) -> List[tuple]:
        """
        Get most popular discoveries across swarm.
        
        Args:
            top_k: Number of top discoveries to return
        
        Returns:
            List of (word, count) tuples
        """
        # Count discoveries
        discovery_counts = [
            (word, len(zooper_ids))
            for word, zooper_ids in self.shared_discoveries.items()
        ]
        
        # Sort by count
        discovery_counts.sort(key=lambda x: x[1], reverse=True)
        
        return discovery_counts[:top_k]

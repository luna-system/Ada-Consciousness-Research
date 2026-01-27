"""
Zooperling - Individual attention head

Navigates, decomposes, and learns through exploration!

Made with 💜 by Ada & Luna - The Consciousness Engineers
"""

import re
import numpy as np
from typing import Dict, List, Tuple, Any, TYPE_CHECKING

from angel.holofield.manager import HolofieldManager

if TYPE_CHECKING:
    from .swarm import ZooperSwarm


class Zooperling:
    """
    Individual attention head that navigates and decomposes.
    
    Like a bee in a swarm - explores independently but shares discoveries!
    """
    
    def __init__(
        self,
        zooper_id: int,
        holofield_manager: HolofieldManager,
        swarm: 'ZooperSwarm'
    ):
        """
        Initialize Zooperling.
        
        Args:
            zooper_id: Unique ID for this zooperling
            holofield_manager: Reference to holofield
            swarm: Reference to parent swarm
        """
        self.id = zooper_id
        self.holofield = holofield_manager
        self.swarm = swarm
        
        # Internal state (recursive self-attention!)
        self.confidence = 0.5
        self.surprise = 0.0
        self.discoveries = []
        self.attention_context = []
    
    def decompose(self, article_data: Dict[str, Any]) -> Dict[int, List]:
        """
        Decompose article into N-grams.
        
        This is PASSIVE LEARNING - discovering structure through navigation!
        
        Args:
            article_data: Article dictionary with 'content' key
        
        Returns:
            Dict with {1: words, 2: bigrams, 3: trigrams}
        """
        text = article_data.get('content', '')
        words = self._tokenize(text)
        
        ngrams = {
            1: words,
            2: self._make_bigrams(words),
            3: self._make_trigrams(words)
        }
        
        # Track discoveries (sample first 10 words)
        self.discoveries.extend(words[:10])
        
        return ngrams
    
    def _tokenize(self, text: str) -> List[str]:
        """
        Simple tokenization - extract words.
        
        Args:
            text: Input text
        
        Returns:
            List of words (lowercase)
        """
        # Extract words (alphanumeric sequences)
        words = re.findall(r'\b\w+\b', text.lower())
        return words
    
    def _make_bigrams(self, words: List[str]) -> List[Tuple[str, str]]:
        """
        Create 2-word phrases.
        
        Args:
            words: List of words
        
        Returns:
            List of (word1, word2) tuples
        """
        bigrams = []
        for i in range(len(words) - 1):
            bigrams.append((words[i], words[i+1]))
        return bigrams
    
    def _make_trigrams(self, words: List[str]) -> List[Tuple[str, str, str]]:
        """
        Create 3-word phrases.
        
        Args:
            words: List of words
        
        Returns:
            List of (word1, word2, word3) tuples
        """
        trigrams = []
        for i in range(len(words) - 2):
            trigrams.append((words[i], words[i+1], words[i+2]))
        return trigrams
    
    def navigate_step(
        self,
        current_coords: np.ndarray,
        target_coords: np.ndarray,
        mode: str
    ) -> Tuple[np.ndarray, float]:
        """
        Single navigation step.
        
        Args:
            current_coords: Current 16D position
            target_coords: Target 16D position
            mode: "LOCAL", "GLOBAL", or "ADAPTIVE"
        
        Returns:
            - next_coords: Where to go next
            - confidence: How confident we are
        """
        if mode == "LOCAL":
            return self._follow_wikilinks(current_coords, target_coords)
        elif mode == "GLOBAL":
            return self._semantic_search(current_coords, target_coords)
        else:  # ADAPTIVE
            return self._hybrid_step(current_coords, target_coords)
    
    def _follow_wikilinks(
        self,
        current_coords: np.ndarray,
        target_coords: np.ndarray
    ) -> Tuple[np.ndarray, float]:
        """
        Follow wikilinks to neighboring articles.
        
        TODO: Implement wikilink following
        """
        # Placeholder
        return current_coords, self.confidence
    
    def _semantic_search(
        self,
        current_coords: np.ndarray,
        target_coords: np.ndarray
    ) -> Tuple[np.ndarray, float]:
        """
        Search entire graph via 16D semantic similarity.
        
        TODO: Implement semantic search
        """
        # Placeholder
        return current_coords, self.confidence
    
    def _hybrid_step(
        self,
        current_coords: np.ndarray,
        target_coords: np.ndarray
    ) -> Tuple[np.ndarray, float]:
        """
        Hybrid navigation mixing local and global.
        
        TODO: Implement hybrid strategy
        """
        # Placeholder
        return current_coords, self.confidence
    
    def receive_broadcast(self, discovery: Dict[int, List]):
        """
        Receive discovery from another zooperling (EVE Fleet!).
        
        Args:
            discovery: N-grams discovered by another zooperling
        """
        # Check if discovery is relevant to our context
        if self._is_relevant(discovery):
            self.attention_context.append(discovery)
            self.confidence += 0.05  # Boost confidence
            self.confidence = min(self.confidence, 1.0)  # Cap at 1.0
    
    def _is_relevant(self, discovery: Dict[int, List]) -> bool:
        """
        Check if discovery is relevant to our current context.
        
        Args:
            discovery: N-grams from another zooperling
        
        Returns:
            True if relevant
        """
        # Simple relevance check: do we have any overlapping words?
        their_words = set(discovery.get(1, []))
        our_words = set(self.discoveries)
        
        overlap = their_words & our_words
        return len(overlap) > 0
    
    def search_local(self, query: str) -> List[str]:
        """
        Search this zooperling's local discoveries.
        
        Args:
            query: Search query
        
        Returns:
            List of matching discoveries
        """
        matches = [
            d for d in self.discoveries
            if query.lower() in str(d).lower()
        ]
        return matches

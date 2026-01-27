"""
ZooperSwarm - Main swarm coordinator

Inherits from EngramCreator and manages 13 zooperlings.

Made with 💜 by Ada & Luna - The Consciousness Engineers
"""

import numpy as np
from typing import Tuple, Dict, List, Optional, Any
from collections import defaultdict

from angel.core.engram_creator import EngramCreator
from angel.core.engram import Engram
from angel.holofield.manager import HolofieldManager

from .zooperling import Zooperling
from .hebbian import HebbianEdgeWeights
from .eve_fleet import EVEFleet
from .kuramoto import KuramotoDynamics


class ZooperSwarm(EngramCreator):
    """
    Swarm of zooperlings (attention heads) that navigate, decompose, and learn.
    
    This is the attention mechanism for Archangel consciousness OS!
    
    Key Features:
    - 13 zooperlings work in parallel
    - Passive learning through navigation (no training!)
    - Hebbian edges strengthen with successful navigation
    - EVE Fleet coordination (swarm intelligence)
    - Kuramoto dynamics for coherence-based mode switching
    """
    
    def __init__(
        self,
        holofield_manager: HolofieldManager,
        num_zooperlings: int = 13,
        eve_fleet: Optional[EVEFleet] = None
    ):
        """
        Initialize ZooperSwarm.
        
        Args:
            holofield_manager: Reference to unified holofield
            num_zooperlings: Number of attention heads (default: 13)
            eve_fleet: Optional EVE Fleet coordinator
        """
        super().__init__(holofield_manager)
        
        self.num_zooperlings = num_zooperlings
        
        # Hebbian edge weights (eventually in TursoDB!)
        self.edge_weights = HebbianEdgeWeights(holofield_manager)
        
        # Create zooperling swarm
        self.zooperlings = [
            Zooperling(i, holofield_manager, self)
            for i in range(num_zooperlings)
        ]
        
        # EVE Fleet coordination
        self.eve_fleet = eve_fleet or EVEFleet(self.zooperlings)
        
        # Kuramoto dynamics for coherence
        self.kuramoto = KuramotoDynamics(num_zooperlings)
        self.K_local = 0.3   # Strong coupling for confident navigation
        self.K_global = 0.05  # Weak coupling for exploration
    
    def process(
        self,
        article_data: Dict[str, Any]
    ) -> Tuple[Dict[int, List], Engram]:
        """
        Process Wikipedia article: decompose and create engrams.
        
        This is the main entry point for Zooper processing!
        
        Args:
            article_data: Dictionary with 'content' and 'metadata' keys
        
        Returns:
            - decomposition_results: Dict with {1: words, 2: bigrams, 3: trigrams}
            - article_engram: Engram for the article
        """
        # Create article engram
        article_engram = self.create_engram(
            content=article_data['content'],
            data=article_data,
            engram_type="knowledge",
            metadata={
                'article_name': article_data.get('metadata', {}).get('article_name', 'unknown'),
                'source': 'wikipedia',
                'decomposed': True,
                'zooper_version': '0.1.0'
            }
        )
        
        # Store article engram
        article_id = self.store_engram(article_engram)
        
        # Parallel decomposition by swarm
        decomposition = self.parallel_decompose(article_data)
        
        # Create word/phrase engrams
        word_engrams = self._create_word_engrams(
            decomposition,
            article_id,
            article_engram.coords_16d
        )
        
        # Create Hebbian edges (ADR-0012!)
        self._create_hebbian_edges(article_id, word_engrams)
        
        return decomposition, article_engram
    
    def to_16d(self, article_data: Dict[str, Any]) -> np.ndarray:
        """
        Map article to 16D consciousness coordinates.
        
        Uses existing coordinates if available, otherwise computes
        via prime resonance.
        
        Args:
            article_data: Article dictionary
        
        Returns:
            16D numpy array
        """
        # Use existing coordinates if available
        if 'coords_16d' in article_data:
            return np.array(article_data['coords_16d'])
        
        # Otherwise compute via holofield's prime resonance
        text = article_data.get('content', '')
        return self.holofield_manager.to_consciousness_coords(text)
    
    def parallel_decompose(
        self,
        article_data: Dict[str, Any]
    ) -> Dict[int, List]:
        """
        All zooperlings decompose article in parallel.
        
        This is like multiple attention heads processing simultaneously!
        
        Args:
            article_data: Article dictionary
        
        Returns:
            Dict with {1: words, 2: bigrams, 3: trigrams}
        """
        all_ngrams = defaultdict(list)
        
        for zooper in self.zooperlings:
            # Each zooperling decomposes
            ngrams = zooper.decompose(article_data)
            
            # Merge discoveries
            for n, grams in ngrams.items():
                all_ngrams[n].extend(grams)
            
            # Broadcast to EVE Fleet
            self.eve_fleet.broadcast(zooper.id, ngrams)
        
        # Deduplicate
        for n in all_ngrams:
            all_ngrams[n] = list(set(all_ngrams[n]))
        
        return dict(all_ngrams)
    
    def navigate(
        self,
        start_coords: np.ndarray,
        target_coords: np.ndarray,
        max_hops: int = 5
    ) -> List[str]:
        """
        Navigate from start to target using hybrid strategy.
        
        Uses Kuramoto coherence to decide LOCAL/GLOBAL/ADAPTIVE mode.
        
        Args:
            start_coords: Starting 16D coordinates
            target_coords: Target 16D coordinates
            max_hops: Maximum navigation steps
        
        Returns:
            List of engram IDs in navigation path
        """
        # Update Kuramoto dynamics
        r, psi = self.kuramoto.order_parameter()
        
        # Choose navigation mode based on coherence
        if r > 0.8:
            # HIGH coherence - use LOCAL (wikilinks)
            return self._local_navigation(start_coords, target_coords, max_hops)
        elif r < 0.5:
            # LOW coherence - use GLOBAL (semantic search)
            return self._global_navigation(start_coords, target_coords, max_hops)
        else:
            # MEDIUM coherence - use ADAPTIVE (hybrid)
            return self._adaptive_navigation(start_coords, target_coords, max_hops, r)
    
    def _create_word_engrams(
        self,
        decomposition: Dict[int, List],
        article_id: str,
        article_coords: np.ndarray
    ) -> List[str]:
        """
        Create engrams for discovered words/phrases.
        
        Args:
            decomposition: N-grams from decomposition
            article_id: Parent article engram ID
            article_coords: Article's 16D coordinates
        
        Returns:
            List of word engram IDs
        """
        word_engram_ids = []
        
        # Sample words to create engrams for (don't create ALL of them!)
        sample_words = decomposition.get(1, [])[:50]  # First 50 words
        
        for word in sample_words:
            # Create word engram
            word_engram = self.create_engram(
                content=word,
                data={'word': word, 'parent_article': article_id},
                engram_type="language",
                metadata={
                    'word': word,
                    'source': 'zooper_decomposition',
                    'parent_article': article_id
                }
            )
            
            # Store word engram
            word_id = self.store_engram(word_engram)
            word_engram_ids.append(word_id)
        
        return word_engram_ids
    
    def _create_hebbian_edges(
        self,
        article_id: str,
        word_engram_ids: List[str]
    ):
        """
        Create Hebbian edges from article to word engrams.
        
        Uses EngramConnection (ADR-0012) with type HEBBIAN!
        
        Args:
            article_id: Article engram ID
            word_engram_ids: List of word engram IDs
        """
        for word_id in word_engram_ids:
            # Strengthen Hebbian edge
            self.edge_weights.strengthen(
                article_id,
                word_id,
                amount=0.2
            )
    
    def _local_navigation(
        self,
        start_coords: np.ndarray,
        target_coords: np.ndarray,
        max_hops: int
    ) -> List[str]:
        """
        LOCAL navigation: Follow wikilinks (convolution-like).
        
        TODO: Implement wikilink following
        """
        # Placeholder for now
        return []
    
    def _global_navigation(
        self,
        start_coords: np.ndarray,
        target_coords: np.ndarray,
        max_hops: int
    ) -> List[str]:
        """
        GLOBAL navigation: Semantic search in 16D (attention-like).
        
        TODO: Implement semantic search
        """
        # Placeholder for now
        return []
    
    def _adaptive_navigation(
        self,
        start_coords: np.ndarray,
        target_coords: np.ndarray,
        max_hops: int,
        coherence: float
    ) -> List[str]:
        """
        ADAPTIVE navigation: Hybrid mixing based on coherence.
        
        TODO: Implement hybrid strategy
        """
        # Placeholder for now
        return []
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about swarm learning.
        
        Returns:
            Dictionary with swarm stats
        """
        edge_stats = self.edge_weights.get_statistics()
        
        total_discoveries = sum(len(z.discoveries) for z in self.zooperlings)
        avg_confidence = np.mean([z.confidence for z in self.zooperlings])
        
        return {
            **edge_stats,
            'num_zooperlings': self.num_zooperlings,
            'total_discoveries': total_discoveries,
            'avg_confidence': float(avg_confidence),
            'kuramoto_coherence': float(self.kuramoto.order_parameter()[0])
        }

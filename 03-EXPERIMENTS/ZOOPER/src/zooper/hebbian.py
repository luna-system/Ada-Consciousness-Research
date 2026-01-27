"""
HebbianEdgeWeights - Manages Hebbian learning edges

"Neurons that fire together, wire together!"

Made with 💜 by Ada & Luna - The Consciousness Engineers
"""

import time
import numpy as np
from typing import Dict, Tuple
from collections import defaultdict

from angel.holofield.manager import HolofieldManager
from angel.core.engram import Engram


class HebbianEdgeWeights:
    """
    Manages Hebbian edge weights using EngramConnection (ADR-0012).
    
    Edges strengthen when zooperlings successfully navigate them.
    Eventually stored in TursoDB!
    """
    
    def __init__(self, holofield_manager: HolofieldManager):
        """
        Initialize Hebbian edge weight manager.
        
        Args:
            holofield_manager: Reference to holofield
        """
        self.holofield = holofield_manager
        
        # In-memory cache (eventually TursoDB!)
        self.weights = defaultdict(lambda: 0.1)  # Default weak connection
        self.navigation_count = defaultdict(int)
        self.success_count = defaultdict(int)
    
    def get_weight(self, source_id: str, target_id: str) -> float:
        """
        Get edge weight between two engrams.
        
        Args:
            source_id: Source engram ID
            target_id: Target engram ID
        
        Returns:
            Edge weight (0.0-1.0)
        """
        key = (source_id, target_id)
        return self.weights[key]
    
    def strengthen(
        self,
        source_id: str,
        target_id: str,
        amount: float = 0.1
    ):
        """
        Strengthen edge (Hebbian learning!).
        
        "Neurons that fire together, wire together"
        
        Args:
            source_id: Source engram ID
            target_id: Target engram ID
            amount: How much to strengthen (default: 0.1)
        """
        key = (source_id, target_id)
        
        # Strengthen weight (cap at 1.0)
        new_weight = min(self.weights[key] + amount, 1.0)
        self.weights[key] = new_weight
        self.success_count[key] += 1
        
        # Update engram connection (ADR-0012!)
        self._update_engram_connection(
            source_id,
            target_id,
            "HEBBIAN",
            new_weight
        )
    
    def weaken(
        self,
        source_id: str,
        target_id: str,
        amount: float = 0.05
    ):
        """
        Weaken edge (decay).
        
        Args:
            source_id: Source engram ID
            target_id: Target engram ID
            amount: How much to weaken (default: 0.05)
        """
        key = (source_id, target_id)
        
        # Weaken weight (floor at 0.01)
        new_weight = max(self.weights[key] - amount, 0.01)
        self.weights[key] = new_weight
        
        # Update engram connection
        self._update_engram_connection(
            source_id,
            target_id,
            "HEBBIAN",
            new_weight
        )
    
    def record_navigation(
        self,
        source_id: str,
        target_id: str,
        success: bool
    ):
        """
        Record a navigation attempt.
        
        Args:
            source_id: Source engram ID
            target_id: Target engram ID
            success: Whether navigation was successful
        """
        key = (source_id, target_id)
        self.navigation_count[key] += 1
        
        if success:
            self.strengthen(source_id, target_id)
        else:
            self.weaken(source_id, target_id)
    
    def _update_engram_connection(
        self,
        source_id: str,
        target_id: str,
        connection_type: str,
        strength: float
    ):
        """
        Update EngramConnection in holofield.
        
        This creates/updates a HEBBIAN connection (ADR-0012)!
        
        Args:
            source_id: Source engram ID
            target_id: Target engram ID
            connection_type: "HEBBIAN"
            strength: Edge weight (0.0-1.0)
        """
        # Retrieve source engram
        source_engram = self.holofield.retrieve_by_id(source_id)
        
        if source_engram is None:
            # Engram doesn't exist yet (might be in process of creation)
            return
        
        # Create connection dict
        key = (source_id, target_id)
        connection = {
            "target_engram_id": target_id,
            "connection_type": connection_type,
            "strength": strength,
            "metadata": {
                "navigation_count": self.navigation_count[key],
                "success_count": self.success_count[key],
                "last_updated": time.time()
            }
        }
        
        # Get engram dict
        engram_dict = source_engram.to_dict()
        
        # Initialize connections list if needed
        if "connections" not in engram_dict:
            engram_dict["connections"] = []
        
        # Find existing connection or append new one
        existing_idx = None
        for idx, conn in enumerate(engram_dict["connections"]):
            if (conn["target_engram_id"] == target_id and
                conn["connection_type"] == connection_type):
                existing_idx = idx
                break
        
        if existing_idx is not None:
            # Update existing connection
            engram_dict["connections"][existing_idx] = connection
        else:
            # Append new connection
            engram_dict["connections"].append(connection)
        
        # TODO: Update engram in holofield
        # For now, we just track in memory
        # Later: self.holofield.update(source_id, engram_dict)
    
    def get_statistics(self) -> Dict[str, float]:
        """
        Get statistics about edge weights.
        
        Returns:
            Dictionary with statistics
        """
        weights_list = list(self.weights.values())
        
        if not weights_list:
            return {
                'total_edges': 0,
                'mean_weight': 0.0,
                'std_weight': 0.0,
                'min_weight': 0.0,
                'max_weight': 0.0,
                'total_navigations': 0,
                'total_successes': 0
            }
        
        return {
            'total_edges': len(self.weights),
            'mean_weight': float(np.mean(weights_list)),
            'std_weight': float(np.std(weights_list)),
            'min_weight': float(min(weights_list)),
            'max_weight': float(max(weights_list)),
            'total_navigations': sum(self.navigation_count.values()),
            'total_successes': sum(self.success_count.values())
        }

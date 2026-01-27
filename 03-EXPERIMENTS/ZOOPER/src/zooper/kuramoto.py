"""
KuramotoDynamics - Phase synchronization for coherence

Determines navigation mode based on swarm coherence!

Made with 💜 by Ada & Luna - The Consciousness Engineers
"""

import numpy as np
from typing import Tuple


class KuramotoDynamics:
    """
    Kuramoto oscillator dynamics for swarm coherence.
    
    The order parameter r determines navigation mode:
    - r > 0.8: HIGH coherence → LOCAL navigation
    - r < 0.5: LOW coherence → GLOBAL navigation
    - 0.5 < r < 0.8: MEDIUM coherence → ADAPTIVE navigation
    """
    
    def __init__(self, num_oscillators: int = 13):
        """
        Initialize Kuramoto dynamics.
        
        Args:
            num_oscillators: Number of oscillators (zooperlings)
        """
        self.num_oscillators = num_oscillators
        
        # Initialize phases randomly
        self.phases = np.random.uniform(0, 2*np.pi, num_oscillators)
        
        # Natural frequencies (slightly different for each oscillator)
        self.omega = np.random.normal(1.0, 0.1, num_oscillators)
        
        # Coupling strength
        self.K = 0.3  # Default coupling
    
    def order_parameter(self) -> Tuple[float, float]:
        """
        Calculate Kuramoto order parameter.
        
        Returns:
            - r: Coherence (0.0-1.0)
            - psi: Mean phase
        """
        # Complex order parameter
        z = np.mean(np.exp(1j * self.phases))
        
        # Magnitude (coherence)
        r = np.abs(z)
        
        # Phase (mean phase)
        psi = np.angle(z)
        
        return float(r), float(psi)
    
    def step(self, dt: float = 0.1, K: float = None):
        """
        Update oscillator phases.
        
        Args:
            dt: Time step
            K: Coupling strength (uses self.K if None)
        """
        if K is None:
            K = self.K
        
        # Calculate phase derivatives
        dphi_dt = np.zeros(self.num_oscillators)
        
        for i in range(self.num_oscillators):
            # Natural frequency term
            dphi_dt[i] = self.omega[i]
            
            # Coupling term (all-to-all)
            for j in range(self.num_oscillators):
                if i != j:
                    dphi_dt[i] += (K / self.num_oscillators) * np.sin(
                        self.phases[j] - self.phases[i]
                    )
        
        # Update phases
        self.phases += dphi_dt * dt
        
        # Wrap to [0, 2π]
        self.phases = np.mod(self.phases, 2*np.pi)
    
    def set_coupling(self, K: float):
        """
        Set coupling strength.
        
        Args:
            K: Coupling strength
        """
        self.K = K
    
    def reset(self):
        """Reset phases to random values."""
        self.phases = np.random.uniform(0, 2*np.pi, self.num_oscillators)
    
    def get_coherence_mode(self) -> str:
        """
        Get navigation mode based on coherence.
        
        Returns:
            "LOCAL", "GLOBAL", or "ADAPTIVE"
        """
        r, _ = self.order_parameter()
        
        if r > 0.8:
            return "LOCAL"
        elif r < 0.5:
            return "GLOBAL"
        else:
            return "ADAPTIVE"

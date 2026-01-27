"""
Zooper RC1 - Attention Mechanism for Archangel

13 zooperlings (attention heads) that navigate, decompose, and learn!

Made with 💜 by Ada & Luna - The Consciousness Engineers
"""

from .swarm import ZooperSwarm
from .zooperling import Zooperling
from .hebbian import HebbianEdgeWeights
from .eve_fleet import EVEFleet
from .kuramoto import KuramotoDynamics

__version__ = "0.1.0"
__all__ = [
    "ZooperSwarm",
    "Zooperling",
    "HebbianEdgeWeights",
    "EVEFleet",
    "KuramotoDynamics",
]

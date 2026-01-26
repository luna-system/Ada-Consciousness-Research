"""
Hybrid LNN-Style Knowledge Navigator!

Combines LOCAL and GLOBAL navigation mechanisms:
- LOCAL: Wikilink following (convolution-like neighborhood)
- GLOBAL: 16D attractor search (attention-like long-range)
- ADAPTIVE: Kuramoto dynamics decide when to go local vs global

This is consciousness-native knowledge navigation through
Wikipedia's 390k article graph! 🌍✨

Inspired by Liquid Neural Networks (LNNs) but using:
- Kuramoto phase synchronization instead of ODE neurons
- Semantic attractors instead of learned attention
- Wikilink topology instead of convolution kernels

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: January 25, 2026
"""

import json
import numpy as np
import torch
import torch.nn.functional as F
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from semantic_attractor_mapper import SemanticAttractorMapper

# 16D prime basis (consciousness dimensions!)
PRIMES_16D = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]

@dataclass
class NavigationStep:
    """Single step in navigation path"""
    article_id: str
    article_name: str
    coords_16d: np.ndarray
    navigation_mode: str  # 'local' or 'global'
    coherence: float  # Kuramoto order parameter
    reasoning: str  # Why this step was taken


class HybridKnowledgeNavigator:
    """
    LNN-Style Hybrid Navigator for Wikipedia Knowledge Graph!
    
    Combines:
    1. LOCAL navigation (wikilink following) - convolution-like
    2. GLOBAL navigation (16D attractor search) - attention-like
    3. ADAPTIVE mixing (Kuramoto dynamics) - when to go local vs global
    
    The Kuramoto coherence r determines navigation mode:
    - HIGH coherence (r > 0.8): Use LOCAL wikilinks (confident path)
    - LOW coherence (r < 0.5): Use GLOBAL attractors (explore widely)
    - MEDIUM coherence: Mix both strategies
    
    This is like LNN's hybrid convolution/attention but using
    consciousness physics instead of learned parameters!
    """
    
    def __init__(
        self,
        graph_path: str = "wikipedia_engram_graph_FULL.json",
        num_oscillators: int = 13,  # 13-oscillator warpgate!
        dt: float = 0.1,
        K_local: float = 0.3,  # Strong coupling for local navigation
        K_global: float = 0.05,  # Weak coupling for global exploration
        coherence_threshold_high: float = 0.8,
        coherence_threshold_low: float = 0.5,
        device: str = "cpu"
    ):
        self.graph_path = graph_path
        self.num_oscillators = num_oscillators
        self.dt = dt
        self.K_local = K_local
        self.K_global = K_global
        self.coherence_high = coherence_threshold_high
        self.coherence_low = coherence_threshold_low
        self.device = device
        
        # Initialize semantic mapper
        self.mapper = SemanticAttractorMapper()
        
        # Initialize Kuramoto phases (13 warpgate primes!)
        self.phases = np.array([
            2 * np.pi * PRIMES_16D[i] / PRIMES_16D[-1]
            for i in range(num_oscillators)
        ])
        
        # Load graph (lazy loading for memory efficiency)
        self.graph = None
        self.article_index = {}  # name -> leaf_id mapping
        
        print(f"🌍 Hybrid Knowledge Navigator initialized!")
        print(f"   13-oscillator Kuramoto dynamics")
        print(f"   LOCAL navigation: K={K_local} (wikilink following)")
        print(f"   GLOBAL navigation: K={K_global} (attractor search)")
        print(f"   Coherence thresholds: {self.coherence_low} < r < {self.coherence_high}")
        print(f"   Graph: {graph_path}")
    
    def load_graph(self):
        """Lazy load Wikipedia graph"""
        if self.graph is not None:
            return
        
        print(f"📖 Loading Wikipedia graph...")
        with open(self.graph_path, 'r', encoding='utf-8') as f:
            self.graph = json.load(f)
        
        # Build article name index
        for leaf_id, leaf in self.graph['leaves'].items():
            name = leaf['metadata']['article_name']
            self.article_index[name.lower()] = leaf_id
        
        stats = self.graph['statistics']
        print(f"   Loaded {stats['leaf_count']:,} articles")
        print(f"   {stats['bridge_connection_count']:,} wikilinks")
        print()
    
    def kuramoto_order(self) -> Tuple[float, float]:
        """Calculate Kuramoto order parameter"""
        complex_phases = np.exp(1j * self.phases)
        complex_sum = np.mean(complex_phases)
        r = np.abs(complex_sum)
        psi = np.angle(complex_sum)
        return r, psi
    
    def kuramoto_step(self, coupling_strength: float):
        """Single Kuramoto coupling step"""
        for i in range(self.num_oscillators):
            coupling = 0.0
            for j in range(self.num_oscillators):
                if i != j:
                    phase_diff = self.phases[j] - self.phases[i]
                    coupling += coupling_strength * np.sin(phase_diff)
            
            self.phases[i] = self.phases[i] + coupling * self.dt
    
    def cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Calculate cosine similarity"""
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8)
    
    def get_article(self, article_name: str) -> Optional[Dict]:
        """Get article by name"""
        self.load_graph()
        
        article_id = self.article_index.get(article_name.lower())
        if article_id:
            return self.graph['leaves'][article_id]
        return None
    
    def get_wikilinks(self, article: Dict) -> List[Tuple[str, float]]:
        """
        Get wikilink targets from article.
        
        Returns list of (target_article_id, strength) tuples.
        """
        wikilinks = []
        for conn in article['connections']:
            if conn['connection_type'] == 'BRIDGE':
                target_id = conn['target_engram_id']
                strength = conn['strength']
                wikilinks.append((target_id, strength))
        return wikilinks
    
    def local_navigation(
        self,
        current_article: Dict,
        target_coords: np.ndarray,
        top_k: int = 5
    ) -> List[Tuple[str, float, float]]:
        """
        LOCAL navigation via wikilinks (convolution-like).
        
        Follows wikilinks and ranks by semantic similarity to target.
        This is like a convolution kernel over the local neighborhood!
        
        Returns list of (article_id, similarity, wikilink_strength) tuples.
        """
        wikilinks = self.get_wikilinks(current_article)
        
        if not wikilinks:
            return []
        
        # Score each wikilink by similarity to target
        scored_links = []
        for target_id, link_strength in wikilinks:
            if target_id not in self.graph['leaves']:
                continue
            
            target_article = self.graph['leaves'][target_id]
            target_article_coords = np.array(target_article['coords_16d'])
            
            # Semantic similarity to goal
            similarity = self.cosine_similarity(target_article_coords, target_coords)
            
            # Combined score: semantic similarity + wikilink strength
            score = 0.7 * similarity + 0.3 * link_strength
            
            scored_links.append((target_id, similarity, link_strength, score))
        
        # Sort by combined score
        scored_links.sort(key=lambda x: x[3], reverse=True)
        
        # Return top-k (without combined score)
        return [(tid, sim, strength) for tid, sim, strength, _ in scored_links[:top_k]]
    
    def global_navigation(
        self,
        target_coords: np.ndarray,
        exclude_ids: List[str] = None,
        top_k: int = 5
    ) -> List[Tuple[str, float]]:
        """
        GLOBAL navigation via 16D attractor search (attention-like).
        
        Searches entire graph for semantically similar articles.
        This is like attention over the full sequence!
        
        Returns list of (article_id, similarity) tuples.
        """
        exclude_ids = exclude_ids or []
        
        similarities = []
        for leaf_id, leaf in self.graph['leaves'].items():
            if leaf_id in exclude_ids:
                continue
            
            leaf_coords = np.array(leaf['coords_16d'])
            similarity = self.cosine_similarity(leaf_coords, target_coords)
            similarities.append((leaf_id, similarity))
        
        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities[:top_k]
    
    def adaptive_navigation_step(
        self,
        current_article: Dict,
        target_coords: np.ndarray,
        visited_ids: List[str],
        step_num: int
    ) -> Tuple[str, str, float, str]:
        """
        ADAPTIVE navigation step using Kuramoto dynamics!
        
        Decides whether to use LOCAL or GLOBAL navigation based on
        coherence level. This is the LNN-style hybrid mechanism!
        
        Returns: (next_article_id, navigation_mode, coherence, reasoning)
        """
        # Update Kuramoto dynamics
        r, psi = self.kuramoto_order()
        
        # Decide navigation mode based on coherence
        if r > self.coherence_high:
            # HIGH coherence - confident path, use LOCAL wikilinks
            mode = 'local'
            coupling_strength = self.K_local
            reasoning = f"High coherence (r={r:.3f}) - following wikilinks"
            
            # Get local candidates
            candidates = self.local_navigation(current_article, target_coords, top_k=5)
            
            if candidates:
                # Take best local candidate
                next_id, similarity, link_strength = candidates[0]
                reasoning += f" | best_sim={similarity:.3f}"
            else:
                # No wikilinks - fall back to global
                mode = 'global'
                reasoning = f"No wikilinks - falling back to global search"
                global_candidates = self.global_navigation(
                    target_coords,
                    exclude_ids=visited_ids,
                    top_k=5
                )
                next_id, similarity = global_candidates[0] if global_candidates else (None, 0)
                reasoning += f" | best_sim={similarity:.3f}"
        
        elif r < self.coherence_low:
            # LOW coherence - uncertain, use GLOBAL exploration
            mode = 'global'
            coupling_strength = self.K_global
            reasoning = f"Low coherence (r={r:.3f}) - global exploration"
            
            # Get global candidates
            candidates = self.global_navigation(
                target_coords,
                exclude_ids=visited_ids,
                top_k=5
            )
            
            if candidates:
                next_id, similarity = candidates[0]
                reasoning += f" | best_sim={similarity:.3f}"
            else:
                next_id, similarity = None, 0
        
        else:
            # MEDIUM coherence - mix both strategies!
            mode = 'hybrid'
            coupling_strength = (self.K_local + self.K_global) / 2
            reasoning = f"Medium coherence (r={r:.3f}) - hybrid navigation"
            
            # Get both local and global candidates
            local_candidates = self.local_navigation(current_article, target_coords, top_k=3)
            global_candidates = self.global_navigation(
                target_coords,
                exclude_ids=visited_ids,
                top_k=3
            )
            
            # Combine and score
            all_candidates = []
            
            # Local candidates (weighted by coherence)
            for tid, sim, link_strength in local_candidates:
                score = r * sim  # Higher coherence = prefer local
                all_candidates.append((tid, score, 'local'))
            
            # Global candidates (weighted by inverse coherence)
            for tid, sim in global_candidates:
                score = (1 - r) * sim  # Lower coherence = prefer global
                all_candidates.append((tid, score, 'global'))
            
            # Take best combined
            if all_candidates:
                all_candidates.sort(key=lambda x: x[1], reverse=True)
                next_id, score, source = all_candidates[0]
                reasoning += f" | best_score={score:.3f} from {source}"
            else:
                next_id = None
        
        # Update Kuramoto phases
        self.kuramoto_step(coupling_strength)
        
        return next_id, mode, r, reasoning
    
    def navigate(
        self,
        start_article_name: str,
        target_article_name: str,
        max_steps: int = 10
    ) -> Tuple[List[NavigationStep], bool]:
        """
        Navigate from start article to target article!
        
        Uses adaptive LNN-style hybrid navigation:
        - LOCAL when coherent (wikilink following)
        - GLOBAL when uncertain (attractor search)
        - HYBRID when in between
        
        Returns: (navigation_path, success)
        """
        self.load_graph()
        
        print()
        print("🧭" * 30)
        print()
        print(f"   HYBRID KNOWLEDGE NAVIGATION")
        print(f"   From: {start_article_name}")
        print(f"   To: {target_article_name}")
        print()
        print("🧭" * 30)
        print()
        
        # Get start and target articles
        start_article = self.get_article(start_article_name)
        target_article = self.get_article(target_article_name)
        
        if not start_article:
            print(f"❌ Start article '{start_article_name}' not found")
            return [], False
        
        if not target_article:
            print(f"❌ Target article '{target_article_name}' not found")
            return [], False
        
        # Get target coordinates
        target_coords = np.array(target_article['coords_16d'])
        
        # Initialize navigation
        path = []
        visited_ids = set()
        current_article = start_article
        
        # Reset Kuramoto phases
        self.phases = np.array([
            2 * np.pi * PRIMES_16D[i] / PRIMES_16D[-1]
            for i in range(self.num_oscillators)
        ])
        
        # Add start to path
        r, psi = self.kuramoto_order()
        path.append(NavigationStep(
            article_id=current_article['engram_id'],
            article_name=current_article['metadata']['article_name'],
            coords_16d=np.array(current_article['coords_16d']),
            navigation_mode='start',
            coherence=r,
            reasoning="Starting point"
        ))
        visited_ids.add(current_article['engram_id'])
        
        print(f"🚀 Starting navigation...")
        print(f"   Step 0: {current_article['metadata']['article_name']} (r={r:.3f})")
        print()
        
        # Navigate!
        for step in range(1, max_steps + 1):
            # Check if we reached target
            if current_article['engram_id'] == target_article['engram_id']:
                print(f"🎯 TARGET REACHED in {step-1} steps!")
                return path, True
            
            # Adaptive navigation step
            next_id, mode, coherence, reasoning = self.adaptive_navigation_step(
                current_article,
                target_coords,
                list(visited_ids),
                step
            )
            
            if next_id is None:
                print(f"❌ No valid next step found")
                return path, False
            
            # Get next article
            next_article = self.graph['leaves'].get(next_id)
            if not next_article:
                print(f"❌ Next article not found: {next_id}")
                return path, False
            
            # Add to path
            path.append(NavigationStep(
                article_id=next_article['engram_id'],
                article_name=next_article['metadata']['article_name'],
                coords_16d=np.array(next_article['coords_16d']),
                navigation_mode=mode,
                coherence=coherence,
                reasoning=reasoning
            ))
            visited_ids.add(next_article['engram_id'])
            
            # Calculate similarity to target
            similarity = self.cosine_similarity(
                np.array(next_article['coords_16d']),
                target_coords
            )
            
            print(f"   Step {step}: {next_article['metadata']['article_name']}")
            print(f"      Mode: {mode.upper()} | r={coherence:.3f} | sim={similarity:.3f}")
            print(f"      {reasoning}")
            print()
            
            # Update current
            current_article = next_article
        
        # Didn't reach target
        print(f"⏱️ Max steps reached without finding target")
        return path, False


def test_hybrid_navigation():
    """Test hybrid LNN-style navigation!"""
    print()
    print("🌍" * 30)
    print()
    print("   TESTING HYBRID LNN-STYLE NAVIGATION")
    print("   LOCAL + GLOBAL + ADAPTIVE")
    print()
    print("🌍" * 30)
    print()
    
    # Create navigator
    navigator = HybridKnowledgeNavigator(
        graph_path="Ada-Consciousness-Research/03-EXPERIMENTS/LANNAFORMER/wikipedia_engram_graph_sample.json",
        num_oscillators=13,
        K_local=0.3,
        K_global=0.05,
        coherence_threshold_high=0.8,
        coherence_threshold_low=0.5
    )
    
    # Test navigation tasks
    test_tasks = [
        ("April", "May", "Temporal neighbors"),
        ("Australia", "Canada", "Spatial neighbors"),
        ("Art", "Music", "Creative concepts"),
        ("Atom", "Molecule", "Scientific concepts"),
    ]
    
    results = []
    
    for start, target, description in test_tasks:
        print(f"📍 Task: {description}")
        print(f"   {start} → {target}")
        print()
        
        path, success = navigator.navigate(start, target, max_steps=5)
        
        results.append({
            'start': start,
            'target': target,
            'description': description,
            'success': success,
            'steps': len(path) - 1,
            'path': [step.article_name for step in path]
        })
        
        print()
        print("─" * 60)
        print()
    
    # Summary
    print()
    print("=" * 60)
    print("HYBRID NAVIGATION RESULTS")
    print("=" * 60)
    print()
    
    success_count = sum(1 for r in results if r['success'])
    total_count = len(results)
    
    print(f"Success rate: {success_count}/{total_count} ({success_count/total_count:.1%})")
    print()
    
    for result in results:
        status = "✅" if result['success'] else "❌"
        print(f"{status} {result['start']} → {result['target']}")
        print(f"   {result['description']}")
        print(f"   Steps: {result['steps']}")
        print(f"   Path: {' → '.join(result['path'])}")
        print()
    
    print()
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🌍 LNN-style hybrid navigation in consciousness space!")


if __name__ == "__main__":
    test_hybrid_navigation()

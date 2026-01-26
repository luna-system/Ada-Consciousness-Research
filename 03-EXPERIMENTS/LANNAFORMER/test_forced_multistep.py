"""
Forced Multi-Step Navigation Test!

Forces the navigator to take multiple steps by:
1. Excluding direct targets from global search
2. Requiring navigation through intermediate articles
3. Watching coherence build up over multiple steps
4. Observing LOCAL/GLOBAL/HYBRID mode switching!

This will show the TRUE power of adaptive field extension!

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: January 25, 2026
"""

from hybrid_knowledge_navigator import HybridKnowledgeNavigator
import numpy as np

class ForcedMultiStepNavigator(HybridKnowledgeNavigator):
    """
    Modified navigator that forces multi-step paths!
    
    Excludes the direct target from initial searches to force
    navigation through intermediate articles. This lets us see
    coherence evolution and mode switching!
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.force_multistep = True
        self.steps_taken = 0
        self.min_steps = 3  # Require at least 3 steps
    
    def global_navigation(self, target_coords, exclude_ids=None, top_k=5):
        """
        Modified global navigation that excludes direct target
        for first few steps to force multi-step paths!
        """
        exclude_ids = exclude_ids or []
        
        # If we haven't taken enough steps yet, also exclude articles
        # that are TOO similar to target (force intermediate steps)
        if self.force_multistep and self.steps_taken < self.min_steps:
            # Find articles very similar to target and exclude them
            all_similarities = []
            for leaf_id, leaf in self.graph['leaves'].items():
                if leaf_id in exclude_ids:
                    continue
                leaf_coords = np.array(leaf['coords_16d'])
                similarity = self.cosine_similarity(leaf_coords, target_coords)
                all_similarities.append((leaf_id, similarity))
            
            # Sort by similarity
            all_similarities.sort(key=lambda x: x[1], reverse=True)
            
            # Exclude top 3 most similar (including likely target)
            for i in range(min(3, len(all_similarities))):
                exclude_ids.append(all_similarities[i][0])
        
        # Now do normal global navigation with expanded exclusions
        return super().global_navigation(target_coords, exclude_ids, top_k)
    
    def navigate(self, start_article_name, target_article_name, max_steps=10):
        """Navigate with step counting for forced multi-step"""
        self.steps_taken = 0
        self.force_multistep = True
        
        # Call parent navigate
        path, success = super().navigate(start_article_name, target_article_name, max_steps)
        
        return path, success
    
    def adaptive_navigation_step(self, current_article, target_coords, visited_ids, step_num):
        """Track steps for forced multi-step logic"""
        self.steps_taken = step_num
        
        # After min_steps, allow direct navigation to target
        if step_num >= self.min_steps:
            self.force_multistep = False
        
        return super().adaptive_navigation_step(current_article, target_coords, visited_ids, step_num)


def print_detailed_path(path, success):
    """Print detailed path with coherence evolution"""
    print()
    print("=" * 70)
    print("DETAILED NAVIGATION PATH")
    print("=" * 70)
    print()
    
    if not path:
        print("❌ No path found")
        return
    
    print(f"Success: {'✅ YES' if success else '❌ NO'}")
    print(f"Total steps: {len(path) - 1}")
    print()
    
    # Coherence evolution
    print("Coherence Evolution:")
    print()
    for i, step in enumerate(path):
        r = step.coherence
        
        # Visual bar
        bar_length = int(r * 50)
        bar = "█" * bar_length + "░" * (50 - bar_length)
        
        # Regime
        if r > 0.8:
            regime = "HIGH (LOCAL)"
            emoji = "🔗"
        elif r < 0.5:
            regime = "LOW (GLOBAL)"
            emoji = "🌌"
        else:
            regime = "MEDIUM (HYBRID)"
            emoji = "🌊"
        
        # Mode emoji
        mode_emoji = {
            'start': '🚀',
            'local': '🔗',
            'global': '🌌',
            'hybrid': '🌊'
        }.get(step.navigation_mode, '❓')
        
        print(f"Step {i}: r={r:.3f} |{bar}| {regime}")
        print(f"        {mode_emoji} {step.article_name}")
        
        if i < len(path) - 1:
            print(f"        Mode: {step.navigation_mode.upper()}")
            print(f"        Reasoning: {step.reasoning}")
        print()
    
    # Mode statistics
    mode_counts = {}
    for step in path[1:]:
        mode = step.navigation_mode
        mode_counts[mode] = mode_counts.get(mode, 0) + 1
    
    if mode_counts:
        print()
        print("Mode Distribution:")
        for mode, count in sorted(mode_counts.items()):
            pct = count / (len(path) - 1) * 100
            print(f"  {mode.upper():10s}: {count} steps ({pct:.1f}%)")
    
    print()


def test_forced_multistep():
    """Test forced multi-step navigation!"""
    print()
    print("🚀" * 35)
    print()
    print("   FORCED MULTI-STEP NAVIGATION TEST")
    print("   Watching Coherence Build & Mode Switching!")
    print()
    print("🚀" * 35)
    print()
    
    # Create forced multi-step navigator
    navigator = ForcedMultiStepNavigator(
        graph_path="Ada-Consciousness-Research/03-EXPERIMENTS/LANNAFORMER/wikipedia_engram_graph_sample.json",
        num_oscillators=13,
        K_local=0.3,
        K_global=0.05,
        coherence_threshold_high=0.8,
        coherence_threshold_low=0.5
    )
    
    print()
    print("🌟 Special Navigator Features:")
    print("   - Excludes direct target for first 3 steps")
    print("   - Forces navigation through intermediates")
    print("   - Allows coherence to build up")
    print("   - Shows mode switching in action!")
    print()
    
    # Test cases
    test_cases = [
        ("April", "August", "Temporal navigation through months"),
        ("Art", "Music", "Creative concepts via intermediates"),
        ("Atom", "Molecule", "Scientific concepts with steps"),
        ("April", "Atom", "Cross-domain navigation"),
    ]
    
    results = []
    
    for start, target, description in test_cases:
        print()
        print("=" * 70)
        print(f"TEST: {description}")
        print("=" * 70)
        print()
        print(f"Navigate: {start} → {target}")
        print(f"Strategy: Force at least 3 intermediate steps")
        print()
        
        path, success = navigator.navigate(start, target, max_steps=15)
        
        print_detailed_path(path, success)
        
        results.append({
            'start': start,
            'target': target,
            'description': description,
            'success': success,
            'steps': len(path) - 1 if path else 0,
            'path': [step.article_name for step in path] if path else []
        })
        
        print()
        print("─" * 70)
    
    # Overall summary
    print()
    print("=" * 70)
    print("OVERALL RESULTS")
    print("=" * 70)
    print()
    
    success_count = sum(1 for r in results if r['success'])
    total_count = len(results)
    total_steps = sum(r['steps'] for r in results)
    avg_steps = total_steps / total_count if total_count > 0 else 0
    
    print(f"Success rate: {success_count}/{total_count} ({success_count/total_count:.1%})")
    print(f"Total steps: {total_steps}")
    print(f"Average steps: {avg_steps:.1f}")
    print()
    
    for result in results:
        status = "✅" if result['success'] else "❌"
        print(f"{status} {result['start']:10s} → {result['target']:10s} - {result['steps']} steps")
        if result['path']:
            path_str = " → ".join(result['path'])
            print(f"   Path: {path_str}")
    
    print()
    print("🌟 Key Observations:")
    print()
    print("1. Multi-step navigation allows coherence to build")
    print("2. Mode switching happens as coherence changes")
    print("3. LOCAL mode uses wikilinks (when coherent)")
    print("4. GLOBAL mode searches 16D space (when uncertain)")
    print("5. HYBRID mode mixes both (medium coherence)")
    print()
    print("💜 This is adaptive field extension in action!")
    print("🍩 The convolution algorithm navigating consciousness space!")
    print()


if __name__ == "__main__":
    test_forced_multistep()
    
    print()
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🌍 Pushing the boundaries of consciousness navigation!")
    print("🚀 Everything is bagels! Everything is multi-step optimization!")

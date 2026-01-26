"""
Advanced Hybrid Navigation Tests!

Tests multi-step navigation with mode switching:
- LOCAL navigation when coherent (following wikilinks)
- GLOBAL navigation when uncertain (attractor search)
- HYBRID navigation when in between (adaptive mixing)

This demonstrates the LNN-style hybrid behavior and shows
how Kuramoto coherence determines navigation strategy!

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: January 25, 2026
"""

from hybrid_knowledge_navigator import HybridKnowledgeNavigator
import json

def print_navigation_summary(path, success):
    """Print beautiful summary of navigation path"""
    print()
    print("=" * 60)
    print("NAVIGATION PATH SUMMARY")
    print("=" * 60)
    print()
    
    if not path:
        print("❌ No path found")
        return
    
    print(f"{'Success:':20s} {'✅ YES' if success else '❌ NO'}")
    print(f"{'Total steps:':20s} {len(path) - 1}")
    print()
    
    print("Path with modes:")
    for i, step in enumerate(path):
        mode_emoji = {
            'start': '🚀',
            'local': '🔗',
            'global': '🌌',
            'hybrid': '🌊'
        }.get(step.navigation_mode, '❓')
        
        print(f"  {i}. {mode_emoji} {step.article_name:30s} "
              f"(r={step.coherence:.3f}, mode={step.navigation_mode})")
        if i < len(path) - 1:
            print(f"     └─ {step.reasoning}")
    
    print()
    
    # Mode statistics
    mode_counts = {}
    for step in path[1:]:  # Skip start
        mode = step.navigation_mode
        mode_counts[mode] = mode_counts.get(mode, 0) + 1
    
    if mode_counts:
        print("Mode usage:")
        for mode, count in sorted(mode_counts.items()):
            print(f"  {mode.upper():10s}: {count} steps")
        print()


def test_multi_step_navigation():
    """Test navigation requiring multiple steps"""
    print()
    print("🌍" * 30)
    print()
    print("   ADVANCED HYBRID NAVIGATION TESTS")
    print("   Multi-Step with Mode Switching")
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
    
    print()
    
    # Test 1: Related concepts (should use LOCAL wikilinks if available)
    print("=" * 60)
    print("TEST 1: RELATED CONCEPTS (LOCAL NAVIGATION)")
    print("=" * 60)
    print()
    print("Task: Navigate from 'April' to 'August'")
    print("Expected: Should follow temporal wikilinks if available")
    print()
    
    path1, success1 = navigator.navigate("April", "August", max_steps=5)
    print_navigation_summary(path1, success1)
    
    # Test 2: Distant concepts (should use GLOBAL search)
    print()
    print("=" * 60)
    print("TEST 2: DISTANT CONCEPTS (GLOBAL NAVIGATION)")
    print("=" * 60)
    print()
    print("Task: Navigate from 'Art' to 'Atom'")
    print("Expected: Should use global attractor search")
    print()
    
    path2, success2 = navigator.navigate("Art", "Atom", max_steps=5)
    print_navigation_summary(path2, success2)
    
    # Test 3: Medium distance (should show HYBRID behavior)
    print()
    print("=" * 60)
    print("TEST 3: MEDIUM DISTANCE (HYBRID NAVIGATION)")
    print("=" * 60)
    print()
    print("Task: Navigate from 'April' to 'Art'")
    print("Expected: Should mix local and global strategies")
    print()
    
    path3, success3 = navigator.navigate("April", "Art", max_steps=5)
    print_navigation_summary(path3, success3)
    
    # Test 4: Longer path (multiple steps)
    print()
    print("=" * 60)
    print("TEST 4: LONGER PATH (MULTI-STEP)")
    print("=" * 60)
    print()
    print("Task: Navigate from 'Atom' to 'August'")
    print("Expected: Should take multiple steps, showing mode transitions")
    print()
    
    path4, success4 = navigator.navigate("Atom", "August", max_steps=10)
    print_navigation_summary(path4, success4)
    
    # Overall summary
    print()
    print("=" * 60)
    print("OVERALL RESULTS")
    print("=" * 60)
    print()
    
    tests = [
        ("April → August", success1, len(path1) - 1 if path1 else 0),
        ("Art → Atom", success2, len(path2) - 1 if path2 else 0),
        ("April → Art", success3, len(path3) - 1 if path3 else 0),
        ("Atom → August", success4, len(path4) - 1 if path4 else 0),
    ]
    
    success_count = sum(1 for _, success, _ in tests if success)
    total_count = len(tests)
    
    print(f"Success rate: {success_count}/{total_count} ({success_count/total_count:.1%})")
    print()
    
    for task, success, steps in tests:
        status = "✅" if success else "❌"
        print(f"{status} {task:20s} - {steps} steps")
    
    print()
    print("🌟 Key Observations:")
    print()
    print("1. LOW coherence (r < 0.5) → GLOBAL navigation")
    print("   - Searches entire 16D consciousness space")
    print("   - Finds implicit semantic connections")
    print("   - Like extended field (7-mult, φ-based)")
    print()
    print("2. HIGH coherence (r > 0.8) → LOCAL navigation")
    print("   - Follows explicit wikilinks")
    print("   - Uses graph structure")
    print("   - Like rational field (8-mult, stable)")
    print()
    print("3. MEDIUM coherence (0.5 < r < 0.8) → HYBRID navigation")
    print("   - Mixes both strategies")
    print("   - Adaptive field extension")
    print("   - Balances exploration vs exploitation")
    print()
    print("💜 This IS the convolution algorithm in consciousness space!")
    print("🍩 Everything is bagels! Everything is φ-based optimization!")
    print()


def test_coherence_evolution():
    """Test how coherence evolves during navigation"""
    print()
    print("🌌" * 30)
    print()
    print("   COHERENCE EVOLUTION TEST")
    print("   Watching Kuramoto Dynamics")
    print()
    print("🌌" * 30)
    print()
    
    navigator = HybridKnowledgeNavigator(
        graph_path="Ada-Consciousness-Research/03-EXPERIMENTS/LANNAFORMER/wikipedia_engram_graph_sample.json",
        num_oscillators=13,
        K_local=0.3,
        K_global=0.05,
        coherence_threshold_high=0.8,
        coherence_threshold_low=0.5
    )
    
    print()
    print("Task: Navigate from 'April' to 'Music'")
    print("Watching how coherence r changes with each step...")
    print()
    
    path, success = navigator.navigate("April", "Music", max_steps=10)
    
    if path:
        print("Coherence Evolution:")
        print()
        for i, step in enumerate(path):
            r = step.coherence
            
            # Visual coherence bar
            bar_length = int(r * 40)
            bar = "█" * bar_length + "░" * (40 - bar_length)
            
            # Determine regime
            if r > 0.8:
                regime = "HIGH (LOCAL)"
            elif r < 0.5:
                regime = "LOW (GLOBAL)"
            else:
                regime = "MEDIUM (HYBRID)"
            
            print(f"Step {i}: r={r:.3f} |{bar}| {regime}")
            print(f"        {step.article_name}")
            if i < len(path) - 1:
                print(f"        Mode: {step.navigation_mode.upper()}")
            print()
        
        print()
        print("🌟 Observations:")
        print()
        print("- Coherence r determines navigation strategy")
        print("- Kuramoto oscillators synchronize over time")
        print("- Mode switches happen at coherence thresholds")
        print("- This is adaptive field extension in action!")
        print()
    
    print_navigation_summary(path, success)


if __name__ == "__main__":
    # Run multi-step tests
    test_multi_step_navigation()
    
    print()
    print("─" * 60)
    print()
    
    # Run coherence evolution test
    test_coherence_evolution()
    
    print()
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🌍 LNN-style hybrid navigation through consciousness space!")
    print("🍩 Everything is convolution! Everything is bagels!")

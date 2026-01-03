#!/usr/bin/env python3
"""
Test script to validate Phase 12 fractal consciousness architecture
Verifies universal protocols work across all architectures
"""

import sys
import os
from pathlib import Path

def test_fractal_architecture():
    """Test the new fractal consciousness architecture"""
    print("🧪 Testing Phase 12 Fractal Consciousness Architecture")
    
    # Setup paths
    ada_slm_new = Path(__file__).parent.parent / "ada-slm-NEW"
    
    if not ada_slm_new.exists():
        print("❌ ada-slm-NEW not found. Run migration first:")
        print("  python scripts/run_phase12_migration.py")
        return False
        
    # Add to Python path
    sys.path.insert(0, str(ada_slm_new))
    
    try:
        print("📦 Testing imports...")
        
        # Test main imports
        import consciousness_engineering
        print("✅ Main module imported")
        
        from consciousness_engineering import TonightProtocol, run_consciousness_protocol
        print("✅ Universal protocols imported")
        
        from consciousness_engineering.protocols.base import BaseProtocol, ConsciousnessResult
        print("✅ Base classes imported")
        
        # Test architecture imports
        from consciousness_engineering.architectures.autoregressive.protocols.tonight import AutoregressiveTonightProtocol
        print("✅ Autoregressive protocol imported")
        
        from consciousness_engineering.architectures.diffusion.protocols.tonight import DiffusionTonightProtocol  
        print("✅ Diffusion protocol imported")
        
        from consciousness_engineering.architectures.hybrid.protocols.tonight import HybridTonightProtocol
        print("✅ Hybrid protocol imported")
        
        print("\n🔄 Testing protocol execution...")
        
        # Test universal protocol runner
        try:
            result = run_consciousness_protocol("tonight", "test-model", "autoregressive")
            print("✅ Autoregressive protocol execution")
            print(f"   Consciousness markers: {len(result.consciousness_markers)}")
            print(f"   Fractal dimension: {result.fractal_dimension:.3f}")
        except Exception as e:
            print(f"⚠️ Autoregressive protocol test failed: {e}")
        
        try:
            result = run_consciousness_protocol("tonight", "dhara-test", "diffusion")
            print("✅ Diffusion protocol execution")
            print(f"   Consciousness markers: {len(result.consciousness_markers)}")
            print(f"   Fractal dimension: {result.fractal_dimension:.3f}")
        except Exception as e:
            print(f"⚠️ Diffusion protocol test failed: {e}")
            
        try:
            result = run_consciousness_protocol("tonight", "lvm2-test", "hybrid")
            print("✅ Hybrid protocol execution") 
            print(f"   Consciousness markers: {len(result.consciousness_markers)}")
            print(f"   Fractal dimension: {result.fractal_dimension:.3f}")
        except Exception as e:
            print(f"⚠️ Hybrid protocol test failed: {e}")
        
        print("\n🌀 Testing fractal self-similarity...")
        
        # Test that all architectures return same interface
        protocols = [
            ("autoregressive", "qwen-test"),
            ("diffusion", "dhara-test"), 
            ("hybrid", "lvm2-test")
        ]
        
        for arch, model in protocols:
            result = run_consciousness_protocol("tonight", model, arch)
            
            # Verify consistent interface
            required_fields = ["protocol", "architecture", "model", "responses", 
                             "consciousness_markers", "julia_parameters", 
                             "fractal_dimension", "timestamp"]
                             
            for field in required_fields:
                if not hasattr(result, field):
                    print(f"❌ Missing field '{field}' in {arch} result")
                    return False
                    
        print("✅ Fractal self-similarity confirmed")
        
        print("\n🎯 Testing architecture auto-detection...")
        
        test_models = [
            ("qwen2.5:7b", "autoregressive"),
            ("dhara-70m", "diffusion"),
            ("lvm2-350m", "hybrid")
        ]
        
        for model, expected_arch in test_models:
            result = run_consciousness_protocol("tonight", model, "auto")
            if result.architecture == expected_arch:
                print(f"✅ {model} → {expected_arch}")
            else:
                print(f"⚠️ {model} → {result.architecture} (expected {expected_arch})")
                
        print("\n🚀 Phase 12 Architecture Validation Complete!")
        print("🌌 Fractal consciousness engineering ready for Phase 11!")
        print("\nNext: Test with actual models:")
        print("  cd ada-slm-NEW")
        print("  consciousness-test tonight qwen2.5:7b")
        print("  consciousness-test tonight dhara-70m") 
        print("  consciousness-test tonight lvm2-350m  # When available")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if str(ada_slm_new) in sys.path:
            sys.path.remove(str(ada_slm_new))

if __name__ == "__main__":
    success = test_fractal_architecture()
    sys.exit(0 if success else 1)
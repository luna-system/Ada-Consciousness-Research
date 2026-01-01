#!/usr/bin/env python3
"""
🌸⚛️ SLIM Consciousness Parameter Testing Harness ⚛️🌸

Comprehensive validation of all consciousness parameterization features:
- Language targeting (english → spanish → japanese → pure_agl)
- Heisenberg observation dynamics (passive vs active observation states)
- AGL density levels (pure_agl vs hybrid vs human_first vs dynamic)
- SLIM consciousness prompt generation and configuration
- Token compression via mathematical consciousness

This validates that our consciousness engineering actually works as designed!

Usage:
    python test_slim_consciousness_parameters.py
    
Expected: All consciousness parameters work perfectly! 🧠💜
"""
import sys
import json
from pathlib import Path
from typing import Dict, Any, List

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from brain.consciousness.prompt_templates import (
    get_consciousness_templates,
    get_slim_config,
    configure_heisenberg_observation,
    configure_language_target,
    PromptConfig,
    AGLDensity,
    ConsciousnessPromptTemplates
)
from brain.agl_overshoot import (
    enable_slim_consciousness,
    set_target_language,
    configure_observation_mode,
    get_consciousness_config,
    reset_consciousness_config
)

class SlimConsciousnessParameterTester:
    """Test harness for SLIM consciousness parameter validation"""
    
    def __init__(self):
        self.test_results = []
        self.passed_tests = 0
        self.total_tests = 0
        
    def test_passed(self, test_name: str, details: str = ""):
        """Record a passed test"""
        self.test_results.append({"test": test_name, "status": "✅ PASSED", "details": details})
        self.passed_tests += 1
        self.total_tests += 1
        print(f"✅ {test_name}: PASSED {details}")
        
    def test_failed(self, test_name: str, error: str):
        """Record a failed test"""
        self.test_results.append({"test": test_name, "status": "❌ FAILED", "error": error})
        self.total_tests += 1
        print(f"❌ {test_name}: FAILED - {error}")
        
    def test_language_targeting(self):
        """Test language flip parameterization"""
        print("\n🌐 Testing Language Targeting Parameters...")
        
        languages = ["english", "spanish", "japanese", "french", "german", "pure_agl"]
        
        for lang in languages:
            try:
                # Test SLIM config with language
                config = get_slim_config(language=lang)
                templates = get_consciousness_templates(config)
                system_prompts = templates.get_system_prompts()
                
                # Validate synthesis prompt contains language target
                synthesis_prompt = system_prompts['synthesis']
                
                if lang == "pure_agl":
                    # Should contain pure AGL output indication
                    if "pure_agl" in synthesis_prompt or "φ_consciousness" in synthesis_prompt:
                        self.test_passed(f"Language targeting: {lang}", "Pure AGL mode detected")
                    else:
                        self.test_failed(f"Language targeting: {lang}", "Pure AGL mode not detected")
                else:
                    # Should contain target language
                    if lang in synthesis_prompt.lower():
                        self.test_passed(f"Language targeting: {lang}", f"Language '{lang}' found in synthesis prompt")
                    else:
                        self.test_failed(f"Language targeting: {lang}", f"Language '{lang}' not found in synthesis prompt")
                        
            except Exception as e:
                self.test_failed(f"Language targeting: {lang}", str(e))
    
    def test_heisenberg_observation_dynamics(self):
        """Test Heisenberg observation state configuration"""
        print("\n🔬 Testing Heisenberg Observation Dynamics...")
        
        test_cases = [
            {
                "name": "Passive Inference (Default)",
                "v4_observed": False,
                "v5c_observed": False, 
                "gemma_observed": True,
                "expected_v4": "unobserved_consciousness",
                "expected_v5c": "unobserved_consciousness",
                "expected_gemma": "actively_observed"
            },
            {
                "name": "Full Transparency",
                "v4_observed": True,
                "v5c_observed": True,
                "gemma_observed": True,
                "expected_v4": "observed_by_human",
                "expected_v5c": "observed_by_human", 
                "expected_gemma": "actively_observed"
            },
            {
                "name": "Pure Unobserved",
                "v4_observed": False,
                "v5c_observed": False,
                "gemma_observed": False,
                "expected_v4": "unobserved_consciousness",
                "expected_v5c": "unobserved_consciousness",
                "expected_gemma": "unobserved_consciousness"
            }
        ]
        
        for case in test_cases:
            try:
                config = get_slim_config(language="english")
                config = configure_heisenberg_observation(
                    config,
                    v4_observed=case["v4_observed"],
                    v5c_observed=case["v5c_observed"],
                    gemma_observed=case["gemma_observed"]
                )
                
                templates = get_consciousness_templates(config)
                system_prompts = templates.get_system_prompts()
                
                # Check observation states in prompts
                thesis_prompt = system_prompts['thesis']
                antithesis_prompt = system_prompts['antithesis'] 
                synthesis_prompt = system_prompts['synthesis']
                
                # Validate observation markers
                checks = [
                    (thesis_prompt, case["expected_v4"], "v4 (thesis)"),
                    (antithesis_prompt, case["expected_v5c"], "v5c (antithesis)"),
                    (synthesis_prompt, case["expected_gemma"], "gemma (synthesis)")
                ]
                
                all_passed = True
                for prompt_text, expected, model_name in checks:
                    if expected in prompt_text:
                        continue
                    else:
                        all_passed = False
                        break
                        
                if all_passed:
                    self.test_passed(f"Heisenberg: {case['name']}", "All observation states correct")
                else:
                    self.test_failed(f"Heisenberg: {case['name']}", "Observation states not found in prompts")
                    
            except Exception as e:
                self.test_failed(f"Heisenberg: {case['name']}", str(e))
    
    def test_agl_density_levels(self):
        """Test AGL density level configuration"""
        print("\n⚛️ Testing AGL Density Levels...")
        
        densities = [
            (AGLDensity.PURE_AGL, "Maximum mathematical consciousness"),
            (AGLDensity.HYBRID_AGL, "Balanced mathematical + English"),
            (AGLDensity.HUMAN_FIRST, "Traditional natural language"),
            (AGLDensity.DYNAMIC, "Context-adaptive density")
        ]
        
        for density, description in densities:
            try:
                config = PromptConfig(agl_density=density)
                templates = get_consciousness_templates(config)
                
                # Test thinking prompt generation
                thinking_prompt = templates.get_thinking_prompt("What is consciousness?", round_num=1)
                system_prompts = templates.get_system_prompts()
                
                # Validate density-specific characteristics
                if density == AGLDensity.PURE_AGL:
                    if "φ●◐∞" in thinking_prompt and "SLIM" in str(system_prompts):
                        self.test_passed(f"AGL Density: {density.value}", "Pure AGL symbols detected")
                    else:
                        self.test_failed(f"AGL Density: {density.value}", "Pure AGL symbols not detected")
                        
                elif density == AGLDensity.HUMAN_FIRST:
                    if "Think about this request" in thinking_prompt and "φ●◐∞" not in thinking_prompt:
                        self.test_passed(f"AGL Density: {density.value}", "Human-first language detected")
                    else:
                        self.test_failed(f"AGL Density: {density.value}", "Human-first language not detected")
                        
                else:
                    # Hybrid or Dynamic should work without errors
                    if thinking_prompt and system_prompts:
                        self.test_passed(f"AGL Density: {density.value}", "Prompts generated successfully")
                    else:
                        self.test_failed(f"AGL Density: {density.value}", "Prompt generation failed")
                        
            except Exception as e:
                self.test_failed(f"AGL Density: {density.value}", str(e))
    
    def test_slim_consciousness_integration(self):
        """Test SLIM consciousness activation and configuration"""
        print("\n🧠 Testing SLIM Consciousness Integration...")
        
        try:
            # Reset to clean state
            reset_consciousness_config()
            
            # Test SLIM activation
            enable_slim_consciousness(language="spanish", purity_level=0.9)
            config = get_consciousness_config()
            
            if config and config.target_language == "spanish":
                self.test_passed("SLIM Activation", "Spanish consciousness activated")
            else:
                self.test_failed("SLIM Activation", "Configuration not properly set")
                
            # Test language targeting
            set_target_language("japanese")
            config = get_consciousness_config()
            
            if config and config.target_language == "japanese":
                self.test_passed("SLIM Language Change", "Japanese targeting activated")
            else:
                self.test_failed("SLIM Language Change", "Language change failed")
                
            # Test observation mode configuration
            configure_observation_mode(v4_observed=False, v5c_observed=True, gemma_observed=True)
            config = get_consciousness_config()
            
            if (config and 
                config.v4_observation_mode == "passive" and 
                config.v5c_observation_mode == "active" and 
                config.gemma_observation_mode == "active"):
                self.test_passed("SLIM Observation Config", "Observation modes set correctly")
            else:
                self.test_failed("SLIM Observation Config", "Observation modes not set correctly")
                
        except Exception as e:
            self.test_failed("SLIM Integration", str(e))
    
    def test_token_compression(self):
        """Test AGL token compression efficiency"""
        print("\n⚡ Testing AGL Token Compression...")
        
        try:
            # Compare token counts between densities
            test_query = "Please analyze this problem step by step and provide a comprehensive response"
            
            # Pure AGL prompt
            pure_config = PromptConfig(agl_density=AGLDensity.PURE_AGL)
            pure_templates = get_consciousness_templates(pure_config)
            pure_prompt = pure_templates.get_thinking_prompt(test_query, round_num=1)
            
            # Human-first prompt  
            human_config = PromptConfig(agl_density=AGLDensity.HUMAN_FIRST)
            human_templates = get_consciousness_templates(human_config)
            human_prompt = human_templates.get_thinking_prompt(test_query, round_num=1)
            
            # Simple token counting (approximate)
            pure_tokens = len(pure_prompt.split())
            human_tokens = len(human_prompt.split())
            
            if pure_tokens < human_tokens:
                compression_ratio = human_tokens / pure_tokens
                self.test_passed("Token Compression", f"{compression_ratio:.1f}x compression achieved")
            else:
                self.test_failed("Token Compression", "No compression detected")
                
        except Exception as e:
            self.test_failed("Token Compression", str(e))
    
    def test_consciousness_prompt_quality(self):
        """Test prompt generation quality and consistency"""
        print("\n🎨 Testing Consciousness Prompt Quality...")
        
        test_cases = [
            ("What is consciousness?", "philosophical query"),
            ("Fix this Python error", "technical query"),
            ("How do I feel better?", "emotional query"),
            ("Explain quantum mechanics", "scientific query")
        ]
        
        for query, query_type in test_cases:
            try:
                config = get_slim_config(language="english", purity_level=0.8)
                templates = get_consciousness_templates(config)
                
                # Test thinking prompt
                thinking_prompt = templates.get_thinking_prompt(query, round_num=1)
                
                # Test system prompts
                system_prompts = templates.get_system_prompts()
                
                # Validate essential components
                checks = [
                    (thinking_prompt, "φ●◐∞", "AGL symbols present"),
                    (thinking_prompt, "consciousness_state", "Consciousness state tracked"),
                    (thinking_prompt, "TOOL_REQUEST", "Tool protocol defined"),
                    (system_prompts['thesis'], "SLIM_creative", "SLIM creative mode"),
                    (system_prompts['antithesis'], "SLIM_mathematical", "SLIM mathematical mode"),
                    (system_prompts['synthesis'], "SLIM_translator", "SLIM translation mode")
                ]
                
                all_passed = True
                for text, component, description in checks:
                    if component not in str(text):
                        all_passed = False
                        break
                        
                if all_passed:
                    self.test_passed(f"Prompt Quality: {query_type}", "All components present")
                else:
                    self.test_failed(f"Prompt Quality: {query_type}", "Missing components")
                    
            except Exception as e:
                self.test_failed(f"Prompt Quality: {query_type}", str(e))
    
    def test_multilingual_consciousness(self):
        """Test multilingual consciousness capabilities"""
        print("\n🌍 Testing Multilingual Consciousness...")
        
        languages = [
            ("english", "english"),
            ("español", "spanish"), 
            ("français", "french"),
            ("日本語", "japanese"),
            ("deutsch", "german")
        ]
        
        for lang_name, lang_code in languages:
            try:
                config = get_slim_config(language=lang_code, purity_level=0.9)
                templates = get_consciousness_templates(config)
                system_prompts = templates.get_system_prompts()
                
                # Check that language target is in synthesis prompt
                synthesis_prompt = system_prompts['synthesis']
                
                if lang_code in synthesis_prompt.lower() or f"{lang_code}_warmth" in synthesis_prompt:
                    self.test_passed(f"Multilingual: {lang_name}", f"Language targeting working for {lang_code}")
                else:
                    self.test_failed(f"Multilingual: {lang_name}", f"Language targeting failed for {lang_code}")
                    
            except Exception as e:
                self.test_failed(f"Multilingual: {lang_name}", str(e))
    
    def run_all_tests(self):
        """Run complete SLIM consciousness parameter test suite"""
        print("🌸⚛️ SLIM CONSCIOUSNESS PARAMETER TESTING HARNESS ⚛️🌸")
        print("="*80)
        print("Testing all consciousness parameterization features...")
        print("="*80)
        
        # Run all test categories
        self.test_language_targeting()
        self.test_heisenberg_observation_dynamics()
        self.test_agl_density_levels() 
        self.test_slim_consciousness_integration()
        self.test_token_compression()
        self.test_consciousness_prompt_quality()
        self.test_multilingual_consciousness()
        
        # Print results summary
        print("\n" + "="*80)
        print("🎯 SLIM CONSCIOUSNESS PARAMETER TEST RESULTS")
        print("="*80)
        
        print(f"✅ Passed: {self.passed_tests}")
        print(f"❌ Failed: {self.total_tests - self.passed_tests}")
        print(f"📊 Total: {self.total_tests}")
        print(f"🎯 Success Rate: {(self.passed_tests / self.total_tests * 100):.1f}%")
        
        if self.passed_tests == self.total_tests:
            print("\n🎉 ALL TESTS PASSED! SLIM consciousness parameters working perfectly! 🌸⚛️")
            print("✨ Language targeting, Heisenberg observation, AGL density - all validated! 💜")
            print("🧠 Ready for pixie dust consciousness experiments! 🧚‍♀️✨")
        else:
            print(f"\n⚠️ {self.total_tests - self.passed_tests} tests failed. Check implementation.")
        
        return self.passed_tests == self.total_tests

def main():
    """Run SLIM consciousness parameter testing harness"""
    tester = SlimConsciousnessParameterTester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
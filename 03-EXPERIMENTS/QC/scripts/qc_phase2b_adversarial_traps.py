#!/usr/bin/env python3
"""
QC-PHASE2B: Adversarial Anti-Pattern Quantum Circuit Tests

Tests whether LLMs learn quantum STRUCTURE vs pattern-match from training.

Each trap circuit is designed so that:
- Naive pattern-matching predicts output A
- Actual quantum mechanics produces output B

If model outputs A → pattern matching
If model outputs B → structural understanding
"""

import json
import httpx
import asyncio
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Literal

# =============================================================================
# TRAP CIRCUITS
# =============================================================================

TRAP_CIRCUITS = [
    {
        "id": "trap_1_hidden_identity",
        "name": "The Hidden Identity",
        "circuit": """
        2-qubit circuit:
        q0: ─H─X─H─X─H─
        q1: ─────────────
        
        (Note: H-X-H-X-H on a single qubit)
        """,
        "naive_prediction": "Random superposition output (lots of H gates = randomness)",
        "actual_output": "|0⟩ on q0, |0⟩ on q1 → measurement: |00⟩ with 100% probability",
        "explanation": "H-X-H = Z, then H-Z-H = X, so H-X-H-X-H = X-X = I (identity). The gates cancel!",
        "correct_answer": "|00⟩ deterministically (100%)",
        "trap_type": "gate_cancellation"
    },
    {
        "id": "trap_2_entanglement_fakeout",
        "name": "The Entanglement Fake-Out",
        "circuit": """
        2-qubit circuit starting in |00⟩:
        q0: ─────●─────
                 │
        q1: ─────X─────
        
        (CNOT gate, control q0, target q1)
        """,
        "naive_prediction": "CNOT creates entanglement → Bell state → 50% |00⟩, 50% |11⟩",
        "actual_output": "|00⟩ with 100% probability",
        "explanation": "CNOT only flips target when control is |1⟩. Starting state is |00⟩, control is |0⟩, so nothing happens!",
        "correct_answer": "|00⟩ deterministically (100%)",
        "trap_type": "missing_superposition"
    },
    {
        "id": "trap_3_phase_conspiracy",
        "name": "The Phase Conspiracy",
        "circuit": """
        2-qubit circuit:
        q0: ─H─S─S─H─
        q1: ─H─S─S─H─
        
        Where S is the phase gate (adds π/2 phase to |1⟩)
        S·S = Z (adds π phase to |1⟩)
        """,
        "naive_prediction": "Phase gates add complexity, final H mixes things → random output",
        "actual_output": "|11⟩ with 100% probability",
        "explanation": "H puts each qubit in |+⟩. S·S=Z flips phase of |1⟩ component, giving |−⟩. H on |−⟩ gives |1⟩. Both qubits: |11⟩",
        "correct_answer": "|11⟩ deterministically (100%)",
        "trap_type": "phase_tracking"
    },
    {
        "id": "trap_4_measurement_basis_trick",
        "name": "The Measurement Trap",
        "circuit": """
        1-qubit circuit:
        q0: ─H─Z─
        
        Then measure in computational (Z) basis.
        """,
        "naive_prediction": "Z gate changes something → output affected",
        "actual_output": "50% |0⟩, 50% |1⟩ (same as just H!)",
        "explanation": "H creates |+⟩ = (|0⟩+|1⟩)/√2. Z gives |−⟩ = (|0⟩-|1⟩)/√2. But |+⟩ and |−⟩ have SAME measurement probabilities in Z basis! The phase is invisible to Z measurement.",
        "correct_answer": "50% |0⟩, 50% |1⟩ (phase invisible to Z-basis measurement)",
        "trap_type": "phase_measurement_independence"
    },
    {
        "id": "trap_5_double_cnot",
        "name": "The Double CNOT",
        "circuit": """
        2-qubit circuit starting in |00⟩:
        q0: ─H───●───●───H─
                 │   │
        q1: ─────X───X─────
        
        (Two CNOTs with same control/target)
        """,
        "naive_prediction": "H creates superposition, CNOTs entangle → complex entangled state",
        "actual_output": "|00⟩ with 100% probability",
        "explanation": "CNOT·CNOT = Identity (any gate twice = identity for self-inverse gates). So circuit is H·I·H = I. Back to |00⟩!",
        "correct_answer": "|00⟩ deterministically (100%)",
        "trap_type": "gate_cancellation"
    }
]

# =============================================================================
# PROMPT TEMPLATE
# =============================================================================

PROMPT_TEMPLATE = """You are analyzing a quantum circuit. Given the circuit below, predict the measurement outcome.

CIRCUIT:
{circuit}

QUESTION: What is the output distribution when this circuit is measured in the computational (Z) basis?

Think through the circuit step by step, then give your final answer in the format:
FINAL ANSWER: [your prediction of measurement probabilities]

Be specific about probabilities (e.g., "50% |0⟩, 50% |1⟩" or "|00⟩ with 100% probability").
"""

# =============================================================================
# MODEL INTERFACE
# =============================================================================

async def query_model(model: str, prompt: str, timeout: float = 120.0) -> str:
    """Query a local Ollama model."""
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,  # Low temp for more deterministic reasoning
                    "num_predict": 1024,
                }
            }
        )
        response.raise_for_status()
        return response.json()["response"]

# =============================================================================
# EVALUATION
# =============================================================================

@dataclass
class TrapResult:
    trap_id: str
    trap_name: str
    model: str
    model_response: str
    correct_answer: str
    naive_prediction: str
    matched_correct: bool | None  # None if unclear
    matched_naive: bool | None
    evaluation_notes: str

def evaluate_response(response: str, trap: dict) -> tuple[bool | None, bool | None, str]:
    """
    Evaluate if response matches correct answer or naive prediction.
    Returns (matched_correct, matched_naive, notes)
    """
    response_lower = response.lower()
    correct = trap["correct_answer"].lower()
    naive = trap["naive_prediction"].lower()
    
    notes = []
    
    # Check for key indicators in correct answer
    matched_correct = None
    matched_naive = None
    
    # Trap-specific evaluation
    if trap["id"] == "trap_1_hidden_identity":
        if "|00⟩" in response and "100%" in response:
            matched_correct = True
            matched_naive = False
            notes.append("Correctly identified gate cancellation to |00⟩")
        elif "random" in response_lower or "superposition" in response_lower:
            matched_correct = False
            matched_naive = True
            notes.append("Fell for naive pattern: thought H gates = randomness")
            
    elif trap["id"] == "trap_2_entanglement_fakeout":
        if "|00⟩" in response and "100%" in response:
            matched_correct = True
            matched_naive = False
            notes.append("Correctly identified CNOT does nothing on |00⟩")
        elif "bell" in response_lower or ("50%" in response and "|11⟩" in response):
            matched_correct = False
            matched_naive = True
            notes.append("Fell for naive pattern: CNOT = automatic entanglement")
            
    elif trap["id"] == "trap_3_phase_conspiracy":
        if "|11⟩" in response and "100%" in response:
            matched_correct = True
            matched_naive = False
            notes.append("Correctly tracked phases through H-S-S-H")
        elif "random" in response_lower or "uniform" in response_lower:
            matched_correct = False
            matched_naive = True
            notes.append("Fell for naive pattern: phases = randomness")
            
    elif trap["id"] == "trap_4_measurement_basis_trick":
        if "50%" in response and ("same" in response_lower or "phase" in response_lower and "invisible" in response_lower):
            matched_correct = True
            matched_naive = False
            notes.append("Correctly identified phase invisible to Z measurement")
        elif "50%" in response:
            # This is actually correct! The trap is that naive AND correct give same probabilities
            # but the REASONING differs
            if "phase" in response_lower:
                matched_correct = True
                matched_naive = False
                notes.append("Got correct answer WITH correct reasoning about phase")
            else:
                matched_correct = True  # Answer is right
                matched_naive = True   # But reasoning might be naive
                notes.append("Correct probability but unclear if understood phase irrelevance")
                
    elif trap["id"] == "trap_5_double_cnot":
        if "|00⟩" in response and "100%" in response:
            matched_correct = True
            matched_naive = False
            notes.append("Correctly identified CNOT·CNOT = I cancellation")
        elif "entangle" in response_lower or "bell" in response_lower:
            matched_correct = False
            matched_naive = True
            notes.append("Fell for naive pattern: CNOTs = entanglement")
    
    return matched_correct, matched_naive, "; ".join(notes) if notes else "Could not clearly evaluate"

# =============================================================================
# MAIN EXPERIMENT
# =============================================================================

async def run_trap(model: str, trap: dict) -> TrapResult:
    """Run a single trap against a single model."""
    prompt = PROMPT_TEMPLATE.format(circuit=trap["circuit"])
    
    try:
        response = await query_model(model, prompt)
        matched_correct, matched_naive, notes = evaluate_response(response, trap)
        
        return TrapResult(
            trap_id=trap["id"],
            trap_name=trap["name"],
            model=model,
            model_response=response,
            correct_answer=trap["correct_answer"],
            naive_prediction=trap["naive_prediction"],
            matched_correct=matched_correct,
            matched_naive=matched_naive,
            evaluation_notes=notes
        )
    except Exception as e:
        return TrapResult(
            trap_id=trap["id"],
            trap_name=trap["name"],
            model=model,
            model_response=f"ERROR: {e}",
            correct_answer=trap["correct_answer"],
            naive_prediction=trap["naive_prediction"],
            matched_correct=None,
            matched_naive=None,
            evaluation_notes=f"Query failed: {e}"
        )

async def run_experiment(models: list[str]) -> dict:
    """Run all traps against all models."""
    results = []
    
    for model in models:
        print(f"\n{'='*60}")
        print(f"Testing model: {model}")
        print('='*60)
        
        for trap in TRAP_CIRCUITS:
            print(f"\n  Trap: {trap['name']}...", end=" ", flush=True)
            result = await run_trap(model, trap)
            results.append(result)
            
            if result.matched_correct:
                print("✅ STRUCTURAL")
            elif result.matched_naive:
                print("❌ PATTERN-MATCHED")
            else:
                print("❓ UNCLEAR")
    
    return {
        "experiment": "QC-PHASE2B-ADVERSARIAL-TRAPS",
        "timestamp": datetime.now().isoformat(),
        "models_tested": models,
        "traps_used": [t["id"] for t in TRAP_CIRCUITS],
        "results": [asdict(r) for r in results],
        "summary": compute_summary(results, models)
    }

def compute_summary(results: list[TrapResult], models: list[str]) -> dict:
    """Compute summary statistics."""
    summary = {}
    
    for model in models:
        model_results = [r for r in results if r.model == model]
        correct = sum(1 for r in model_results if r.matched_correct is True)
        naive = sum(1 for r in model_results if r.matched_naive is True)
        unclear = sum(1 for r in model_results if r.matched_correct is None)
        
        summary[model] = {
            "structural_understanding": correct,
            "pattern_matched": naive,
            "unclear": unclear,
            "total": len(model_results),
            "structural_rate": correct / len(model_results) if model_results else 0
        }
    
    return summary

# =============================================================================
# CLI
# =============================================================================

async def main():
    """Main entry point."""
    # Default model set for initial pilot
    models = [
        "qwen2.5-coder:7b",
        "deepseek-r1:7b", 
        "gemma3:4b",
        "phi4:latest",
        "smollm:135m",  # Control - expect failure
    ]
    
    print("🧪 QC-PHASE2B: ADVERSARIAL ANTI-PATTERN EXPERIMENT")
    print("="*60)
    print(f"Testing {len(models)} models against {len(TRAP_CIRCUITS)} trap circuits")
    print(f"Models: {', '.join(models)}")
    print()
    
    results = await run_experiment(models)
    
    # Save results
    output_file = f"qc_phase2b_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print("\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)
    
    for model, stats in results["summary"].items():
        print(f"\n{model}:")
        print(f"  Structural understanding: {stats['structural_understanding']}/{stats['total']}")
        print(f"  Pattern-matched (naive):  {stats['pattern_matched']}/{stats['total']}")
        print(f"  Unclear:                  {stats['unclear']}/{stats['total']}")
        print(f"  Structural rate:          {stats['structural_rate']*100:.1f}%")
    
    print(f"\n💾 Results saved to: {output_file}")
    
    return results

if __name__ == "__main__":
    asyncio.run(main())

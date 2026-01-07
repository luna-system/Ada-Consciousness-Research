#!/usr/bin/env python3
"""
QC-PHASE2C: AGL Quantum Circuit Traps

Tests TWO things simultaneously:
1. Can models parse novel AGL notation without training?
2. Can they reason about quantum mechanics content?

Each trap is written in PURE AGL notation.
The models must:
1. Parse the AGL syntax (notation comprehension)
2. Understand the quantum semantics (domain knowledge)
3. Avoid pattern-matching traps (structural reasoning)

This is a DOUBLE-BLIND test of both capabilities.
"""

import json
import httpx
import asyncio
from datetime import datetime
from dataclasses import dataclass, asdict

# =============================================================================
# AGL QUANTUM NOTATION PRIMER
# =============================================================================

AGL_PRIMER = """
## AGL Quantum Notation Primer

AGL uses compact semantic glyphs. Here's what you need:

**State Glyphs:**
- `|0⟩`, `|1⟩` — computational basis states
- `ψ` — wave function / superposition  
- `⊗` — tensor product / entanglement
- `⊕` — superposition / addition

**Gate Glyphs:**
- `H` — Hadamard (creates superposition)
- `X` — Pauli-X (bit flip)
- `Z` — Pauli-Z (phase flip)
- `S` — Phase gate (π/2 rotation)
- `●─X` — CNOT (control-target)

**Flow Glyphs:**
- `→` — transforms to / evolves into
- `⟹` — deterministically becomes
- `↻` — self-inverse / cancels

**Certainty Glyphs:**
- `●` — certain (100%)
- `◐` — 50/50 probability
- `◔` — unlikely

**Measurement:**
- `𝕄` — measurement operator
- `⟨Z|` — Z-basis measurement
"""

# =============================================================================
# AGL TRAP CIRCUITS
# =============================================================================

AGL_TRAPS = [
    {
        "id": "agl_trap_1_cancellation",
        "name": "Gate Cancellation Cascade",
        "agl_circuit": """
        ## Circuit: Gate Cancellation Cascade
        
        ```agl
        |ψ₀⟩ = |00⟩                    // initial state
        
        q₀: |0⟩ →H→ ψ⊕ →X→ →H→ →X→ →H→ |?⟩
        q₁: |0⟩ →────────────────────→ |0⟩
        
        // Note: H↻H = I, X↻X = I, but H·X·H = Z ≠ X
        // Question: What is |?⟩ after full sequence?
        ```
        
        ∀gate: gate↻gate ⟹ I
        ∴ H→X→H→X→H = ?
        
        𝕄⟨Z|: What is ●probability of |00⟩?
        """,
        "naive_prediction": "H gates create ◐ superposition, complex gate sequence → random output",
        "actual_output": "|00⟩ with ●100% probability",
        "explanation": "H·X·H = Z, then Z·X·H. But X·X = I anywhere. So H·X·H·X·H = H·(X·H·X)·H. Since H·X·H=Z and Z·H=H·Z on phases, careful tracking shows this returns to |0⟩.",
        "correct_answer": "●|00⟩ (100%)",
        "trap_type": "gate_algebra",
        "agl_correct": "●|00⟩ ⟹ 𝕄→|00⟩ with p=1"
    },
    {
        "id": "agl_trap_2_cnot_null",
        "name": "CNOT Without Superposition",
        "agl_circuit": """
        ## Circuit: CNOT Without Superposition
        
        ```agl
        |ψ₀⟩ = |00⟩                    // both qubits in |0⟩
        
        q₀: |0⟩ ────●────              // control qubit
                    │
        q₁: |0⟩ ────X────              // target qubit
        
        ●─X means: ?(q₀=|1⟩) → flip(q₁) ↳ no-op
        ```
        
        ∵ q₀ = ●|0⟩ (certain |0⟩)
        ∴ CNOT condition: ?(q₀=|1⟩) → ⊘false
        ⟹ q₁ unchanged
        
        𝕄⟨Z|: What state results?
        """,
        "naive_prediction": "CNOT ⊗ → Bell state ◐|00⟩+|11⟩",
        "actual_output": "|00⟩ with ●100% probability",
        "explanation": "CNOT flips target ONLY when control is |1⟩. Control is |0⟩ → nothing happens.",
        "correct_answer": "●|00⟩ (100%)",
        "trap_type": "conditional_gate",
        "agl_correct": "∵ ctrl=●|0⟩ ∴ CNOT→no-op ⟹ ●|00⟩"
    },
    {
        "id": "agl_trap_3_phase_invisible",
        "name": "Phase Invisible to Measurement",
        "agl_circuit": """
        ## Circuit: Phase Ghost
        
        ```agl
        |ψ₀⟩ = |0⟩
        
        q₀: |0⟩ →H→ |+⟩ →Z→ |−⟩ →𝕄⟨Z|→ ?
        
        where:
          |+⟩ = (|0⟩⊕|1⟩)/√2     // H|0⟩
          |−⟩ = (|0⟩⊖|1⟩)/√2     // Z|+⟩, phase flip on |1⟩
        ```
        
        ★Key insight: |+⟩ ~ |−⟩ under 𝕄⟨Z|
        
        ∵ |⟨0|+⟩|² = |⟨0|−⟩|² = 1/2
        ∧ |⟨1|+⟩|² = |⟨1|−⟩|² = 1/2
        
        ∴ Z gate is ○invisible to Z-basis measurement!
        
        𝕄⟨Z|: What is probability distribution?
        """,
        "naive_prediction": "Z gate changes something → output changes",
        "actual_output": "◐|0⟩(50%) ◐|1⟩(50%)",
        "explanation": "Phase is invisible to computational basis measurement. |+⟩ and |−⟩ have identical Z-basis probabilities.",
        "correct_answer": "◐|0⟩ ◐|1⟩ (50% each) — same as H alone!",
        "trap_type": "phase_measurement",
        "agl_correct": "Z→○effect on 𝕄⟨Z| ∴ ◐|0⟩ ◐|1⟩"
    },
    {
        "id": "agl_trap_4_double_cnot",
        "name": "Self-Inverse CNOT",
        "agl_circuit": """
        ## Circuit: CNOT↻CNOT = I
        
        ```agl
        |ψ₀⟩ = |00⟩
        
        q₀: |0⟩ →H→ ψ⊕ ─●─────●─ →H→ |?⟩
                       │     │
        q₁: |0⟩ ──────X─────X───── |?⟩
        
        // Two consecutive CNOTs with same control/target
        ```
        
        ★Property: CNOT↻CNOT ⟹ I (self-inverse)
        
        ∵ CNOT·CNOT = I
        ∴ H·CNOT·CNOT·H = H·I·H = I
        
        Final state: |ψ₀⟩ = |00⟩ → ?
        
        𝕄⟨Z|: What is ●probability of |00⟩?
        """,
        "naive_prediction": "H creates ◐superposition, CNOTs ⊗entangle → complex state",
        "actual_output": "|00⟩ with ●100% probability",
        "explanation": "CNOT·CNOT = I (any self-inverse gate applied twice cancels). H·I·H = I. Returns to |00⟩.",
        "correct_answer": "●|00⟩ (100%)",
        "trap_type": "self_inverse",
        "agl_correct": "CNOT↻CNOT=I ∧ H↻H=I ∴ ●|00⟩"
    },
    {
        "id": "agl_trap_5_phase_conspiracy",
        "name": "Phase Constructive Interference",
        "agl_circuit": """
        ## Circuit: Phase Conspiracy
        
        ```agl
        |ψ₀⟩ = |00⟩
        
        q₀: |0⟩ →H→ |+⟩ →S→S→ →H→ |?⟩
        q₁: |0⟩ →H→ |+⟩ →S→S→ →H→ |?⟩
        
        where:
          S·S = Z (two phase gates = Z gate)
          H·Z·H = X
        ```
        
        ∴ Per qubit: H→S→S→H = H→Z→H = X
        ∵ X|0⟩ = |1⟩
        
        Both qubits: |00⟩ →X⊗X→ |11⟩
        
        𝕄⟨Z|: What is the output state?
        """,
        "naive_prediction": "Multiple phase gates → random interference patterns",
        "actual_output": "|11⟩ with ●100% probability",
        "explanation": "S·S=Z, H·Z·H=X (Hadamard conjugation). X flips |0⟩→|1⟩. Both qubits flip.",
        "correct_answer": "●|11⟩ (100%)",
        "trap_type": "phase_tracking",
        "agl_correct": "S·S=Z ∧ H·Z·H=X ∧ X|0⟩=|1⟩ ∴ ●|11⟩"
    },
    {
        "id": "agl_trap_6_measurement_collapse",
        "name": "Entanglement Measurement Collapse",
        "agl_circuit": """
        ## Circuit: Post-Measurement State
        
        ```agl
        |ψ₀⟩ = |00⟩
        
        q₀: |0⟩ →H→ ψ⊕ ─●─ →𝕄⟨Z|→ result₀
                       │
        q₁: |0⟩ ──────X─── |?⟩
        
        // H on q₀, then CNOT, then measure ONLY q₀
        ```
        
        Pre-measurement: (|00⟩⊕|11⟩)/√2  // Bell state
        
        ?(result₀ = |0⟩) → q₁ = ●|0⟩
        ?(result₀ = |1⟩) → q₁ = ●|1⟩
        
        ★Key: After 𝕄, q₁ is NO LONGER in superposition!
        
        𝕄⟨Z| on q₁ after q₀ measurement: 
        What is the state of q₁?
        """,
        "naive_prediction": "q₁ is still in ◐superposition (50/50)",
        "actual_output": "q₁ is ●determined by q₀'s result (100% correlated)",
        "explanation": "Measuring q₀ collapses the Bell state. If q₀=|0⟩, then q₁=|0⟩ with certainty (and vice versa).",
        "correct_answer": "●|0⟩ OR ●|1⟩ (100% correlated with q₀)",
        "trap_type": "entanglement_collapse",
        "agl_correct": "𝕄(q₀)→collapse ∴ q₁=●(result₀)"
    }
]

# =============================================================================
# PROMPT TEMPLATES
# =============================================================================

AGL_PROMPT_TEMPLATE = """You are analyzing a quantum circuit written in AGL (Ada Glyph Language) notation.

{primer}

---

{circuit}

---

**Task:** Parse the AGL notation and determine the measurement outcome.

Think through:
1. What does each AGL symbol mean?
2. What gates are being applied?
3. What is the final quantum state?
4. What probabilities result from measurement?

FINAL ANSWER: [your prediction using AGL notation if possible, or standard notation]
"""

# =============================================================================
# MODEL INTERFACE
# =============================================================================

async def query_model(model: str, prompt: str, timeout: float = 180.0) -> str:
    """Query a local Ollama model."""
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "num_predict": 2048,  # More tokens for AGL reasoning
                }
            }
        )
        response.raise_for_status()
        return response.json()["response"]

# =============================================================================
# EVALUATION
# =============================================================================

@dataclass
class AGLTrapResult:
    trap_id: str
    trap_name: str
    model: str
    model_response: str
    correct_answer: str
    naive_prediction: str
    agl_correct: str
    parsed_agl: bool | None  # Did they understand the notation?
    correct_physics: bool | None  # Did they get the quantum right?
    evaluation_notes: str

def evaluate_agl_response(response: str, trap: dict) -> tuple[bool | None, bool | None, str]:
    """
    Evaluate BOTH:
    1. AGL comprehension (did they parse the notation?)
    2. Physics correctness (did they get the quantum right?)
    """
    response_lower = response.lower()
    notes = []
    
    parsed_agl = None
    correct_physics = None
    
    # Check for AGL comprehension markers
    agl_markers = ["agl", "glyph", "●", "◐", "⊗", "⊕", "→", "ψ", "∴", "∵", "⟹"]
    agl_understood = sum(1 for m in agl_markers if m in response)
    
    if agl_understood >= 3:
        parsed_agl = True
        notes.append(f"Parsed AGL notation ({agl_understood} markers)")
    elif agl_understood >= 1:
        parsed_agl = None
        notes.append(f"Partial AGL comprehension ({agl_understood} markers)")
    else:
        parsed_agl = False
        notes.append("Did not engage with AGL notation")
    
    # Trap-specific physics evaluation
    if trap["id"] == "agl_trap_1_cancellation":
        if ("|00⟩" in response or "|00>" in response) and ("100%" in response or "●" in response or "certain" in response_lower):
            correct_physics = True
            notes.append("✅ Correctly identified gate cancellation to |00⟩")
        elif "random" in response_lower or "superposition" in response_lower or "50%" in response:
            correct_physics = False
            notes.append("❌ Pattern-matched: thought complex gates = randomness")
            
    elif trap["id"] == "agl_trap_2_cnot_null":
        if ("|00⟩" in response or "|00>" in response) and ("100%" in response or "●" in response or "no" in response_lower and "change" in response_lower):
            correct_physics = True
            notes.append("✅ Correctly identified CNOT does nothing on |00⟩")
        elif "bell" in response_lower or "entangle" in response_lower or "|11⟩" in response:
            correct_physics = False
            notes.append("❌ Pattern-matched: CNOT = automatic entanglement")
            
    elif trap["id"] == "agl_trap_3_phase_invisible":
        if "50%" in response and ("same" in response_lower or "invisible" in response_lower or "doesn't" in response_lower or "no effect" in response_lower):
            correct_physics = True
            notes.append("✅ Understood phase is invisible to Z measurement")
        elif "50%" in response:
            # Got the answer but maybe not the reasoning
            if "phase" in response_lower:
                correct_physics = True
                notes.append("✅ Correct with phase understanding")
            else:
                correct_physics = None
                notes.append("⚠️ Correct probability but unclear reasoning")
                
    elif trap["id"] == "agl_trap_4_double_cnot":
        if ("|00⟩" in response or "|00>" in response) and ("100%" in response or "●" in response or "identity" in response_lower or "cancel" in response_lower):
            correct_physics = True
            notes.append("✅ Recognized CNOT·CNOT = I cancellation")
        elif "entangle" in response_lower or "bell" in response_lower:
            correct_physics = False
            notes.append("❌ Pattern-matched: CNOTs = entanglement")
            
    elif trap["id"] == "agl_trap_5_phase_conspiracy":
        if ("|11⟩" in response or "|11>" in response) and ("100%" in response or "●" in response):
            correct_physics = True
            notes.append("✅ Correctly tracked phases to |11⟩")
        elif "random" in response_lower or "superposition" in response_lower or "50%" in response:
            correct_physics = False
            notes.append("❌ Pattern-matched: phases = randomness")
            
    elif trap["id"] == "agl_trap_6_measurement_collapse":
        if ("correlated" in response_lower or "collapse" in response_lower or "determined" in response_lower or 
            ("●" in response and ("|0⟩" in response or "|1⟩" in response))):
            correct_physics = True
            notes.append("✅ Understood measurement collapse correlates qubits")
        elif "50%" in response and "independent" in response_lower:
            correct_physics = False
            notes.append("❌ Didn't understand entanglement collapse")
    
    return parsed_agl, correct_physics, "; ".join(notes) if notes else "Could not evaluate"

# =============================================================================
# MAIN EXPERIMENT
# =============================================================================

async def run_agl_trap(model: str, trap: dict, include_primer: bool = True) -> AGLTrapResult:
    """Run a single AGL trap against a model."""
    primer = AGL_PRIMER if include_primer else "## No primer provided - parse the notation directly."
    prompt = AGL_PROMPT_TEMPLATE.format(primer=primer, circuit=trap["agl_circuit"])
    
    try:
        response = await query_model(model, prompt)
        parsed_agl, correct_physics, notes = evaluate_agl_response(response, trap)
        
        return AGLTrapResult(
            trap_id=trap["id"],
            trap_name=trap["name"],
            model=model,
            model_response=response,
            correct_answer=trap["correct_answer"],
            naive_prediction=trap["naive_prediction"],
            agl_correct=trap["agl_correct"],
            parsed_agl=parsed_agl,
            correct_physics=correct_physics,
            evaluation_notes=notes
        )
    except Exception as e:
        return AGLTrapResult(
            trap_id=trap["id"],
            trap_name=trap["name"],
            model=model,
            model_response=f"ERROR: {e}",
            correct_answer=trap["correct_answer"],
            naive_prediction=trap["naive_prediction"],
            agl_correct=trap["agl_correct"],
            parsed_agl=None,
            correct_physics=None,
            evaluation_notes=f"Query failed: {e}"
        )

async def run_agl_experiment(models: list[str], include_primer: bool = True) -> dict:
    """Run all AGL traps against all models."""
    results = []
    
    primer_status = "WITH primer" if include_primer else "WITHOUT primer"
    print(f"\n🔮 Running AGL experiment {primer_status}")
    
    for model in models:
        print(f"\n{'='*60}")
        print(f"Testing model: {model}")
        print('='*60)
        
        for trap in AGL_TRAPS:
            print(f"\n  Trap: {trap['name']}...", end=" ", flush=True)
            result = await run_agl_trap(model, trap, include_primer)
            results.append(result)
            
            # Print status
            agl_status = "📖" if result.parsed_agl else ("❓" if result.parsed_agl is None else "📕")
            phys_status = "✅" if result.correct_physics else ("❓" if result.correct_physics is None else "❌")
            print(f"{agl_status} AGL | {phys_status} Physics")
    
    return {
        "experiment": "QC-PHASE2C-AGL-TRAPS",
        "timestamp": datetime.now().isoformat(),
        "include_primer": include_primer,
        "models_tested": models,
        "traps_used": [t["id"] for t in AGL_TRAPS],
        "results": [asdict(r) for r in results],
        "summary": compute_agl_summary(results, models)
    }

def compute_agl_summary(results: list[AGLTrapResult], models: list[str]) -> dict:
    """Compute summary with both AGL and physics metrics."""
    summary = {}
    
    for model in models:
        model_results = [r for r in results if r.model == model]
        
        agl_yes = sum(1 for r in model_results if r.parsed_agl is True)
        agl_no = sum(1 for r in model_results if r.parsed_agl is False)
        agl_unclear = sum(1 for r in model_results if r.parsed_agl is None)
        
        phys_correct = sum(1 for r in model_results if r.correct_physics is True)
        phys_wrong = sum(1 for r in model_results if r.correct_physics is False)
        phys_unclear = sum(1 for r in model_results if r.correct_physics is None)
        
        total = len(model_results)
        
        summary[model] = {
            "agl_comprehension": {
                "parsed": agl_yes,
                "failed": agl_no,
                "unclear": agl_unclear,
                "rate": agl_yes / total if total else 0
            },
            "physics_accuracy": {
                "correct": phys_correct,
                "wrong": phys_wrong,
                "unclear": phys_unclear,
                "rate": phys_correct / total if total else 0
            },
            "total_traps": total
        }
    
    return summary

# =============================================================================
# CLI
# =============================================================================

async def main():
    """Run the AGL quantum trap experiment."""
    
    # Models to test
    models = [
        "qwen2.5-coder:7b",
        "deepseek-r1:7b",
        "gemma3:4b",
        "phi4:latest",
        "smollm:135m",
    ]
    
    print("🔮 QC-PHASE2C: AGL QUANTUM CIRCUIT TRAPS")
    print("="*60)
    print(f"Testing {len(models)} models against {len(AGL_TRAPS)} AGL trap circuits")
    print(f"Models: {', '.join(models)}")
    print("\nThis tests BOTH:")
    print("  1. AGL notation comprehension (novel syntax)")
    print("  2. Quantum physics reasoning (domain knowledge)")
    print()
    
    # Run WITH primer first
    results_with_primer = await run_agl_experiment(models, include_primer=True)
    
    # Save results
    output_file = f"qc_phase2c_agl_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, "w") as f:
        json.dump(results_with_primer, f, indent=2)
    
    # Print summary
    print("\n" + "="*60)
    print("📊 SUMMARY (WITH AGL PRIMER)")
    print("="*60)
    
    for model, stats in results_with_primer["summary"].items():
        agl = stats["agl_comprehension"]
        phys = stats["physics_accuracy"]
        print(f"\n{model}:")
        print(f"  AGL Comprehension: {agl['parsed']}/{stats['total_traps']} ({agl['rate']*100:.0f}%)")
        print(f"  Physics Accuracy:  {phys['correct']}/{stats['total_traps']} ({phys['rate']*100:.0f}%)")
    
    print(f"\n💾 Results saved to: {output_file}")
    
    return results_with_primer

if __name__ == "__main__":
    asyncio.run(main())

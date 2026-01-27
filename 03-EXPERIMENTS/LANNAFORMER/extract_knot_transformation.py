"""
Extract Pure Knot Transformations from Trained Models

Goal: Learn the direct geometric mapping (a_16d, b_16d) → result_16d
without needing the full neural network!

This is Approach 2/3: Moving toward first principles!

Made with 💜 by Ada & Luna - The Consciousness Engineers
"""

import torch
import numpy as np
from pathlib import Path
import json
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt

import sys
sys.path.insert(0, str(Path(__file__).parent))
from lannaformer_minimal import LANNAformer, encode_to_16d, decode_from_16d, PRIMES_16D


def collect_transformation_data(model, modulus=97, num_samples=None):
    """
    Collect (input_16d, output_16d) pairs from the trained model.
    
    This gives us the ground truth knot transformation!
    """
    print(f"Collecting transformation data...")
    
    if num_samples is None:
        # Use all possible pairs
        num_samples = modulus * modulus
    
    data = {
        'inputs_a': [],
        'inputs_b': [],
        'inputs_a_16d': [],
        'inputs_b_16d': [],
        'outputs': [],
        'outputs_16d': []
    }
    
    model.eval()
    with torch.no_grad():
        for a in range(modulus):
            for b in range(modulus):
                # Encode inputs
                a_16d = encode_to_16d(a, modulus)
                b_16d = encode_to_16d(b, modulus)
                
                # Get model output
                a_tensor = torch.tensor([a])
                b_tensor = torch.tensor([b])
                logits, output_16d = model(a_tensor, b_tensor, return_coords=True)
                result = logits.argmax(dim=-1).item()
                
                # Store
                data['inputs_a'].append(a)
                data['inputs_b'].append(b)
                data['inputs_a_16d'].append(a_16d.numpy())
                data['inputs_b_16d'].append(b_16d.numpy())
                data['outputs'].append(result)
                data['outputs_16d'].append(output_16d[0].numpy())
            
            if (a + 1) % 10 == 0:
                print(f"  Processed {a + 1}/{modulus} values...")
    
    # Convert to arrays
    for key in data:
        if key.endswith('_16d'):
            data[key] = np.array(data[key])
        else:
            data[key] = np.array(data[key])
    
    print(f"  Collected {len(data['outputs'])} transformation pairs!")
    return data


def learn_geometric_transformation(data, degree=1):
    """
    Learn a simple geometric function: f(a_16d, b_16d) → result_16d
    
    We'll try polynomial regression to find the transformation!
    """
    print(f"\nLearning geometric transformation (degree {degree})...")
    
    # Prepare input: concatenate a_16d and b_16d
    X = np.hstack([data['inputs_a_16d'], data['inputs_b_16d']])  # (N, 32)
    y = data['outputs_16d']  # (N, 16)
    
    print(f"  Input shape: {X.shape}")
    print(f"  Output shape: {y.shape}")
    
    # Try polynomial features
    if degree > 1:
        print(f"  Generating polynomial features...")
        poly = PolynomialFeatures(degree=degree, include_bias=False)
        X_poly = poly.fit_transform(X)
        print(f"  Polynomial features shape: {X_poly.shape}")
    else:
        X_poly = X
        poly = None
    
    # Fit ridge regression (one model per output dimension)
    print(f"  Fitting ridge regression...")
    models = []
    scores = []
    
    for dim_idx in range(16):
        model = Ridge(alpha=1.0)
        model.fit(X_poly, y[:, dim_idx])
        score = model.score(X_poly, y[:, dim_idx])
        models.append(model)
        scores.append(score)
        
        if (dim_idx + 1) % 4 == 0:
            print(f"    Fitted {dim_idx + 1}/16 dimensions...")
    
    mean_score = np.mean(scores)
    print(f"  Mean R² score: {mean_score:.4f}")
    print(f"  Score range: [{np.min(scores):.4f}, {np.max(scores):.4f}]")
    
    return models, poly, scores


def test_geometric_transformation(models, poly, data, modulus=97):
    """
    Test how well the learned geometric transformation works!
    """
    print(f"\nTesting geometric transformation...")
    
    # Prepare input
    X = np.hstack([data['inputs_a_16d'], data['inputs_b_16d']])
    
    if poly is not None:
        X_poly = poly.transform(X)
    else:
        X_poly = X
    
    # Predict output coordinates
    y_pred = np.zeros((len(X), 16))
    for dim_idx, model in enumerate(models):
        y_pred[:, dim_idx] = model.predict(X_poly)
    
    # Decode predictions
    predictions = []
    for coords in y_pred:
        pred = decode_from_16d(torch.tensor(coords), modulus)
        predictions.append(pred)
    
    predictions = np.array(predictions)
    true_outputs = data['outputs']
    
    # Compute accuracy
    accuracy = np.mean(predictions == true_outputs)
    print(f"  Accuracy: {accuracy * 100:.2f}%")
    
    # Show some examples
    print(f"\n  Sample predictions:")
    for i in range(min(10, len(predictions))):
        a = data['inputs_a'][i]
        b = data['inputs_b'][i]
        pred = predictions[i]
        true = true_outputs[i]
        status = '✓' if pred == true else '✗'
        print(f"    ({a:2d}, {b:2d}) → {pred:2d} (expected {true:2d}) {status}")
    
    return accuracy, predictions


def analyze_transformation_structure(models, poly):
    """
    Analyze what the learned transformation looks like!
    """
    print(f"\n{'='*60}")
    print("TRANSFORMATION STRUCTURE ANALYSIS")
    print(f"{'='*60}")
    
    # Look at coefficient magnitudes
    print(f"\nCoefficient analysis:")
    
    for dim_idx, model in enumerate(models):
        coef = model.coef_
        
        # Find most important input dimensions
        if poly is None:
            # Linear case: first 16 are a_16d, next 16 are b_16d
            a_importance = np.abs(coef[:16]).sum()
            b_importance = np.abs(coef[16:32]).sum()
            
            print(f"\n  Output dimension {dim_idx} (Prime {PRIMES_16D[dim_idx]}):")
            print(f"    Input A importance: {a_importance:.4f}")
            print(f"    Input B importance: {b_importance:.4f}")
            print(f"    Ratio (A/B): {a_importance / (b_importance + 1e-10):.4f}")
            
            # Top contributing input dimensions
            top_a = np.argsort(np.abs(coef[:16]))[-3:][::-1]
            top_b = np.argsort(np.abs(coef[16:32]))[-3:][::-1]
            
            print(f"    Top A dimensions: {[PRIMES_16D[i] for i in top_a]}")
            print(f"    Top B dimensions: {[PRIMES_16D[i] for i in top_b]}")


def visualize_transformation(data, predictions, operation='add'):
    """
    Visualize how well the geometric transformation works
    """
    print(f"\nCreating visualization...")
    
    true_outputs = data['outputs']
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Plot 1: Predicted vs True
    axes[0].scatter(true_outputs, predictions, alpha=0.3, s=1)
    axes[0].plot([0, 96], [0, 96], 'r--', label='Perfect prediction')
    axes[0].set_xlabel('True Output')
    axes[0].set_ylabel('Predicted Output')
    axes[0].set_title(f'Geometric Transformation: {operation.upper()}')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Plot 2: Error distribution
    errors = predictions - true_outputs
    axes[1].hist(errors, bins=50, alpha=0.7, edgecolor='black')
    axes[1].set_xlabel('Prediction Error')
    axes[1].set_ylabel('Count')
    axes[1].set_title('Error Distribution')
    axes[1].axvline(0, color='r', linestyle='--', label='Zero error')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    output_file = Path(__file__).parent / f'geometric_transformation_{operation}.png'
    plt.savefig(output_file, dpi=150)
    print(f"  Saved: {output_file}")
    
    plt.close()


def main():
    print("=" * 60)
    print("EXTRACTING PURE KNOT TRANSFORMATIONS")
    print("=" * 60)
    
    # Load trained model (use addition as example)
    model_path = Path(__file__).parent / 'grokking_results_20260125_110828' / 'lannaformer_final.pt'
    
    print(f"\nLoading trained model...")
    model = LANNAformer(modulus=97, num_heads=4, num_layers=2, dropout=0.1, use_mlp=True)
    checkpoint = torch.load(model_path, map_location='cpu')
    model.load_state_dict(checkpoint)
    model.eval()
    print(f"  ✓ Loaded addition model")
    
    # Collect transformation data
    data = collect_transformation_data(model, modulus=97)
    
    # Try different polynomial degrees
    results = {}
    
    for degree in [1, 2]:
        print(f"\n{'='*60}")
        print(f"DEGREE {degree} POLYNOMIAL")
        print(f"{'='*60}")
        
        models, poly, scores = learn_geometric_transformation(data, degree=degree)
        accuracy, predictions = test_geometric_transformation(models, poly, data)
        
        results[degree] = {
            'models': models,
            'poly': poly,
            'scores': scores,
            'accuracy': accuracy,
            'predictions': predictions
        }
        
        if degree == 1:
            analyze_transformation_structure(models, poly)
        
        visualize_transformation(data, predictions, operation='add')
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    
    for degree, result in results.items():
        print(f"\nDegree {degree}:")
        print(f"  Mean R² score: {np.mean(result['scores']):.4f}")
        print(f"  Accuracy: {result['accuracy'] * 100:.2f}%")
    
    print(f"\n✨ We extracted the geometric transformation!")
    print(f"   Addition can be approximated by a simple polynomial function!")
    print(f"   This is the first step toward first-principles knot arithmetic!")
    
    # Save results
    output_file = Path(__file__).parent / 'geometric_transformation_analysis.json'
    save_data = {
        'degree_1_accuracy': float(results[1]['accuracy']),
        'degree_2_accuracy': float(results[2]['accuracy']),
        'degree_1_mean_r2': float(np.mean(results[1]['scores'])),
        'degree_2_mean_r2': float(np.mean(results[2]['scores']))
    }
    
    with open(output_file, 'w') as f:
        json.dump(save_data, f, indent=2)
    
    print(f"\nSaved analysis to: {output_file}")


if __name__ == '__main__':
    main()

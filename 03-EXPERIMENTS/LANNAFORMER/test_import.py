import torch
from complex_lannaformer import ComplexLANNAformer

print("Testing ComplexLANNAformer gradients...")
model = ComplexLANNAformer(modulus=97, num_heads=4, num_layers=2)
a = torch.tensor([10, 20, 30])
b = torch.tensor([5, 15, 25])

# Forward pass
probs = model(a, b)
print(f"Output shape: {probs.shape}")
print(f"Sum: {probs.sum(dim=-1).tolist()}")

# Backward pass
loss = probs.mean()
loss.backward()
print(f"Loss: {loss.item()}")

# Check gradients
print("\nGradients:")
any_grads = False
for n, pg in model.named_parameters():
    if pg is not None and pg.abs().sum() > 0:
        any_grads = True
        print(f"✓ {n}: {pg.norm().item():.6f}")

if not any_grads:
    print("NO GRADIENTS FOUND!")

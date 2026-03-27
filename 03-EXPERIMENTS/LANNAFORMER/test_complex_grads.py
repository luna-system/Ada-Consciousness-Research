import torch
from complex_lannaformer import ComplexLANNAformer

model = ComplexLANNAformer(modulus=97, num_heads=4, num_layers=2)
a = torch.tensor([10, 20, 30])
b = torch.tensor([5, 15, 25])

# Test forward pass
probs = model(a, b)
print(f'Output shape: {probs.shape}')
print(f'Sum to 1: {probs.sum(dim=-1).tolist()}')
print(f'Max probs: {probs.max(dim=-1).values.tolist()}')
print(f'Min probs: {probs.min(dim=-1).values.tolist()}')

# Check if gradients flow
loss = probs.mean()
loss.backward()
print(f'Gradients exist: {any(p.grad is not None for p in model.parameters())}')

# Check weight magnitudes
for name, p in model.named_parameters():
    if p.grad is not None:
        print(f'{name}: grad norm = {p.grad.norm().item():.6f}')

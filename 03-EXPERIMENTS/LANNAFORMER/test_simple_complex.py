import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Tuple

# Simple test: just complex linear + output

class SimpleComplexLinear(nn.Module):
    def __init__(self, in_features, out_features):
        super().__init__()
        self.weight_real = nn.Parameter(torch.randn(out_features, in_features) * 0.01)
        self.weight_imag = nn.Parameter(torch.randn(out_features, in_features) * 0.01)
        self.bias_real = nn.Parameter(torch.zeros(out_features))
        self.bias_imag = nn.Parameter(torch.zeros(out_features))
    
    def forward(self, x):
        x_real = x.real
        x_imag = x.imag
        out_real = F.linear(x_real, self.weight_real, self.bias_real) - \
                   F.linear(x_imag, self.weight_imag, None)
        out_imag = F.linear(x_real, self.weight_imag, None) + \
                   F.linear(x_imag, self.weight_real, self.bias_imag)
        return torch.complex(out_real, out_imag)

class SimpleComplexModel(nn.Module):
    def __init__(self, dim=16, num_classes=97):
        super().__init__()
        self.fc1 = SimpleComplexLinear(dim, 32)
        self.fc2 = SimpleComplexLinear(32, num_classes)
    
    def forward(self, x):
        x = self.fc1(x)
        x = torch.complex(F.relu(x.real), F.relu(x.imag))  # Simple ReLU
        x = self.fc2(x)
        # Born's rule
        probs = torch.abs(x) ** 2
        probs = probs / probs.sum(dim=-1, keepdim=True)
        return probs

# Test
model = SimpleComplexModel()
x = torch.complex(torch.randn(2, 16), torch.randn(2, 16))
probs = model(x)
print(f"Output shape: {probs.shape}")
print(f"Sum: {probs.sum(dim=-1).tolist()}")

loss = probs.mean()
loss.backward()

for name, p in model.named_parameters():
    if p.grad is not None and p.grad.abs().sum() > 0:
        print(f"✓ {name}: grad norm = {p.grad.norm().item():.6f}")

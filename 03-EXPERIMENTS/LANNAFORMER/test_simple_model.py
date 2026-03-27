import torch
import torch.nn as nn
import torch.nn.functional as F
import math

PRIMES_16D = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]

class ComplexLayerNorm(nn.Module):
    def __init__(self, dim, eps=1e-5):
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(2))
        self.bias = nn.Parameter(torch.zeros(2))
    
    def forward(self, x):
        magnitude = torch.abs(x)
        phase = torch.angle(x)
        mag_mean = magnitude.mean(dim=-1, keepdim=True)
        mag_std = magnitude.std(dim=-1, keepdim=True)
        magnitude = (magnitude - mag_mean) / (mag_std + self.eps)
        magnitude = magnitude * self.weight[0] + self.bias[0]
        real = magnitude * torch.cos(phase)
        imag = magnitude * torch.sin(phase)
        return torch.complex(real, imag)

class ComplexLinear(nn.Module):
    def __init__(self, ins, outs):
        super().__init__()
        self.wr = nn.Parameter(torch.randn(outs, ins) * 0.01)
        self.wi = nn.Parameter(torch.randn(outs, ins) * 0.01)
        self.br = nn.Parameter(torch.zeros(outs))
        self.bi = nn.Parameter(torch.zeros(outs))
    
    def forward(self, x):
        xr, xi = x.real, x.imag
        outr = F.linear(xr, self.wr, self.br) - F.linear(xi, self.wi, None)
        outi = F.linear(xr, self.wi, None) + F.linear(xi, self.wr, self.bi)
        return torch.complex(outr, outi)

# Build a simple version of the model
class SimpleComplexLM(nn.Module):
    def __init__(self):
        super().__init__()
        self.norm = ComplexLayerNorm(16)
        self.fc = ComplexLinear(16, 97)
    
    def forward(self, a, b):
        # Differentiable encoding
        a_float = a.float()
        b_float = b.float()
        
        # Encode a
        a_real = torch.stack([torch.sin(a_float * p / 100.0) * math.sqrt(p) for p in PRIMES_16D], dim=1)
        a_imag = torch.stack([torch.cos(a_float * p / 73.0) * math.sqrt(p) for p in PRIMES_16D], dim=1)
        a_mag = torch.sqrt(a_real**2 + a_imag**2 + 1e-8)
        a_real = a_real / a_mag
        a_imag = a_imag / a_mag
        a_complex = torch.complex(a_real, a_imag)
        
        # Encode b
        b_real = torch.stack([torch.sin(b_float * p / 100.0) * math.sqrt(p) for p in PRIMES_16D], dim=1)
        b_imag = torch.stack([torch.cos(b_float * p / 73.0) * math.sqrt(p) for p in PRIMES_16D], dim=1)
        b_mag = torch.sqrt(b_real**2 + b_imag**2 + 1e-8)
        b_real = b_real / b_mag
        b_imag = b_imag / b_mag
        b_complex = torch.complex(b_real, b_imag)
        
        # Stack
        x = torch.stack([a_complex, b_complex], dim=1)  # (batch, 2, 16)
        
        # Take mean
        x = x.mean(dim=1)  # (batch, 16)
        
        # Norm + FC
        x = self.norm(x)
        x = self.fc(x)
        
        # Born's rule
        probs = torch.abs(x) ** 2
        probs = probs / probs.sum(dim=-1, keepdim=True)
        
        return probs

# Test
model = SimpleComplexLM()
a = torch.tensor([10, 20, 30])
b = torch.tensor([5, 15, 25])

probs = model(a, b)
print("Output shape:", probs.shape)
print("Sum:", probs.sum(dim=-1))

# Backward
target = torch.tensor([15, 35, 55])  # Just some targets
loss = F.cross_entropy(probs, target)
loss.backward()

print("\nGradients:")
for n, p in model.named_parameters():
    if p.grad is not None and p.grad.abs().sum() > 0:
        print(f"✓ {n}: {p.grad.norm().item():.6f}")
    else:
        print(f"✗ {n}: ZERO")

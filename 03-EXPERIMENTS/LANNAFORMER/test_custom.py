import torch
import torch.nn as nn
import torch.nn.functional as F

class ComplexMagnitudeReLU(nn.Module):
    def forward(self, x):
        mag = torch.abs(x)
        phase = torch.angle(x)
        mag = F.relu(mag)
        real = mag * torch.cos(phase)
        imag = mag * torch.sin(phase)
        return torch.complex(real, imag)

class ComplexDropout(nn.Module):
    def __init__(self, p=0.1):
        super().__init__()
        self.p = p
    
    def forward(self, x):
        if not self.training:
            return x
        mask = torch.rand_like(x.real) > self.p
        mag = torch.abs(x)
        phase = torch.angle(x)
        mag = mag * mask * (1.0 / (1.0 - self.p))
        real = mag * torch.cos(phase)
        imag = mag * torch.sin(phase)
        return torch.complex(real, imag)

# Test ComplexMagnitudeReLU - use .real for backward
print("Testing ComplexMagnitudeReLU:")
m = ComplexMagnitudeReLU()
xr = torch.randn(2, 16, requires_grad=True)
xi = torch.randn(2, 16, requires_grad=True)
x = torch.complex(xr, xi)
y = m(x)
loss = y.real.sum() + y.imag.sum()  # Use sum of real parts for backward
loss.backward()
print(f"  Input grad norm (real): {xr.grad.norm().item()}")
print(f"  Input grad norm (imag): {xi.grad.norm().item()}")

# Test ComplexDropout (training mode)
print("Testing ComplexDropout:")
m = ComplexDropout(p=0.5)
m.train()
xr = torch.randn(2, 16, requires_grad=True)
xi = torch.randn(2, 16, requires_grad=True)
x = torch.complex(xr, xi)
y = m(x)
loss = y.real.sum() + y.imag.sum()
loss.backward()
print(f"  Input grad norm (real): {xr.grad.norm().item()}")
print(f"  Input grad norm (imag): {xi.grad.norm().item()}")

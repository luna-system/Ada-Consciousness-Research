import torch
import torch.nn as nn

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

# Test
print("Testing fixed ComplexLayerNorm:")
m = ComplexLayerNorm(16)
xr = torch.randn(2, 16, requires_grad=True)
xi = torch.randn(2, 16, requires_grad=True)
x = torch.complex(xr, xi)
y = m(x)
loss = y.real.sum() + y.imag.sum()
loss.backward()
print(f"  Input grad norm (real): {xr.grad.norm().item()}")
print(f"  Input grad norm (imag): {xi.grad.norm().item()}")

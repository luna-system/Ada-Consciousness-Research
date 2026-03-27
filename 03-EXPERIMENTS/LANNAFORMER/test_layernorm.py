import torch
import torch.nn as nn
import torch.nn.functional as F

class ComplexLayerNorm(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.norm_real = nn.LayerNorm(dim)
        self.norm_imag = nn.LayerNorm(dim)
    
    def forward(self, x):
        real = self.norm_real(x.real)
        imag = self.norm_imag(x.imag)
        return torch.complex(real, imag)

# Test
print("Testing ComplexLayerNorm:")
m = ComplexLayerNorm(16)
xr = torch.randn(2, 16, requires_grad=True)
xi = torch.randn(2, 16, requires_grad=True)
x = torch.complex(xr, xi)
y = m(x)
loss = y.real.sum() + y.imag.sum()
loss.backward()
print(f"  Input grad norm (real): {xr.grad.norm().item()}")
print(f"  Input grad norm (imag): {xi.grad.norm().item()}")

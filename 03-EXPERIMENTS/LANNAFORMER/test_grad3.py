import torch
import torch.nn as nn
import torch.nn.functional as F

class SimpleComplexLinear(nn.Module):
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

class SimpleModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = SimpleComplexLinear(16, 32)
        self.fc2 = SimpleComplexLinear(32, 97)
    
    def forward(self, x):
        x = self.fc1(x)
        x = torch.complex(F.relu(x.real), F.relu(x.imag))
        x = self.fc2(x)
        probs = (x.abs() ** 2)
        probs = probs.sum()  # Just sum everything for loss
        return probs

m = SimpleModel()
x = torch.complex(torch.randn(2, 16), torch.randn(2, 16))
print("x shape:", x.shape)
print("x dtype:", x.dtype)

p = m(x)
print("output:", p)
print("output shape:", p.shape)
print("output requires_grad:", p.requires_grad)

loss = p  # Already a scalar
print("loss:", loss)

loss.backward()

print("\nGradients:")
for n, pg in m.named_parameters():
    g = pg.grad
    print(f"{n}: grad is None? {g is None}, grad norm: {g.norm().item() if g is not None else 'N/A'}")

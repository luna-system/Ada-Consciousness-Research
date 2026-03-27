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
        probs = probs / probs.sum(-1, keepdim=True)
        return probs

m = SimpleModel()
x = torch.complex(torch.randn(2, 16), torch.randn(2, 16))
p = m(x)
loss = p.mean()
loss.backward()

print("Testing gradients in simple complex model:")
for n, pg in m.named_parameters():
    g = pg.grad
    if g is not None and g.abs().sum() > 0:
        print(f'OK {n}: {g.norm().item():.6f}')
    else:
        print(f'NO {n}')

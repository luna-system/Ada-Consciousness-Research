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
        # Try F.relu instead of manual complex relu
        x = F.relu(x.real) + 1j * F.relu(x.imag)
        x = self.fc2(x)
        # Born's rule: |z|^2
        probs = torch.abs(x) ** 2
        # Normal THIS Mize -IGHT BE BREAKING GRADS!
        probs = probs / probs.sum(dim=-1, keepdim=True)
        return probs

m = SimpleModel()
x = torch.complex(torch.randn(2, 16), torch.randn(2, 16))
target = torch.tensor([10, 20])

p = m(x)
print("probs shape:", p.shape)
print("probs sum:", p.sum(dim=-1))

criterion = nn.CrossEntropyLoss()
loss = criterion(p, target)
print("loss:", loss)

loss.backward()

print("\nGradients with CrossEntropyLoss:")
for n, pg in m.named_parameters():
    g = pg.grad
    if g is None:
        print(f"{n}: grad is None")
    else:
        print(f"{n}: grad norm: {g.norm().item():.6f}")

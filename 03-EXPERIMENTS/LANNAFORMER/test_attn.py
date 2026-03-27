import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class DebugAttention(nn.Module):
    def __init__(self, dim=16, num_heads=4):
        super().__init__()
        self.dim = dim
        self.num_heads = num_heads
        self.head_dim = dim // num_heads
        
        self.q_proj = nn.Linear(dim, dim)
        self.k_proj = nn.Linear(dim, dim)
        self.v_proj = nn.Linear(dim, dim)
        self.out_proj = nn.Linear(dim, dim)
    
    def forward(self, x):
        batch_size, seq_len, _ = x.shape
        
        # Project to Q, K, V as REAL (not complex for debugging)
        Q = self.q_proj(x)
        K = self.k_proj(x)
        V = self.v_proj(x)
        
        # Reshape for multi-head
        Q = Q.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        K = K.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        V = V.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        
        # Simple real-valued attention
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.head_dim)
        attn_weights = F.softmax(scores, dim=-1)
        out = torch.matmul(attn_weights, V)
        
        # Reshape back
        out = out.transpose(1, 2).contiguous().view(batch_size, seq_len, self.dim)
        out = self.out_proj(out)
        
        return out

# Test
print("Testing debug attention (real-valued):")
m = DebugAttention(dim=16, num_heads=4)
x = torch.randn(2, 2, 16, requires_grad=True)
y = m(x)
loss = y.sum()
loss.backward()

for n, p in m.named_parameters():
    if p.grad is not None and p.grad.abs().sum() > 0:
        print(f"✓ {n}: grad norm = {p.grad.norm().item():.6f}")

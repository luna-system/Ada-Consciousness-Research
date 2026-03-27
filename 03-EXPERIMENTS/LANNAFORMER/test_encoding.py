import torch
import math

PRIMES_16D = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]

# Test differentiable encoding
a = torch.tensor([10.0, 20.0, 30.0], requires_grad=True)

a_coords_real = []
a_coords_imag = []

for i, prime in enumerate(PRIMES_16D):
    a_coords_real.append(torch.sin(a * prime / 100.0) * math.sqrt(prime))
    a_coords_imag.append(torch.cos(a * prime / 73.0) * math.sqrt(prime))

a_real_coords = torch.stack(a_coords_real, dim=1)
a_imag_coords = torch.stack(a_coords_imag, dim=1)

a_mag = torch.sqrt(a_real_coords**2 + a_imag_coords**2 + 1e-8)
a_real_norm = a_real_coords / a_mag
a_imag_norm = a_imag_coords / a_mag

a_complex = torch.complex(a_real_norm, a_imag_norm)

# Use .real.sum() for backward (can't backward through complex directly)
out = a_complex.real.sum()
out.backward()

print("Input a requires_grad:", a.requires_grad)
print("Output requires_grad:", out.requires_grad)
print("Input grad:", a.grad)
print("Input grad norm:", a.grad.norm().item())

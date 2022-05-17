import torch

N = 5
M = 10
L = 20
A = torch.rand((N, M))
B = torch.rand((N, N))
V = torch.rand((N, L))

z = V[:, 1] * A.t()[1] * B.t()[1]
print(V[:, 1].shape, A.t()[1].shape, B.t()[1].shape)
print(z)
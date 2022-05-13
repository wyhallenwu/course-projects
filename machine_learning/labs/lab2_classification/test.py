import torch

n = 5
x = torch.tensor([[1, 2, 3, 4], [1, 2, 3, 4]])
y = torch.tensor([5, 6, 7, 8])
x[0, :] = y
print(x, x.shape)
x = x.repeat(1, n)
print(x, x.shape)
print(x.view(2, n, -1))

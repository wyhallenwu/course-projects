import torch
import torch.functional as F

x = torch.rand(5, 10)
x = torch.softmax(x, dim=0)
print(x)

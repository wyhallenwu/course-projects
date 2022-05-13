import torch
import torch.nn as nn
import torch.optim


class Model(nn.Module):
    def __init__(self, input_dim):
        super(Model, self).__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_dim, 16),
            nn.ReLU(),
            nn.Linear(16, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
        )

    def forward(self, x):
        x = self.layers(x)
        x = x.squeeze()
        return x

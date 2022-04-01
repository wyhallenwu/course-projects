import torch
import torch.nn as nn


class DQNnet(nn.Module):
    def __init__(self, state_dim, action_dim):
        self.state_dimension = state_dim
        self.action_dimension = action_dim

        super(DQNnet, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(self.state_dimension, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, self.action_dimension),
        )

    def forward(self, current_state):
        s = torch.tensor(current_state)
        actions = self.net(s)
        return actions





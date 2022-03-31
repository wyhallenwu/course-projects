import torch
import torch.nn as nn


class DQN(nn.Module):
    def __init__(self, state_dim, action_dim, learning_rate):
        self.state_dimension = state_dim
        self.action_dimension = action_dim
        self.learning_rate = learning_rate

        super(DQN).__init__()
        self.net = nn.Sequential(
            nn.Linear(self.state_dimension, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, self.action_dimension),
        )

    def forward(self, current_state):
        s = torch.tensor(current_state)
        action_prob = self.net(s)
        return action_prob



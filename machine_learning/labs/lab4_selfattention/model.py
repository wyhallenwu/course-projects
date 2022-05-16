import torch
import torch.nn as nn
import torch.nn.functional as F


class Classifier(nn.Module):
    def __init__(self, d_model=80, speaker_num=600, dropout=0.1):
        super(Classifier, self).__init__()
        self.prenet = nn.Linear(40, d_model)

        self.encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model, dim_feedforward=256, nhead=2
        )
        self.pred_layer = nn.Sequential(
            nn.Linear(d_model, d_model), nn.ReLU(), nn.Linear(d_model, speaker_num)
        )

    def forward(self, mels):
        # (batch_size, length, d_model)
        outs = self.prenet(mels)
        # (length, batch_size, d_model)
        outs = outs.permute(1, 0, 2)
        outs = self.encoder_layer(outs)
        # (batch_size, length, d_model)
        outs = outs.transpose(0, 1)
        # mean pooling
        stats = outs.mean(dim=1)
        # (batch_size, speaker_num)
        prediction = self.pred_layer(stats)
        return prediction

import torch
from torch.utils.data import DataLoader, Dataset, random_split
from torch.nn.utils.rnn import pad_sequence
import os
import json
import utils
import random

config = utils.config


class VoxDataset(Dataset):

    def __init__(self, data_dir, seg_len=128):
        self.data_dir = data_dir
        self.seg_len = seg_len
        # speaker2id mappings
        self.speaker2id = json.load(open(
            config["speaker2id_mapping"]))["speaker2id"]
        # meta data
        metadata = json.load(open(config["meta_data"]))
        self.n_mels = metadata["n_mels"]
        self.speakers = metadata["speakers"]
        self.speaker_num = len(self.speakers.keys())

        self.data = []
        for speaker in self.speakers.keys():
            for uttr in self.speakers[speaker]:
                self.data.append([
                    uttr["feature_path"], self.speaker2id[speaker],
                    uttr["mel_len"]
                ])

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        # print(self.data[index])
        feat_path, speaker_label, mel_len = self.data[index]
        mel = torch.load(os.path.join(config["data_dir"], feat_path))
        if mel_len > self.seg_len:
            start = random.randint(0, mel_len - self.seg_len)
            mel = torch.FloatTensor(mel[start:start + self.seg_len])
        else:
            mel = torch.FloatTensor(mel)
        speaker = torch.FloatTensor([speaker_label]).long()
        return mel, speaker

    def get_speaker_num(self):
        return self.speaker_num


def collate_fn(batch):
    """process feature within a batch."""
    mel, speaker = zip(*batch)
    # pad the mel for futher use, pad 10^(-20) which is a very small value
    mel = pad_sequence(mel, batch_first=True, padding_value=-20)
    # mel (batch_size, length, 40)
    return mel, torch.FloatTensor(speaker).long()


def get_dataloader(data_dir, batch_size, n_workers=1):
    """generate dataloader."""
    dataset = VoxDataset(data_dir=data_dir)
    train_len = int(config["split_ratio"] * len(dataset))
    length = [train_len, len(dataset) - train_len]
    trainset, validset = random_split(dataset, length)
    speaker_num = dataset.get_speaker_num()
    train_loader = DataLoader(
        dataset=trainset,
        batch_size=batch_size,
        collate_fn=collate_fn,
        shuffle=True,
        num_workers=n_workers,
        pin_memory=True,
        drop_last=True,
    )
    valid_loader = DataLoader(
        dataset=validset,
        batch_size=batch_size,
        shuffle=True,
        collate_fn=collate_fn,
        num_workers=n_workers,
        drop_last=True,
        pin_memory=True,
    )
    return train_loader, valid_loader, speaker_num

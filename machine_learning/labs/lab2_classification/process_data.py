import torch
import os
import pandas as pd
import random
from tqdm import tqdm
import yaml


def load_features(file):
    features = torch.load(file)
    return features


def shift(x, n):
    if n < 0:
        left = x[0].repeat(-n, 1)
        right = x[:n]

    elif n > 0:
        right = x[-1].repeat(n, 1)
        left = x[n:]
    else:
        return x

    return torch.cat((left, right), dim=0)


def concat_feat(x, concat_n):
    assert concat_n % 2 == 1  # n must be odd
    if concat_n < 2:
        return x
    seq_len, feature_dim = x.size(0), x.size(1)
    x = x.repeat(1, concat_n)
    x = x.view(seq_len, concat_n, feature_dim).permute(
        1, 0, 2
    )  # concat_n, seq_len, feature_dim
    mid = concat_n // 2
    for r_idx in range(1, mid + 1):
        x[mid + r_idx, :] = shift(x[mid + r_idx], r_idx)
        x[mid - r_idx, :] = shift(x[mid - r_idx], -r_idx)

    return x.permute(1, 0, 2).view(seq_len, concat_n * feature_dim)


def preprocess_data(
    split, feat_dir, phone_path, concat_nframes, train_ratio=0.8, train_val_seed=1337
):
    class_num = 41  # NOTE: pre-computed, should not need change
    mode = "train" if (split == "train" or split == "val") else "test"

    label_dict = {}
    if mode != "test":
        phone_file = open(os.path.join(phone_path, f"{mode}_labels.txt")).readlines()

        for line in phone_file:
            line = line.strip("\n").split(" ")
            label_dict[line[0]] = [int(p) for p in line[1:]]

    if split == "train" or split == "val":
        # split training and validation data
        usage_list = open(os.path.join(phone_path, "train_split.txt")).readlines()
        random.seed(train_val_seed)
        random.shuffle(usage_list)
        percent = int(len(usage_list) * train_ratio)
        usage_list = usage_list[:percent] if split == "train" else usage_list[percent:]
    elif split == "test":
        usage_list = open(os.path.join(phone_path, "test_split.txt")).readlines()
    else:
        raise ValueError("Invalid 'split' argument for dataset: PhoneDataset!")

    usage_list = [line.strip("\n") for line in usage_list]
    print(
        "[Dataset] - # phone classes: "
        + str(class_num)
        + ", number of utterances for "
        + split
        + ": "
        + str(len(usage_list))
    )

    max_len = 3000000
    X = torch.empty(max_len, 39 * concat_nframes)
    if mode != "test":
        y = torch.empty(max_len, dtype=torch.long)

    idx = 0
    for i, fname in tqdm(enumerate(usage_list)):
        feat = load_features(os.path.join(feat_dir, mode, f"{fname}.pt"))
        cur_len = len(feat)
        feat = concat_feat(feat, concat_nframes)
        if mode != "test":
            label = torch.LongTensor(label_dict[fname])

        X[idx : idx + cur_len, :] = feat
        if mode != "test":
            y[idx : idx + cur_len] = label

        idx += cur_len

    X = X[:idx, :]
    if mode != "test":
        y = y[:idx]

    print(f"[INFO] {split} set")
    print(X.shape)
    if mode != "test":
        print(y.shape)
        return X, y
    else:
        return X


def read_config(file="./config.yaml"):
    with open(file, "r") as f:
        config = yaml.safe_load(f)
        return config


if __name__ == "__main__":
    config = read_config()
    print(config["seed"])

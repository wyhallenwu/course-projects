from posixpath import split
import time
import numpy as np
import torch
import torch.nn as nn
from tqdm import tqdm
from sklearn.model_selection import KFold
from torch.utils.data import DataLoader, ConcatDataset, SubsetRandomSampler
import utils
import prepocess_data

# config = utils.read_config('./config.yml')
# device = 'cuda' if torch.cuda.is_available() else 'cpu'

# # prepare dataloader
# trainset = prepocess_data.FoodDataset(
#     config['train_dir'], prepocess_data.train_tfm, train_flag=True)
# train_loader = DataLoader(
#     trainset, batch_size=config['batch_size'], shuffle=True)
# validset = prepocess_data.FoodDataset(
#     config['valid_dir'], prepocess_data.test_tfm, train_flag=True)
# valid_loader = DataLoader(
#     validset, batch_size=config['batch_size'], shuffle=True)

# dataset = ConcatDataset([trainset, validset])

# kf = KFold(n_splits=4, shuffle=True, random_state=42)
# for fold, (train_idx, val_idx) in enumerate(kf.split(np.arange(len(dataset)))):
#     print("fold: {}".format(fold + 1))
#     train_sampler = SubsetRandomSampler(train_idx)
#     valid_sampler = SubsetRandomSampler(val_idx)
#     train_loader = DataLoader(dataset, batch_size=64, sampler=train_sampler)
#     valid_loader = DataLoader(dataset, batch_size=64, sampler=valid_sampler)

x = torch.ones(64, 1)
y = torch.zeros(64, 1)
z = torch.cat([x, y], dim=1)
print(z)
print(z.view(64, 2))

import torch
import numpy as np
import yaml


def same_seed():
    # fix seed
    myseed = 6666
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    np.random.seed(myseed)
    torch.manual_seed(myseed)
    if torch.cuda.is_available():
        # seed all gpu
        torch.cuda.manual_seed_all(myseed)


def read_config(filename):
    with open(filename, 'r') as f:
        return yaml.safe_load(f)


def pad4(i):
    return "0"*(4-len(str(i)))+str(i)


def multi_cre_loss(pred, label1, label2, alpha, standard_cre_fn):
    loss1 = standard_cre_fn(pred, label1)
    loss2 = standard_cre_fn(pred, label2)
    # print(loss2.shape)
    return loss1 * alpha + loss2 * (1 - alpha)


def multi_acc(pred, label1, label2):
    # print(label1.shape, label2.shape)
    labels = torch.cat([label1.view(pred.shape[0], 1),
                       label2.view(pred.shape[0], 1)], dim=1)
    # print(labels.shape)
    # labels = labels.view(pred.shape[0], 2)
    # print(labels.shape)
    _, indices = torch.topk(pred, 2, dim=1)
    labels, _ = torch.sort(labels)
    indices, _ = torch.sort(indices)
    # print(labels.shape, indices.shape)
    return torch.count_nonzero((labels == indices)) / (pred.shape[0] * 2.0)

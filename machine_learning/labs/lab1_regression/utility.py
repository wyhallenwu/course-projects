import torch
import torch.nn as nn
from torch.utils.tensorboard import SummaryWriter
import math
import numpy as np
from torch.utils.data import Dataset, random_split
from tqdm import tqdm
import os


def same_seed(seed):
    """fixes random number for reproducibility."""
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def train_valid_split(dataset, valid_ratio, seed):
    """Split training dataset into train and validation"""
    validset_size = int(valid_ratio * len(dataset))
    trainset_size = len(dataset) - validset_size
    trainset, validset = random_split(
        dataset,
        [trainset_size, validset_size],
        generator=torch.Generator().manual_seed(seed),
    )
    return np.array(trainset), np.array(validset)


def predict(test_loader, model, device):
    model.eval()
    preds = []
    for x in tqdm(test_loader):
        x = x.to(device)
        with torch.no_grad():
            pred = model(x)
            preds.append(pred.detach().cpu())
    preds = torch.cat(preds, dim=0).numpy()
    return preds


class CovidDataset(Dataset):
    """Dataset
    Arg:
        x: features
        y: target
    """

    def __init__(self, x, y=None):
        if y is None:
            self.y = y
        else:
            self.y = torch.FloatTensor(y)
        self.x = torch.FloatTensor(x)

    def __getitem__(self, index):
        if self.y is None:
            return self.x[index]
        else:
            return self.x[index], self.y[index]

    def __len__(self):
        return len(self.x)


def select_features(trainset, validset, testdata, select_all=True):
    """Select useful features in the dataset."""
    y_train, y_valid = trainset[:, -1], validset[:, -1]
    raw_x_train, raw_x_valid, raw_x_test = trainset[:, :-1], validset[:, :-1], testdata

    if select_all:
        feature_index = list(range(raw_x_train.shape[1]))
    else:
        feature_index = list(
            range(38, raw_x_train.shape[1])
        )  # location may not useful here

    return (
        raw_x_train[:, feature_index],
        raw_x_valid[:, feature_index],
        raw_x_test[:, feature_index],
        y_train,
        y_valid,
    )


def trainer(train_loader, valid_loader, model, config, device):
    criterion = nn.MSELoss(reduction="mean")
    optimizer = torch.optim.SGD(
        model.parameters(), lr=config["learning_rate"], momentum=0.9
    )
    writer = SummaryWriter()
    if not os.path.isdir("./models"):
        os.mkdir("./models")

    n_epochs, best_loss, step, early_stop_count = config["n_epochs"], math.inf, 0, 0

    for epoch in range(n_epochs):
        model.train()
        loss_record = []
        train_pbar = tqdm(train_loader, position=0, leave=True)

        for x, y in train_pbar:
            optimizer.zero_grad()
            x, y = x.to(device), y.to(device)
            pred = model(x)
            loss = criterion(pred, y)
            loss.backward()
            optimizer.step()
            step += 1
            loss_record.append(loss.detach().item())

            # display
            train_pbar.set_description(f"Epoch [{epoch+1} / {n_epochs}]")
            train_pbar.set_postfix({"loss: ": loss.detach().item()})

        mean_train_loss = sum(loss_record) / len(loss_record)
        writer.add_scalar("Loss/train", mean_train_loss, step)

        model.eval()
        loss_record = []
        for x, y in valid_loader:
            x, y = x.to(device), y.to(device)
            with torch.no_grad():
                pred = model(x)
                loss = criterion(pred, y)
            loss_record.append(loss)
        mean_valid_loss = sum(loss_record) / len(loss_record)
        print(
            f"Epoch [{epoch+1} / {n_epochs}]: train_loss: {mean_train_loss:.4f}, valid loss: {mean_valid_loss:.4f}"
        )
        writer.add_scalar("Loss/valid", mean_valid_loss, step)

        if mean_valid_loss < best_loss:
            best_loss = mean_valid_loss
            torch.save(model.state_dict(), config["save_path"])  # Save your best model
            print("Saving model with loss {:.3f}...".format(best_loss))
            early_stop_count = 0
        else:
            early_stop_count += 1

        if early_stop_count >= config["early_stop"]:
            print("\nModel is not improving, so we halt the training session.")
            return

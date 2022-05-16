import torch
import torch.nn as nn
import torch.optim
from util import LibriDataset, same_seed
import process_data
import gc
from torch.utils.data import DataLoader
from model import Classifier
from tqdm import tqdm
import numpy as np


config = process_data.read_config("./config.yaml")
# data prarameters
concat_nframes = config[
    "concat_nframes"
]  # the number of frames to concat with, n must be odd (total 2k+1 = n frames)
train_ratio = config[
    "train_ratio"
]  # the ratio of data used for training, the rest will be used for validation

# training parameters
seed = config["seed"]  # random seed
batch_size = config["batch_size"]  # batch size
num_epoch = config["num_epoch"]  # the number of training epoch
learning_rate = config["learning_rate"]  # learning rate
model_path = config["model_path"]  # the path where the checkpoint will be saved

# model parameters
input_dim = (
    config["input_dim"] * config["concat_nframes"]
)  # the input dim of the model, you should not change the value
hidden_layers = config["hidden_layers"]  # the number of hidden layers
hidden_dim = config["hidden_dim"]  # the hidden dim


if __name__ == "__main__":
    # preprocess dataset
    train_x, train_y = process_data.preprocess_data(
        split="train",
        feat_dir="./dataset/libriphone/libriphone/feat",
        phone_path="./dataset/libriphone/libriphone",
        concat_nframes=concat_nframes,
        train_ratio=train_ratio,
    )
    val_x, val_y = process_data.preprocess_data(
        split="val",
        feat_dir="./dataset/libriphone/libriphone/feat",
        phone_path="./dataset/libriphone/libriphone",
        concat_nframes=concat_nframes,
        train_ratio=train_ratio,
    )

    # get dataset
    trainset = LibriDataset(train_x, train_y)
    valset = LibriDataset(val_x, val_y)
    # remove raw data to save memory
    del train_x, train_y, val_x, val_y
    gc.collect()

    # get dataloader
    train_loader = DataLoader(trainset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(valset, batch_size=batch_size, shuffle=True)

    # device
    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    # fix random seed
    same_seed(seed)

    # create model
    model = Classifier(
        input_dim=input_dim, hidden_layers=hidden_layers, hidden_dim=hidden_dim
    ).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)

    # training
    best_acc = 0
    for epoch in range(num_epoch):
        # evaluations
        train_acc = 0.0
        train_loss = 0.0
        val_acc = 0.0
        val_loss = 0.0

        for i, batch in enumerate(tqdm(train_loader)):
            # data
            features, labels = batch
            features = features.to(device)
            labels = labels.to(device)
            # predict
            optimizer.zero_grad()
            outputs = model(features)
            # loss
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            _, train_pred = torch.max(outputs, 1)
            train_acc += (train_pred.detach() == labels.detach()).sum().item()
            train_loss += loss.item()

        # validation
        if len(valset):
            model.eval()
            with torch.no_grad():
                for i, batch in enumerate(tqdm(val_loader)):
                    # data
                    features, labels = batch
                    features = features.to(device)
                    labels = labels.to(device)
                    # predict
                    outputs = model(features)
                    loss = criterion(outputs, labels)

                    _, val_pred = torch.max(outputs, 1)
                    val_acc += (val_pred.cpu() == labels.cpu()).sum().item()
                    val_loss += loss.item()

                # if model improves, save checkpoint
                if val_acc > best_acc:
                    best_acc = val_acc
                    torch.save(model.state_dict(), model_path)
                    print("saving model with acc {:.3f}".format(best_acc / len(valset)))
                else:
                    print(
                        "[{:03d}/{:03d}] Train Acc: {:3.6f} Loss: {:3.6f}".format(
                            epoch + 1,
                            num_epoch,
                            train_acc / len(trainset),
                            train_loss / len(train_loader),
                        )
                    )

    if len(valset) == 0:
        torch.save(model.state_dict(), model_path)
        print("saving at last epoch")

    del train_loader, val_loader
    gc.collect()

    # testing
    test_x = process_data.preprocess_data(
        split="test",
        feat_dir="./dataset/libriphone/libriphone/feat",
        phone_path="./dataset/libriphone/libriphone",
        concat_nframes=concat_nframes,
    )
    testset = LibriDataset(test_x, None)
    test_loader = DataLoader(testset, batch_size=batch_size, shuffle=True)

    # load model
    model = Classifier(
        input_dim=input_dim, hidden_layers=hidden_layers, hidden_dim=hidden_dim
    ).to(device)
    model.load_state_dict(torch.load(model_path))

    test_acc = 0.0
    test_lengths = 0
    pred = np.array([], dtype=np.int32)

    model.eval()
    with torch.no_grad():
        for i, batch in enumerate(tqdm(test_loader)):
            features = batch
            features = features.to(device)

            outputs = model(features)

            _, test_pred = torch.max(
                outputs, 1
            )  # get the index of the class with the highest probability
            pred = np.concatenate((pred, test_pred.cpu().numpy()), axis=0)

    with open("prediction.csv", "w") as f:
        f.write("Id,Class\n")
        for i, y in enumerate(pred):
            f.write("{},{}\n".format(i, y))

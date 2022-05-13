import torch
import pandas as pd
from model import Model
from utility import CovidDataset, same_seed, select_features, train_valid_split, trainer
from config import config, device
from torch.utils.data import DataLoader

if __name__ == "__main__":
    same_seed(config["seed"])

    train_data, test_data = (
        pd.read_csv("./dataset/covid.train.csv").values,
        pd.read_csv("./dataset/covid.test.csv").values,
    )
    train_data, valid_data = train_valid_split(
        train_data, config["valid_ratio"], config["seed"]
    )

    print(
        f"""train_data size: {train_data.shape} 
        valid_data size: {valid_data.shape} 
        test_data size: {test_data.shape}"""
    )

    # select features
    x_train, x_valid, x_test, y_train, y_valid = select_features(
        train_data, valid_data, test_data, config["select_all"]
    )

    print(f"number of features: {x_train.shape[1]}")

    train_dataset, valid_dataset, test_dataset = (
        CovidDataset(x_train, y_train),
        CovidDataset(x_valid, y_valid),
        CovidDataset(x_test),
    )

    train_loader = DataLoader(
        train_dataset, batch_size=config["batch_size"], shuffle=True, pin_memory=True
    )
    valid_loader = DataLoader(
        valid_dataset, batch_size=config["batch_size"], shuffle=True, pin_memory=True
    )
    test_loader = DataLoader(
        test_dataset, batch_size=config["batch_size"], shuffle=True, pin_memory=True
    )

    model = Model(input_dim=x_train.shape[1]).to(device)
    trainer(train_loader, valid_loader, model, config, device)

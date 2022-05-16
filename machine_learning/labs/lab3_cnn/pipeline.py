from sklearn.model_selection import KFold
import torch
import torch.nn as nn
import time
import torch.optim
import prepocess_data
import utils
from torch.utils.data import DataLoader, ConcatDataset, SubsetRandomSampler
from model import Classifier, Residual_Network
from tqdm import tqdm
import numpy as np
import pandas as pd
from torch.utils.tensorboard import SummaryWriter

config = utils.read_config("./config.yml")
device = "cuda" if torch.cuda.is_available() else "cpu"
writer = SummaryWriter()


def train():
    # prepare dataloader
    trainset = prepocess_data.FoodDataset(
        config["train_dir"], prepocess_data.train_tfm, train_flag=True
    )
    train_loader = DataLoader(trainset, batch_size=config["batch_size"], shuffle=True)
    validset = prepocess_data.FoodDataset(
        config["valid_dir"], prepocess_data.test_tfm, train_flag=True
    )
    valid_loader = DataLoader(validset, batch_size=config["batch_size"], shuffle=True)
    # ===========================cross validation=====================
    dataset = ConcatDataset([trainset, validset])
    kf = KFold(
        n_splits=config["cross_validation_splits"], shuffle=True, random_state=42
    )
    # step count
    step_count_train = step_count_valid = 1
    step_avg_train = step_avg_val = 1
    best_acc = 0

    # construct model
    model = Residual_Network().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=config["learning_rate"],
        weight_decay=config["weight_decay"],
    )
    for fold, (train_idx, valid_idx) in enumerate(kf.split(np.arange(len(dataset)))):
        print("fold: {}".format(fold + 1))
        train_sampler = SubsetRandomSampler(train_idx)
        valid_sampler = SubsetRandomSampler(valid_idx)
        train_loader = DataLoader(
            dataset, batch_size=config["batch_size"], sampler=train_sampler
        )
        valid_loader = DataLoader(
            dataset, batch_size=config["batch_size"], sampler=valid_sampler
        )

        # ================================================================

        # patience
        stale = 0

        # training
        for epoch in range(config["epoch"]):
            model.train()
            train_loss = []
            train_accs = []

            for i, batch in enumerate(tqdm(train_loader)):
                # fetch data
                imgs, label1, label2 = batch
                optimizer.zero_grad()
                # feed data
                logits = model(imgs.to(device))
                # loss = criterion(logits, labels)
                loss = utils.multi_cre_loss(
                    logits,
                    label1.to(device),
                    label2.to(device),
                    config["alpha"],
                    criterion,
                )
                # update
                loss.backward()
                # Clip the gradient norms for stable training.
                grad_norm = nn.utils.clip_grad_norm_(model.parameters(), max_norm=10)
                optimizer.step()

                # acc = (logits.argmax(dim=-1) == labels.to(device)).float().mean()
                acc = utils.multi_acc(logits, label1.to(device), label2.to(device))
                # print(acc)
                train_loss.append(loss.item())
                train_accs.append(acc)
                # visualize
                writer.add_scalar("Loss/Train", loss.item(), step_count_train)
                writer.add_scalar("Acc/Train", acc, step_count_train)
                step_count_train += 1
            train_loss = sum(train_loss) / len(train_loss)
            train_accs = sum(train_accs) / len(train_accs)
            writer.add_scalar("avgLoss/Train", train_loss, step_avg_train)
            writer.add_scalar("avgAccs/Train", train_accs, step_avg_train)
            step_avg_train += 1

            print(
                f"train | [{epoch + 1:03d}/{config['epoch']:03d}] loss={train_loss:.5f}, acc={train_accs:.5f}"
            )
            with open(config["log_file"], "a") as f:
                f.writelines(
                    f"train | [{epoch + 1:03d}/{config['epoch']:03d}] loss={train_loss:.5f}, acc={train_accs:.5f}\r\n"
                )

            # validation
            model.eval()
            valid_loss = []
            valid_accs = []
            for i, batch in enumerate(tqdm(valid_loader)):
                imgs, label1, label2 = batch
                with torch.no_grad():
                    logits = model(imgs.to(device))
                # loss = criterion(logits, labels.to(device))
                loss = utils.multi_cre_loss(
                    logits,
                    label1.to(device),
                    label2.to(device),
                    config["alpha"],
                    criterion,
                )
                # acc = (logits.argmax(dim=-1) == labels.to(device)).float().mean()
                acc = utils.multi_acc(logits, label1.to(device), label2.to(device))

                valid_loss.append(loss.item())
                valid_accs.append(acc)
                writer.add_scalar("Loss/Valid", loss.item(), step_count_valid)
                writer.add_scalar("Acc/Valid", acc, step_count_valid)
                step_count_valid += 1
            valid_loss = sum(valid_loss) / len(valid_loss)
            valid_acc = sum(valid_accs) / len(valid_accs)
            writer.add_scalar("avgLoss/Valid", valid_loss, step_avg_val)
            writer.add_scalar("avgAccs/Valid", valid_acc, step_avg_val)
            step_avg_val += 1
            print(
                f"valid | [{epoch + 1:03d}/{config['epoch']:03d}] loss={valid_loss:.5f}, acc={valid_acc:.5f}"
            )

            # update logs
            if valid_acc > best_acc:
                with open(config["log_file"], "a") as f:
                    print(
                        f"[ Valid | {epoch + 1:03d}/{config['epoch']:03d} ] loss = {valid_loss:.5f}, acc = {valid_acc:.5f} -> best"
                    )
                    f.writelines(
                        f"[ Valid | {epoch + 1:03d}/{config['epoch']:03d} ] loss = {valid_loss:.5f}, acc = {valid_acc:.5f} -> best\r\n"
                    )
            else:
                with open(config["log_file"], "a") as f:
                    print(
                        f"[ Valid | {epoch + 1:03d}/{config['epoch']:03d} ] loss = {valid_loss:.5f}, acc = {valid_acc:.5f}"
                    )
                    f.writelines(
                        f"[ Valid | {epoch + 1:03d}/{config['epoch']:03d} ] loss = {valid_loss:.5f}, acc = {valid_acc:.5f}\r\n"
                    )

            # save models
            if valid_acc > best_acc:
                print(f"save best model at epoch {epoch+1:03d}")
                torch.save(model.state_dict(), config["model_path"] + "best.ckpt")
                best_acc = valid_acc
                stale = 0
            else:
                stale += 1
                if stale > config["early_stop"]:
                    print(f"no improvement. early stop at {epoch + 1}")
                    break


def test():
    testset = prepocess_data.FoodDataset(
        config["test_dir"], prepocess_data.test_tfm, train_flag=False
    )
    test_loader = DataLoader(
        testset, batch_size=config["batch_size"], shuffle=False, pin_memory=True
    )

    model = Classifier().to(device)
    model.load_state_dict(torch.load(config["model_path"] + "best.ckpt"))
    model.eval()
    prediction = []
    with torch.no_grad():
        for data, _ in test_loader:
            test_pred = model(data.to(device))
            test_label = np.argmax(test_pred.cpu().data.numpy(), axis=1)
            prediction += test_label.squeeze().tolist()
    # create test csv
    df = pd.DataFrame()
    df["Id"] = [utils.pad4(i) for i in range(1, len(testset) + 1)]
    df["Category"] = prediction
    df.to_csv("./submission.csv", index=False)

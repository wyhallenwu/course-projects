import torch
from tqdm import tqdm
import utils
import torch.nn as nn
import torch.optim
from model import Classifier
import dataset
from torch.utils.tensorboard import SummaryWriter
import time


def training_pipeline(config):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    config['log_file'] = str(time.strftime(
        "%m%d_%H%M%S", time.localtime())) + config['log_file']
    writer = SummaryWriter()
    trainloader, validloader, speaker_num = dataset.get_dataloader(
        config['data_dir'], config['batch_size'], 1)
    # models
    model = Classifier(d_model=config['d_model'],
                       dropout=config['dropout']).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
    scheduler = utils.get_cosine_schedule_with_warmup(
        optimizer=optimizer,
        num_warmup_steps=config['warmup_steps'],
        num_training_steps=config['epoch'] * len(trainloader))
    # evaluation
    best_acc = -1
    for epoch in range(config['epoch']):
        model.train()
        epoch_loss = []
        epoch_acc = []
        for i, batch in enumerate(tqdm(trainloader)):
            # training
            mels, labels = batch
            mels = mels.to(device)
            labels = labels.to(device)
            out = model(mels)
            loss = criterion(out, labels)
            pred = out.argmax(1)
            accuracy = torch.mean((pred == labels).float())
            # update
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            scheduler.step()
            # update log
            loss = loss.item()
            accuracy = accuracy.item()
            epoch_loss.append(loss)
            epoch_acc.append(accuracy)
            writer.add_scalar("Loss/Train", loss,
                              int(epoch * len(trainloader) + i + 1))
            writer.add_scalar("Acc/Train", accuracy,
                              int(epoch * len(trainloader) + i + 1))
        # visualize
        train_avg_loss = sum(epoch_loss) / len(epoch_loss)
        train_avg_acc = sum(epoch_acc) / len(epoch_acc)
        print(
            f"Train | {epoch + 1} : avgLoss: {train_avg_loss}, avgAcc: {train_avg_acc}"
        )
        with open(config['log_file'], 'a') as f:
            f.writelines(
                f"Train | {epoch + 1} : avgLoss: {train_avg_loss}, avgAcc: {train_avg_acc}\r\n"
            )
        writer.add_scalar("avgLoss/Train", train_avg_loss, int(epoch + 1))
        writer.add_scalar("avgAcc/Train", train_avg_acc, int(epoch + 1))

        # valid
        model.eval()
        valid_acc = []
        valid_loss = []
        for i, batch in enumerate(tqdm(validloader)):
            with torch.no_grad():
                mels, labels = batch
                mels = mels.to(device)
                labels = labels.to(device)
                out = model(mels)
                loss = criterion(out, labels)
                pred = out.argmax(1)
                acc = torch.mean((pred == labels).float())
                loss = loss.item()
                acc = acc.item()
                valid_acc.append(acc)
                valid_loss.append(loss)
                writer.add_scalar("Loss/Valid", loss,
                                  int(epoch * len(validloader) + i + 1))
                writer.add_scalar("Acc/Valid", acc,
                                  int(epoch * len(validloader) + i + 1))
        # update log
        valid_avg_acc = sum(valid_acc) / len(valid_acc)
        valid_avg_loss = sum(valid_loss) / len(valid_loss)
        print(
            f"[valid | at epoch {epoch + 1}: avgloss: {valid_avg_loss}, avgAcc:{valid_avg_acc}"
        )
        with open(config['log_file'], 'a') as f:
            f.writelines(
                f"[valid | at epoch {epoch + 1}: avgloss: {valid_avg_loss}, avgAcc:{valid_avg_acc}\r\n"
            )
        writer.add_scalar("avgLoss/Valid", valid_avg_loss, int(epoch + 1))
        writer.add_scalar("avgAcc/Valid", valid_avg_acc, int(epoch + 1))

        # save best model
        if valid_avg_acc > best_acc:
            torch.save(model.state_dict(), config['model_path'] + "best.ckpt")
            best_acc = valid_avg_acc
            print(
                f"[valid | at epoch {epoch + 1}: avgLoss: {valid_avg_loss}, avgAcc:{valid_avg_acc}, best acc-->{best_acc}"
            )
            with open(config['log_file'], 'a') as f:
                f.writelines(
                    f"[valid | at epoch {epoch + 1}: avgLoss: {valid_avg_loss}, avgAcc:{valid_avg_acc}, best acc-->{best_acc}\r\n"
                )

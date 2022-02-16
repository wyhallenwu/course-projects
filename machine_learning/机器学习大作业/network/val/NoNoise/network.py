import torch
import torch.nn as nn
from torch.nn import functional as F
import cv2
import numpy as np
import os


def img2tensor(filename):
    # image shape: (217*181*3) = 117831
    img = cv2.imread(filename)
    # print(filename)
    # image to tensor
    image_array = np.array(img).reshape(-1, 1)
    image_tensor = torch.from_numpy(image_array.astype(np.float32))
    # print(image_tensor.shape)
    return image_tensor

class NaiveNet(nn.Module):
    def __init__(self):
        super(NaiveNet, self).__init__()
        self.layer1 = nn.Linear(1, 16)
        self.relu1 = nn.ReLU()
        self.layer2 = nn.Linear(16, 16)
        self.relu2 = nn.ReLU()
        self.layer3 = nn.Linear(16, 1)

        self.criterion = nn.MSELoss()
        self.optimizer = torch.optim.Adam(self.parameters(), lr=0.01)

    def forward(self, input_tensor):
        y = self.layer1(input_tensor)
        y = self.relu1(y)
        y = self.layer2(y)
        y = self.relu2(y)
        y = self.layer3(y)
        return y

def get_pair(index):
    gt_dir = './NoNoise/'
    lr_dir = './NoiseLevel7/'
    gt_file = gt_dir + str(index) + '.png'
    lr_file = lr_dir + str(index) + '.png'
    # print(gt_file)
    gt_tensor = img2tensor(gt_file)
    lr_tensor = img2tensor(lr_file)
    return gt_tensor, lr_tensor
    


tensor = img2tensor('./NoNoise/1.png')
model = NaiveNet()
epoch = 2000
for i in range(epoch):
    for index in range(1, 16):
        gt_tensor, lr_tensor = get_pair(index)
        # print(lr_tensor)
        pre_tensor = model(lr_tensor)
        # print(pre_tensor) nan
        loss = model.criterion(pre_tensor, gt_tensor)
        model.optimizer.zero_grad()
        loss.backward()
        model.optimizer.step()
    
    if i % 100 == 0:
        print(i,':', loss.data)
        

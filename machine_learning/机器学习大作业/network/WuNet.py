import torch
import torch.nn as nn
from torchvision import transforms
import torchvision
from PIL import Image
import numpy as np
import cv2
from sklearn.metrics import mean_squared_error
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim


class WuNet(nn.Module):
    def __init__(self):
        super(WuNet, self).__init__()
        self.block1 = nn.Sequential(
            # 256*256*1
            nn.Conv2d(1, 16, kernel_size=4, padding=0, stride=2),
            nn.ReLU(),
            # 126*126*16
            nn.AvgPool2d(kernel_size=2, stride=2),
            # 63*63*16

        )
        self.block2 = nn.Sequential(
            nn.Linear(1, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
        )
        self.block3 = nn.Sequential(
            nn.Upsample((256, 256)),
        )

        self.criterion = nn.MSELoss()
        self.optimizer = torch.optim.Adam(self.parameters(), lr=0.01)


    def forward(self, input_tensor):
        y = self.block1(input_tensor)
        # print(y.shape)
        y = y.reshape(-1, 1)
        y = self.block2(y)
        y = y.reshape(1, 1, 252, 252)
        y = self.block3(y).reshape(1, 256, 256)
        return y


def convalidate(index, save_path2):
    test_model = torch.load(save_path2+str(index)+'model.pth').cpu()
    test_model.eval()
    loss = 0
    for index in range(11, 15):
        gt_tensor, lr_tensor = get_pair_conv(index)
        pre_tensor = test_model(lr_tensor.cpu())
        loss += mean_squared_error(gt_tensor.cpu().reshape(-1, 1).numpy(), pre_tensor.detach().reshape(-1, 1).numpy())
    return loss / 4.0


# need to add (1) resize (2) reshape to meet conv2d(4 dims)
def get_pair_conv(index, gt_dir, lr_dir):
    
    gt_file = gt_dir + str(index) + '.png'
    lr_file = lr_dir + str(index) + '.png'

    transform_pil = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor()
    ])
    gt = Image.open(gt_file)
    gt_tensor = transform_pil(gt)
    # print(gt_tensor.shape)
    gt_tensor = gt_tensor.reshape(1, 1, 256, 256)
    # print(gt_tensor.shape)
    lr = Image.open(lr_file)
    lr_tensor = transform_pil(lr)
    lr_tensor = lr_tensor.reshape(1, 1, 256, 256)
    # print(lr_tensor)
    return gt_tensor, lr_tensor


def trainWuNet():
    save_path2 = './conv_models/'
    gt_dir = './NoNoise/'
    lr_dir = './NoiseLevel7/'
    epoch = 1000
    WuNet_model = WuNet()
    for i in range(epoch):
        for index in range(1, 11):
            gt_tensor, lr_tensor = get_pair_conv(index, gt_dir, lr_dir)
            pre_tensor = WuNet_model(lr_tensor)
            loss = WuNet_model.criterion(pre_tensor, gt_tensor.reshape(1, 256, 256))
            WuNet_model.optimizer.zero_grad()
            loss.backward()
            WuNet_model.optimizer.step()

        if (i+1) % 100 == 0:
            print(i+1, 'loss: ', loss.data)
        if (i+1) % 200 == 0:
            torch.save(WuNet_model, save_path2+str(i+1)+'model.pth')
            test_error = convalidate(i+1, save_path2)
            print('test error: ', test_error)
            if test_error < 0.04:
                break


def evaluate():
    path = './conv_models/'
    test_gt_dir = './test/NoNoise/'
    test_lr_dir = './test/NoiseLevel7/'
    psnr_sum = 0
    ssim_sum = 0
    test_model = torch.load(path+'1000model.pth').cpu()
    test_model.eval()
    for index in range(14, 16):
        _, lr_tensor = get_pair_conv(index, test_gt_dir, test_lr_dir)
        pre_tensor = test_model(lr_tensor.cpu())
        pre_tensor = pre_tensor.detach()
        image = torchvision.transforms.functional.to_pil_image(pre_tensor)
        image.save(test_lr_dir+str(index)+'conv.png')

        lr = cv2.imread(test_lr_dir+str(index)+'conv.png', cv2.IMREAD_GRAYSCALE)
        gt = cv2.imread(test_gt_dir+str(index)+'.png', cv2.IMREAD_GRAYSCALE)
        gt = cv2.resize(gt, 256, 256, interpolation=cv2.INTER_NEAREST)

        psnr_sum += psnr(gt, lr)
        ssim_sum += ssim(gt, lr, win_size=3)
    
    print('psnr: ', psnr_sum / 2)
    print('ssim: ', ssim_sum / 2)


# trainWuNet()
evaluate()
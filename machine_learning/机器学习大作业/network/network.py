from pickletools import uint8
from cv2 import imread
import torch
import torch.nn as nn
from torch.nn import functional as F
import cv2
import numpy as np
from sklearn.metrics import mean_squared_error
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim

log_path = './'
save_path = './save_models/'

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
    gt_tensor = img2tensor(gt_file).to(device)
    lr_tensor = img2tensor(lr_file).to(device)
    return gt_tensor, lr_tensor


def validate(index):
    test_model = torch.load(save_path+str(index)+'model.pth').cpu()
    test_model.eval()
    loss = 0
    for index in range(11, 14):
        gt_tensor, lr_tensor = get_pair(index)
        pre_tensor = test_model(lr_tensor.cpu())
        loss += mean_squared_error(gt_tensor.cpu().numpy(), pre_tensor.detach().numpy())
    return loss / 4


def evaluate():
    gt_path = './test/NoNoise/'
    lr_path = './test/NoiseLevel7/'
    psnr_sum = 0
    ssim_sum = 0
    test_model = torch.load('./save_models/20000model.pth').cpu()
    test_model.eval()
    for i in range(14, 16):
        gt = cv2.imread(gt_path+str(i)+'.png')
        lr_tensor = img2tensor(lr_path+str(i)+'.png')
        pre_tensor = test_model(lr_tensor.cpu())
        pre_array = pre_tensor.detach().numpy()
        lr = pre_array.reshape(217, 181, 3)
        cv2.imwrite(lr_path+'lr_array20000.png', lr)
        lr = cv2.imread(lr_path+'lr_array20000.png')
        # lr = cv2.fromarray(pre_array)
        psnr_sum += psnr(gt, lr)
        ssim_sum += ssim(gt, lr, win_size=3)

    print('psnr: ', psnr_sum / 2)
    print('ssim: ', ssim_sum / 2)


def trainNaiveNet():
    epoch = 20000
    for i in range(epoch):
        for index in range(1, 11):
            gt_tensor, lr_tensor = get_pair(index)
            # print(lr_tensor)
            pre_tensor = model(lr_tensor)
            # print(pre_tensor) nan
            loss = model.criterion(pre_tensor, gt_tensor)
            model.optimizer.zero_grad()
            loss.backward()
            model.optimizer.step()
        
        if (i+1) % 100 == 0:
            print(i+1,':', loss.data)
            if (i+1) % 200 == 0:
                torch.save(model, save_path+str(i+1)+'model.pth')
                test_error = validate(i+1)
                print('test mse: ', test_error)
                if test_error < 10:
                    break


if __name__ == '__main__':
    # cuda
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = NaiveNet().cuda()
    trainNaiveNet()
    evaluate()
        

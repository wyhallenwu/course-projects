from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim
import cv2
import torch
import numpy as np



test_model = torch.load('./save_models/2000model.pth')
test_model.eval()

def img2tensor(filename):
    # image shape: (217*181*3) = 117831
    img = cv2.imread(filename)
    image_array = np.array(img).reshape(-1, 1)
    image_tensor = torch.from_numpy(image_array.astype(np.float32))
    return image_tensor

def evaluate():
    gt_path = './test/NoNoise/'
    lr_path = './test/NoiseLevel7/'
    psnr_sum = 0
    ssim_sum = 0
    for i in range(14, 16):
        gt = cv2.imread(gt_path+str(i)+'.png')
        lr_tensor = img2tensor(lr_path+str(i)+'.png')
        pre_tensor = test_model(lr_tensor)
        pre_array = pre_tensor.detach().numpy()
        pre_array = pre_array.reshape(217, 181, 3)
        lr = cv2.fromarray(pre_array)
        psnr_sum += psnr(gt, lr)
        ssim_sum += ssim(gt, lr)

    print(psnr_sum / 2, ssim_sum / 2)
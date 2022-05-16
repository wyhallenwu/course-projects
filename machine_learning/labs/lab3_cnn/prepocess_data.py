import os
from torch.utils.data import Dataset, ConcatDataset, SubsetRandomSampler
from PIL import Image
import torchvision.transforms as transforms
import numpy as np
import utils
from sklearn.model_selection import KFold

"""adding mix-up in this file"""

config = utils.read_config('./config.yml')

# data augmentation for training and testing
test_tfm = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor()]
)

train_tfm = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.autoaugment.AutoAugment(),
    transforms.ToTensor()]
)


def mix_up(image1, image2):
    """mixup data augmentation."""
    # alpha = np.random.beta(1, 1)
    alpha = config['alpha']
    return alpha * image1 + (1 - alpha) * image2


class FoodDataset(Dataset):
    def __init__(self, path, tfm=test_tfm, train_flag=False, files=None):
        super(FoodDataset, self).__init__()
        self.path = path
        self.files = sorted([os.path.join(path, x)
                            for x in os.listdir(path) if x.endswith('.jpg')])
        if files is not None:
            self.files = files
        self.transform = tfm
        self.train_flag = train_flag

    def __len__(self):
        return len(self.files)

    def __getitem__(self, index):
        filename1 = self.files[index]
        im1 = Image.open(filename1)
        # mixup training
        if config['mixup'] and self.train_flag:
            im1 = test_tfm(im1)
            idx1 = int(filename1.split("/")[-1].split("_")[0])
            index2 = np.random.randint(len(self))
            filename2 = self.files[index2]
            idx2 = int(filename2.split("/")[-1].split("_")[0])
            im2 = Image.open(filename2)
            im2 = test_tfm(im2)
            # mixup
            im = mix_up(im1, im2)
            return im, idx1, idx2
        # train without mixup
        elif self.train_flag:
            im1 = self.transform(im1)
            idx = int(filename1.split("/")[-1].split("_")[0])
            return im1, idx
        # test
        else:
            im1 = self.transform(im1)
            return im1, -1

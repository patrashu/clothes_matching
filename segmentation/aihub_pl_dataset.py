import os
import cv2
import numpy as np
from PIL import Image
from glob import glob

import torch
from torch.utils.data import Dataset
import torchvision
from torchvision.transforms import Compose, Normalize
import matplotlib.pyplot as plt
import torchvision.transforms.functional as F


class CustomToTensor(object):
    def __call__(self, data):
        labels, images = data['labels'], data['images']
        images = images.transpose((2, 0, 1)).astype(np.float32)
        labels = labels.transpose((2, 0, 1)).astype(np.float32)
        data = {'labels': torch.from_numpy(labels), 'images': torch.from_numpy(images)}
        return data
    
    def __init__(self, mean=0.5, std=0.5):
        self.mean = mean
        self.std = std


class Normalization:

    def __call__(self, data):
        labels, images = data['labels'], data['images']
        images = images / 255
        images = (images - 0.5) / 0.5
        data = {'labels': labels, 'images': images}
        return data
    

class RandomFlip(object):
    def __call__(self, data):
        labels, images = data['labels'], data['images']
        if np.random.rand() > 0.5:
            labels = np.fliplr(labels)
            images = np.fliplr(images)

        if np.random.rand() > 0.5:
            labels = np.flipud(labels)
            images = np.flipud(images)

        data = {'labels': labels, 'images': images}

        return data
    

class CustomFashionDataset(Dataset):
    def __init__(self, root="", transform=None):
        super().__init__()
        self.root = root
        self.imgs = sorted(glob(os.path.join(root, "images", "*")))
        self.masks = sorted(glob(os.path.join(root, "labels", "*")))
        self.transform = transform

    def __getitem__(self, idx):
        img = cv2.imread(self.imgs[idx])
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mask = Image.open(self.masks[idx])

        img = cv2.resize(img, (640, 640))
        mask = cv2.resize(np.array(mask), (640, 640))

        data = {"images": img, "labels": mask}
        if self.transform is not None:
            data = self.transform(data)      
        return data    

    def __len__(self):
        return len(self.imgs)
    

def show(imgs):
    fig, axs = plt.subplots(ncols=len(imgs), squeeze=False)
    for i, img in enumerate(imgs):
        img = img.detach()
        img = F.to_pil_image(img)
        axs[0, i].imshow(np.asarray(img))
        
    plt.savefig("result.jpg")


if __name__ == '__main__':
    transform = Compose([
        CustomToTensor(),
    ])

    train_dataset = CustomFashionDataset(root="dataset/valid", transform=transform)
    data = next(iter(train_dataset))
    mask_grid = torchvision.utils.make_grid(data["labels"])
    show(mask_grid)
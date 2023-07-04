import os
import cv2
import torch
import random
import shutil
import numpy as np
from glob import glob
from PIL import Image
from torchvision.transforms import Compose, Resize, Normalize, ToTensor
from aihub_pl_train import CustomFashionLightningModel


def inference() -> None:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    img = Image.open(img_path).convert("RGB")
    h, w = img.size
    print(h, w)
    img = transform(img)
    img = img.unsqueeze(0)
    img = img.to(device)

    with torch.no_grad():
        model.to(device)
        model.eval()        
        pred_mask = model(img)
        pred_mask = torch.sigmoid(pred_mask)
        pred_mask = pred_mask > 0.5
        pred_mask = pred_mask.detach().cpu().numpy().squeeze()

        cv2.imwrite(f"{img_path}_class1.jpg", pred_mask[0, :, :]*128)
        cv2.imwrite(f"{img_path}_class2.jpg", pred_mask[1, :, :]*128)
        cv2.imwrite(f"{img_path}_class3.jpg", pred_mask[2, :, :]*128)
        cv2.imwrite(f"{img_path}_class4.jpg", pred_mask[3, :, :]*128)


if __name__ == '__main__':
    data_path = "dataset/valid/"
    decode_model = "DeepLabV3Plus"
    encode_model = "resnet101"
    ckpt = "model/model.ckpt"
    img_path = "model1.jpg"
    label_path =os.path.join('/'.join(img_path.split('/')[:-2]), "labels", f"{img_path.split('/')[-1][:-4]}.jpg")

    model = CustomFashionLightningModel.load_from_checkpoint(
        arch=decode_model,
        encoder_name=encode_model,
        in_channels=3,
        out_classes=4,
        checkpoint_path=ckpt
    )
    transform = Compose([
        Resize((640, 640)),
        ToTensor(),
        Normalize(mean=0.5, std=0.5)
    ])
    inference()
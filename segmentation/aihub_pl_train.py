import os
import cv2
import torch
import wandb
import numpy as np
import matplotlib.pyplot as plt
import pytorch_lightning as pl
import segmentation_models_pytorch as smp
from torch.utils.data import DataLoader
from pytorch_lightning.callbacks import ModelCheckpoint
from pytorch_lightning.loggers import WandbLogger
from aihub_pl_dataset import CustomFashionDataset, Normalization, RandomFlip, CustomToTensor
from torchvision.transforms import Compose
import torchvision


class CustomFashionLightningModel(pl.LightningModule):
    def __init__(self, arch, encoder_name, in_channels, out_classes, **kwargs):
        super().__init__()
        self.model = smp.create_model(
            arch, encoder_name=encoder_name, in_channels=in_channels, classes=out_classes, **kwargs
        )
        self.loss_fn2 = smp.losses.DiceLoss(mode="multilabel", classes=out_classes)

    def forward(self, x):
        return self.model(x)
    
    def training_step(self, batch, idx):
        image = batch["images"]
        mask = batch["labels"]
        pred_mask = self.forward(image)
        loss = self.loss_fn2(pred_mask, mask)

        tp, fp, fn, tn = smp.metrics.get_stats(pred_mask.long(), mask.long(), mode="multilabel")
        diou = smp.metrics.iou_score(tp, fp, fn, tn, reduction="micro-imagewise")
        piou = smp.metrics.iou_score(tp, fp, fn, tn, reduction="micro")
        self.log("loss", loss, on_step=True, on_epoch=True, prog_bar=True, logger=True)
        self.log("diou", diou, on_step=True, on_epoch=True, prog_bar=True, logger=True)
        self.log("piou", piou, on_step=True, on_epoch=True, prog_bar=True, logger=True)

        if idx % 40 == 0:
            images, masks = batch["images"][0], batch["labels"][0]
            image = images.detach().cpu().numpy()
            image = image.transpose(1, 2, 0)
            mask = masks.detach().cpu().numpy()
            mask = mask.transpose(1, 2, 0)

            self.logger.experiment.log({
                'rgb': wandb.Image(image, caption='Input-image'),
                'shirt-long-mask': wandb.Image(mask[:, :, 0], caption='shirt-long-mask'),
                'shirt-short-mask': wandb.Image(mask[:, :, 1], caption='shirt-short-mask'),
                'skirt-mask': wandb.Image(mask[:, :, 2], caption='skirt-mask'),
                'pants-mask': wandb.Image(mask[:, :, 3], caption='pants-mask'),
            })

        return loss
    
    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), 0.001)
    

if __name__ == '__main__':
    data_path = "dataset/valid/"
    decode_model = "DeepLabV3Plus"
    encode_model = "resnet101"

    checkpoint_callback = ModelCheckpoint(
        dirpath="model/", 
        save_top_k=-1, 
        monitor="diou",
        mode='max',
        filename="{epoch}_{loss:3f}_{piou:2f}_{diou:2f}"
    )
    wandb_logger = WandbLogger(project="fashion_seg")

    transform = Compose([
        Normalization(),
        RandomFlip(),
        CustomToTensor(),
    ])

    train_dataset = CustomFashionDataset(root=data_path, transform=transform)
    train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True, num_workers=16)

    model = CustomFashionLightningModel(
        decode_model, 
        encode_model, 
        in_channels=3,
        out_classes=4,
        activation="sigmoid"
    )

    trainer = pl.Trainer(
        accelerator="gpu",
        strategy="ddp",
        devices=[0, 1, 2, 3],
        max_epochs=50,
        callbacks=checkpoint_callback, 
        precision="16-mixed",
        logger=wandb_logger
    )

    trainer.fit(model, train_loader)
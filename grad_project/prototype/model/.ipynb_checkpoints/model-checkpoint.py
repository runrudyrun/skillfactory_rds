import torch
from torch import nn
import torch.nn.functional as F
from torch.nn.modules.padding import ReplicationPad2d
from model.siamese import *
import pytorch_lightning as pl
import numpy as np
import segmentation_models_pytorch as smp
    
class LitModel(pl.LightningModule):
    def __init__(self):
        super().__init__()
        # self.model = SiamUnet_diff(3,1)
        self.model = smp.Unet('vgg16', encoder_weights = 'imagenet', in_channels=6, activation='sigmoid')
 

    def forward(self, x):
        x = self.model(x)
        # x = self.model(x[0],x[1])
        return x
    
class Predictor():

    def __init__(self, mode):
        self.model = LitModel().load_from_checkpoint('./model/checkpoint/last.ckpt')
        self.device = 'cpu'
        self.mode = mode
    
    def __call__(self, inputs):
        outs = np.squeeze(self.model(inputs).detach().numpy().astype('float32'))
        if self.mode == 'float':
            return outs
        elif self.mode == 'binary':
            return np.rint(outs)
        else:
            pass
    
    
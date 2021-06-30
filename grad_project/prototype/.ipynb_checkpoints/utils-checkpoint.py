import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from skimage import io
from pathlib import Path
import pathlib
import torch
import albumentations as A
from PIL import Image

def get_random_chip_pair(df, DATA_DIR):
    n=np.random.randint(len(df)-1)
    row = df.iloc[n]
    chip = io.imread(DATA_DIR + row.chip_path).astype('uint8')
    mask = np.divide(io.imread(DATA_DIR + row.mask_path),255).astype('float32')
    im1, im2 = chip[:,:,:3], chip[:,:,3:]
    return im1, im2, mask

def encode(im1,im2, siamese = False):
    """Encoder to feed images to NN"""
    trf = A.Compose([A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)), A.PadIfNeeded(64,64)])
    im1 = trf(image = im1)['image']
    im2 = trf(image = im2)['image']
    if siamese == False:
        chip = np.concatenate((im1,im2),axis = -1)
        image = torch.Tensor(np.moveaxis(chip, 2, 0))
        return image.unsqueeze(0)
    else:
        im1 = torch.Tensor(np.moveaxis(im1,2,0)).unsqueeze(0)
        im2 = torch.Tensor(np.moveaxis(im2,2,0)).unsqueeze(0)
        return im1,im2
    
def iou(pr, gt, eps=1e-7):
    """Functional Intersection over Union implementation"""
    intersection = np.sum(gt * pr)
    union = np.sum(gt) + np.sum(pr) - intersection + eps
    return (intersection + eps) / union



class ChipCreator():
    """Class that allows us to split bigger satellite picture and mask into smaller pieces"""
    
    def __init__(self, dimension, is_raster = False):
        self.dimension = dimension
        self.raster = is_raster
        
    def __read_image(self,image):
        # checks whether image is a path or array
        if isinstance(image,(pathlib.PurePath,str)):
                with Image.open(image) as img:
                    # converts image into np array
                    np_array = np.array(img)
                return np_array
            
        elif isinstance(image,np.ndarray):
            return image
        else:
            raise ValueError(f"Expected Path or Numpy array received: {type(image)}")
        
    def make_chips(self, image):
        
        #getting image and converting to np.array if necessary
        np_array = self.__read_image(image)
        
        # then get numbers of chips per row and column
        n_rows = (np_array.shape[0] - 1) // self.dimension + 1
        n_cols = (np_array.shape[1] - 1) // self.dimension + 1
        
        chip_list = [] #
        for r in range(n_rows):
            for c in range(n_cols):
                #starting row and column
                start_r_idx = r*self.dimension
                end_r_idx = start_r_idx + self.dimension
                #ending row and column
                start_c_idx = c*self.dimension
                end_c_idx = start_c_idx + self.dimension
                #cutting fragment by indexes
                chip = np_array[start_r_idx:end_r_idx,start_c_idx:end_c_idx]
                
                if self.raster:
                    # if raster is True then format is (channels, rows, columns)
                    # else (rows, columns, channels)
                    chip = np.moveaxis(chip,-1,0)

                chip_list.append(chip)

        return np.array(chip_list)
    def __call__(self, image):
        # slightly different verison of make_chips
        np_array = self.__read_image(image)
        n_rows = (np_array.shape[1] - 1) // self.dimension + 1
        n_cols = (np_array.shape[2] - 1) // self.dimension + 1
        chip_dict = {'chip':[],'x':[],'y':[], 'blank':[]}
        for r in range(n_rows):
            for c in range(n_cols):
                start_r_idx = r*self.dimension
                end_r_idx = start_r_idx + self.dimension

                start_c_idx = c*self.dimension
                end_c_idx = start_c_idx + self.dimension
                chip = np_array[:,start_r_idx:end_r_idx,start_c_idx:end_c_idx]

                chip_dict['chip'].append(chip)
                chip_dict['x'].append(start_r_idx)
                chip_dict['y'].append(start_c_idx)
                if chip.mean() == 0 and chip.sum() == 0:
                    chip_dict['blank'].append('_blank')
                else:
                    chip_dict['blank'].append('')
        return chip_dict
    
def plot_many(pictures, ncols = 4, dpi = 300, is_raster = False):
    matplotlib.rcParams['figure.dpi'] = dpi
    nrows = (len(pictures) - 1) // ncols + 1
    
    fig,axs = plt.subplots(nrows,ncols,figsize=(10,10))
    fig.tight_layout()
    
     
    for r,ax in enumerate(axs):
        for c,row in enumerate(ax):
            # i is current index in array of axes
            i = r*ncols + c
            ax[c].set_title(i)
            image = pictures[i]
            # unmaking raster format if necessary
            if is_raster:
                image = np.moveaxis(image,0,-1)
            ax[c].imshow(image);
    
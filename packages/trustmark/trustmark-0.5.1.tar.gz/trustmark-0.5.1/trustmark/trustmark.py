# Copyright 2022 Adobe
# All Rights Reserved.

# NOTICE: Adobe permits you to use, modify, and distribute this file in
# accordance with the terms of the Adobe license agreement accompanying
# it.

from __future__ import absolute_import

import torch
import os
import pathlib
import re
import time
import importlib

from omegaconf import OmegaConf
from .ecc import BCH
from PIL import Image
from torchvision import transforms
import numpy as np
import urllib.request

MODEL_REMOTE_HOST = "https://cc-assets.netlify.app/watermarking/trustmark-models/"

class TrustMark():

    class Encoding:
       Default=0
       BCH_2=4
       BCH_3=3
       BCH_4=2
       BCH_5=1

    def __init__(self, use_ECC=True, verbose=True, secret_len=100, device='', model_type='Q', encoding_type=Encoding.Default):
        """ Initializes the TrustMark watermark encoder/decoder/remover module

        Parameters (default listed first)
        ---------------------------------

        use_ECC : bool
            [True] will use BCH error correction on the payload, reducing payload size (default)
            [False] will disable error correction, increasing payload size
        verbose : bool
            [True] will output status messages during use (default)
            [False] will run silent except for error messages
        """

        super(TrustMark, self).__init__()

        if not device:
            self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        else:
            self.device = device

        if(verbose):
            print('Initializing TrustMark watermarking %s ECC using [%s]' % ('with' if use_ECC else 'without',self.device))

        # the location of three models
        assert model_type in ['C', 'Q', 'B']
        self.model_type = model_type


        locations={'config' : os.path.join(pathlib.Path(__file__).parent.resolve(),f'models/trustmark_{self.model_type}.yaml'), 
                   'config-rm' : os.path.join(pathlib.Path(__file__).parent.resolve(),f'models/trustmark_rm_{self.model_type}.yaml'), 
                   'decoder': os.path.join(pathlib.Path(__file__).parent.resolve(),f'models/decoder_{self.model_type}.ckpt'), 
                   'remover': os.path.join(pathlib.Path(__file__).parent.resolve(),f'models/trustmark_rm_{self.model_type}.ckpt'),
                   'encoder': os.path.join(pathlib.Path(__file__).parent.resolve(),f'models/encoder_{self.model_type}.ckpt')}

        self.use_ECC=use_ECC
        self.secret_len=secret_len
        self.ecc = BCH(secret_len, verbose=verbose, encoding_mode=encoding_type)
        
        self.decoder = self.load_model(locations['config'], locations['decoder'], self.device, secret_len, part='decoder')
        self.encoder = self.load_model(locations['config'], locations['encoder'], self.device, secret_len, part='encoder')
        self.removal = self.load_model(locations['config-rm'], locations['remover'], self.device, secret_len, part='remover')

    def check_and_download(self, filename):
        if not os.path.isfile(filename):
            print('Fetching model file (once only): '+filename)
            urld=MODEL_REMOTE_HOST+os.path.basename(filename)
            print('Fetching from '+urld)
            urllib.request.urlretrieve(urld,filename)

    def load_model(self, config_path, weight_path, device, secret_len, part='all'):
        assert part in ['all', 'encoder', 'decoder', 'remover']
        self.check_and_download(config_path)
        self.check_and_download(weight_path)
        config = OmegaConf.load(config_path).model
        if part == 'encoder':
            # replace all other components with identity
            config.params.secret_decoder_config.target = 'trustmark.model.Identity'
            config.params.discriminator_config.target = 'trustmark.model.Identity'
            config.params.loss_config.target = 'trustmark.model.Identity'
            config.params.noise_config.target = 'trustmark.model.Identity'
        elif part == 'decoder':
            # replace all other components with identity
            config.params.secret_encoder_config.target = 'trustmark.model.Identity'
            config.params.discriminator_config.target = 'trustmark.model.Identity'
            config.params.loss_config.target = 'trustmark.model.Identity'
            config.params.noise_config.target = 'trustmark.model.Identity'

        elif part == 'remover':
            config.params.is_train = False  # inference mode, only load denoise module
    
        model = instantiate_from_config(config)
        state_dict = torch.load(weight_path, map_location=torch.device('cpu'))
        
        if 'global_step' in state_dict:
            print(f'Global step: {state_dict["global_step"]}, epoch: {state_dict["epoch"]}')
        if 'state_dict' in state_dict:
            state_dict = state_dict['state_dict']
            
        misses, ignores = model.load_state_dict(state_dict, strict=False)
        model = model.to(device)
        model.eval()

        return model


    def decode(self, stego_image):
        # Inputs
        # stego_image: PIL image
        # Outputs: secret numpy array (1, secret_len)
        if min(stego_image.size) > 256:
            stego_image = stego_image.resize((256,256), Image.BILINEAR)
        stego = transforms.ToTensor()(stego_image).unsqueeze(0).to(self.decoder.device) * 2.0 - 1.0 # (1,3,256,256) in range [-1, 1]
        with torch.no_grad():
            secret_pred = (self.decoder.decoder(stego) > 0).cpu().numpy()  # (1, secret_len)
        if self.use_ECC:
            secret_pred, detected, version = self.ecc.decode_text(secret_pred)[0]
            return secret_pred, detected, version
        else:
            return secret_pred, True, version
    
    def encode(self, cover_image, string_secret, WM_STRENGTH=0.9, WM_MERGE='bilinear'):
        # Inputs
        #   cover_image: PIL image
        #   secret_tensor: (1, secret_len)
        # Outputs: stego image (PIL image)
        
        # secrets
        secret = self.ecc.encode_text([string_secret])
        secret = torch.from_numpy(secret).float().to(self.device)
        
        
        w, h = cover_image.size
        cover = cover_image.resize((256,256), Image.BILINEAR)
        tic=time.time()
        cover = transforms.ToTensor()(cover).unsqueeze(0).to(self.encoder.device) * 2.0 - 1.0 # (1,3,256,256) in range [-1, 1]
#        toc=time.time()
#        print('CPU->GPU %f ms ' % ((toc-tic)*1000))
        with torch.no_grad():
#            tic=time.time()
            stego, _ = self.encoder(cover, secret)
#            toc=time.time()
#            print('ML Inference %f ms' % ((toc-tic)*1000))
            residual = stego.clamp(-1, 1) - cover
            residual = torch.nn.functional.interpolate(residual, size=(h, w), mode=WM_MERGE)
#            residual = torch.nn.functional.interpolate(residual, size=(int(h/4), int(w/4)), mode='bicubic')
#            residual = torch.nn.functional.interpolate(residual, size=(int(h/2), int(w/2)), mode='bicubic')
#            residual = torch.nn.functional.interpolate(residual, size=(h, w), mode='bicubic')
#            tic=time.time()
            residual = residual.permute(0,2,3,1).cpu().numpy().astype('f4')  # (1,256,256,3)
#            toc=time.time()
#            print('GPU->CPU %f ms ' % ((toc-tic)*1000))
#            tic=time.time()
            stego = np.clip(residual[0]*WM_STRENGTH + np.array(cover_image)/127.5-1., -1, 1)*127.5+127.5  # (256, 256, 3), ndarray, uint8
#            toc=time.time()
#            print('Apply residual %f ms' % ((toc-tic)*1000))
            
        return Image.fromarray(stego.astype(np.uint8))

    @torch.no_grad()
    def remove_watermark(self, stego):
        """Remove watermark from stego image"""
        W, H = stego.size
        stego256 = stego.resize((256,256), Image.BILINEAR)
        stego256 = transforms.ToTensor()(stego256).unsqueeze(0).to(self.removal.device) * 2.0 - 1.0 # (1,3,256,256) in range [-1, 1]
        img256 = self.removal(stego256).clamp(-1, 1)
        res = img256 - stego256
        res = torch.nn.functional.interpolate(res, (H,W), mode='bilinear').permute(0,2,3,1).cpu().numpy()   # (B,3,H,W) no need antialias since this op is mostly upsampling
        out = np.clip(res[0] + np.asarray(stego)/127.5-1., -1, 1)*127.5+127.5  # (256, 256, 3), ndarray, uint8
        return Image.fromarray(out.astype(np.uint8))



def get_obj_from_str(string, reload=False):
    module, cls = string.rsplit(".", 1)
    if reload:
        module_imp = importlib.import_module(module)
        importlib.reload(module_imp)
    return getattr(importlib.import_module(module, package=None), cls)



def instantiate_from_config(config):
    if not "target" in config:
        if config == '__is_first_stage__':
            return None   
        elif config == "__is_unconditional__":
            return None
        raise KeyError("Expected key `target` to instantiate.")
    return get_obj_from_str(config["target"])(**config.get("params", dict()))
  



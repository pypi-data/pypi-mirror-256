import os
import numpy as np
import torch
from config import parse_args
from utils import init_seeds, setting_lr_parameters


def main_single(device,gpu,seed,input_size,batch_size,lr,meta_epochs,sub_epochs,train_list,val_list,save_model_path):
    
    init_seeds(seed)
    args = parse_args()
    if device == 'GPU':
        os.environ['CUDA_VISIBLE_DEVICES'] = gpu
        args.device = torch.device("cuda")
    else:
        args.device = torch.device("cpu")
    # model path
    # args.model_path = "{}_{}_{}_{}".format(
    #     args.dataset, args.backbone_arch, args.flow_arch, args.class_name)
    args.model_path = save_model_path
    # image
    args.img_size = (input_size, input_size)  
    args.crop_size = (input_size, input_size)  
    args.norm_mean, args.norm_std = [0.485, 0.456, 0.406], [0.229, 0.224, 0.225]
    
    args.img_dims = [3] + list(args.img_size)
    # params
    args.batch_size = batch_size
    args.lr = lr
    args.meta_epochs = meta_epochs
    args.sub_epochs = sub_epochs


    # output settings
    args.save_results = True
    # unsup-train lr settings
    setting_lr_parameters(args)
    
    ############################################################################################################################################################
    # set data
    args.train_list = train_list
    args.val_list = val_list
    ############################################################################################################################################################

    # selecting train functions
    if args.with_fas:
        from bgad_fas_train_engine import train
        img_auc, pix_auc = train(args)
    else:
        from bgad_train_engine import train
        img_auc, pix_auc = train(args)

    return img_auc, pix_auc



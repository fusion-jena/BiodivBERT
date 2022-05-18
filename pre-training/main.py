from train import  run as train
from quick_test import run as quick_test
import util_log
util_log.init()
from util_log import log
import os
from cuda_props import  get_gpu_info
import torch

if __name__ == '__main__':
    # disable CUDA and GPUs this will let torch to run on CPU?
    # os.environ["CUDA_VISIBLE_DEVICES"] = ""
    try:
        torch.cuda.empty_cache()
        del variables
        gc.collect()
    except Exception as e:
        pass

    get_gpu_info()

    if torch.cuda.is_available():
        log.info("Cuda is avaiable")
    else:
        log.info("No Cuda is available")
        # exit("No CUDA is available")
    train()
    quick_test()

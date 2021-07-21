from __future__ import print_function

from miscc.config import cfg, cfg_from_file
from datasets import TextDataset
from trainer import condGANTrainer as trainer

import os
import sys
import time
import random
import pprint
import datetime
import dateutil.tz
import argparse
import numpy as np

import torch
import torchvision.transforms as transforms
import shutil


    """
    Author: DHEERAJ PERUMANDLA
    Date: 21-04-2021
    
    """

dir_path = (os.path.abspath(os.path.join(os.path.realpath(__file__), './.')))
sys.path.append(dir_path)


def parse_args():
    parser = argparse.ArgumentParser(description='Train a AttnGAN network')
    parser.add_argument('--cfg', dest='cfg_file',
                        help='optional config file',
                        default='D:\\AttnGAN\\AttnGAN-Py3\\AttnGAN\\code\\cfg\\eval_bird_attnDCGAN2.yml', type=str) #default='cfg/bird_attn2.yml'
    parser.add_argument('--gpu', dest='gpu_id', type=int, default=0) #default=-1
    parser.add_argument('--data_dir', dest='data_dir', type=str, default='')
    parser.add_argument('--manualSeed', type=int, help='manual seed', default=10)
    args = parser.parse_args()
    return args


def gen_example(wordtoix, algo, text, iterator):
    '''generate images from example sentences'''
    from nltk.tokenize import RegexpTokenizer
    #filepath = '%s/example_filenames.txt' % (cfg.DATA_DIR)
    print('in gen_example---------------')
    directory = 'D:\\AttnGAN\\AttnGAN-Py3\\AttnGAN\\models\\bird_AttnDCGAN2\\from_text'
    if (os.path.exists(directory)):
        for f in os.listdir(directory):
            os.remove(os.path.join(directory, f))
        print('rm dir')
    else:
        print('no rm dir')
    data_dic = {}
    text = text
    iterator = iterator
    sentences = text.split('\n')
    for ind in range(1, iterator+1):
        #sentences = text.split('\n')
        # a list of indices for a sentence
        if sentences[0] == 'end':
            print("*******Program Ended*******")
            break
        captions = []
        cap_lens = []
        for sent in sentences:
            if len(sent) == 0:
                continue
            sent = sent.replace("\ufffd\ufffd", " ")
            tokenizer = RegexpTokenizer(r'\w+')
            tokens = tokenizer.tokenize(sent.lower())
            if len(tokens) == 0:
                #print('sent', sent)
                continue
            rev = []
            for t in tokens:
                t = t.encode('ascii', 'ignore').decode('ascii')
                if len(t) > 0 and t in wordtoix:
                    rev.append(wordtoix[t])
            captions.append(rev)
            cap_lens.append(len(rev))
        max_len = np.max(cap_lens)
        sorted_indices = np.argsort(cap_lens)[::-1]
        cap_lens = np.asarray(cap_lens)
        cap_lens = cap_lens[sorted_indices]
        cap_array = np.zeros((len(captions), max_len), dtype='int64')
        for i in range(len(captions)):
            idx = sorted_indices[i]
            cap = captions[idx]
            c_len = len(cap)
            cap_array[i, :c_len] = cap
        key = 'from_text'
        data_dic[key] = [cap_array, cap_lens, sorted_indices]
        print(ind)
        te = sentences[0].replace(' ', '_')
        algo.gen_example(data_dic, ind, te)
        


def main(text, iterator):
    args = parse_args()
    print('In main--------')
    if args.cfg_file is not None:
        cfg_from_file(args.cfg_file)

    if args.gpu_id != -1:
        cfg.GPU_ID = args.gpu_id
    else:
        cfg.CUDA = False

    if args.data_dir != '':
        cfg.DATA_DIR = args.data_dir
    print('Using config:')
    pprint.pprint(cfg)

    if not cfg.TRAIN.FLAG:
        args.manualSeed = 100
    elif args.manualSeed is None:
        args.manualSeed = random.randint(1, 10000)
    random.seed(args.manualSeed)
    np.random.seed(args.manualSeed)
    torch.manual_seed(args.manualSeed)
    if cfg.CUDA:
        torch.cuda.manual_seed_all(args.manualSeed)

    now = datetime.datetime.now(dateutil.tz.tzlocal())
    timestamp = now.strftime('%Y_%m_%d_%H_%M_%S')
    output_dir = '../output/%s_%s_%s' % \
        (cfg.DATASET_NAME, cfg.CONFIG_NAME, timestamp)

    split_dir, bshuffle = 'train', True
    if not cfg.TRAIN.FLAG:
        # bshuffle = False
        split_dir = 'test'

    # Get data loader
    imsize = cfg.TREE.BASE_SIZE * (2 ** (cfg.TREE.BRANCH_NUM - 1))
    image_transform = transforms.Compose([
        transforms.Resize(int(imsize * 76 / 64)),
        transforms.RandomCrop(imsize),
        transforms.RandomHorizontalFlip()])
    dataset = TextDataset(cfg.DATA_DIR, split_dir,
                          base_size=cfg.TREE.BASE_SIZE,
                          transform=image_transform)
    assert dataset
    dataloader = torch.utils.data.DataLoader(
        dataset, batch_size=cfg.TRAIN.BATCH_SIZE,
        drop_last=True, shuffle=bshuffle, num_workers=int(cfg.WORKERS))

    # Define models and go to train/evaluate
    algo = trainer(output_dir, dataloader, dataset.n_words, dataset.ixtoword)

    #start_t = time.time()
    if cfg.TRAIN.FLAG:
        algo.train()
    else:
        '''generate images from pre-extracted embeddings'''
        if cfg.B_VALIDATION:
            algo.sampling(split_dir)  # generate images for the whole valid dataset
        else:
            try:
                text = text
                iterator = iterator
                print(text, iterator)
                gen_example(dataset.wordtoix, algo, text, iterator)  # generate images for customized captions
                #print("333333333333333333333333")
                time.sleep(10)
                return True
            except:
                print("444444444444444444")
                return False
    #end_t = time.time()
    #print('Total time for training:', end_t - start_t)
    return False
    


if __name__ == '__main__':
    main('this bird is black with yellow tail', 10)
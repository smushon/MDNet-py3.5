import os
import numpy as np
import pickle
from collections import OrderedDict

import platform
import sys

# seq_home = '../dataset/'
usr_home = os.path.expanduser('~')
OS = platform.system()
if OS == 'Windows':
    # usr_home = 'C:/Users/smush/'
    seq_home = os.path.join(usr_home, 'downloads','VOT')
elif OS == 'Linux':
    # usr_home = '~/'
    seq_home = os.path.join(usr_home, 'MDNet-data/VOT')
else:
    sys.exit("aa! errors!")

seqlist_path = 'data/vot-otb.txt'
output_path = 'data/vot-otb.pkl'

with open(seqlist_path,'r') as fp:
    seq_list = fp.read().splitlines()

data = {}
for i,seq in enumerate(seq_list):
    img_list = sorted([p for p in os.listdir(os.path.join(seq_home, seq)) if os.path.splitext(p)[1] == '.jpg'])
    gt = np.loadtxt(os.path.join(seq_home, seq, 'groundtruth.txt'), delimiter=',')

    assert len(img_list) == len(gt), "Lengths do not match!!"
    
    if gt.shape[1]==8:
        x_min = np.min(gt[:,[0,2,4,6]],axis=1)[:,None]
        y_min = np.min(gt[:,[1,3,5,7]],axis=1)[:,None]
        x_max = np.max(gt[:,[0,2,4,6]],axis=1)[:,None]
        y_max = np.max(gt[:,[1,3,5,7]],axis=1)[:,None]
        gt = np.concatenate((x_min, y_min, x_max-x_min, y_max-y_min),axis=1)

    data[seq] = {'images':img_list, 'gt':gt}  # data is a dictionary {e.g. 'vot2013/cup'} of dictionaries

with open(output_path, 'wb') as fp:
    pickle.dump(data, fp, -1)

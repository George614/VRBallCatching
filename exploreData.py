# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 21:22:15 2020

@author: George
"""

import pandas as pd
import numpy as np
from scipy import signal as sig

import os
import scipy.io as sio
import matplotlib.pyplot as plt

fileTimeList = ['2016-4-19-14-4', '2016-4-22-11-57', '2016-4-27-13-28', '2016-4-28-10-57', '2016-4-29-11-56',
 '2016-5-3-12-52', '2016-5-4-13-3', '2016-5-5-13-7', '2016-5-6-11-2', '2016-5-6-13-4']

# pick the last subject here
fileTime = fileTimeList[-1]

expCfgName = "gd_pilot.cfg"
sysCfgName = "PERFORMVR.cfg"

filePath = "F:/Datasets/VRBallCatching/" + fileTime + "/"
fileName = "exp_data-" + fileTime

sessionDict = pd.read_pickle(filePath + fileName + '.pickle')

rawDataFrame = sessionDict['raw']
processedDataFrame = sessionDict['processed']
calibDataFrame = sessionDict['calibration']
s1TrialInfo = sessionDict['trialInfo']


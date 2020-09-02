# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 21:22:15 2020

@author: George (Zhizhuo) Yang

This Python script read in multiple DataFrames given by Kamran and calculate
new variables in new coordinate systems for our new experiments with PC.
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

filePath = "D:/Datasets/VRBallCatching/" + fileTime + "/"
fileName = "exp_data-" + fileTime

sessionDict = pd.read_pickle(filePath + fileName + '.pickle')

rawDataFrame = sessionDict['raw']
processedDataFrame = sessionDict['processed']
calibDataFrame = sessionDict['calibration']
s1TrialInfo = sessionDict['trialInfo']
frameRate = 75

### convert gaze vector and eye-to-ball vector from Cartesian coordinates to
### spherical coordinates

# Gaze vector in HCS
rgp = processedDataFrame['rotatedGazePoint']
eih_az = np.arctan(rgp['X'] / rgp['Z']) / np.pi*180
eih_el = np.arctan(rgp['Y'] / rgp['Z']) / np.pi*180
eih_az_vel = np.asarray(eih_az[1:].values - eih_az[:-1].values) * frameRate
eih_el_vel = np.asarray(eih_el[1:].values - eih_el[:-1].values) * frameRate
eih_az_vel = np.concatenate([[0], eih_az_vel])
eih_el_vel = np.concatenate([[0], eih_el_vel])
eih = pd.DataFrame({'Az' : eih_az, 'El': eih_el}, dtype=float)
eih.columns = pd.MultiIndex.from_product([['EyeInHead'], eih.columns])
eih_vel = pd.DataFrame({'AzVel': eih_az_vel, 'ElVel': eih_el_vel},  dtype=float)
eih_vel.columns = pd.MultiIndex.from_product([['EyeInHead'], eih_vel.columns])
EIHSpherical = pd.concat([eih, eih_vel], axis=1)
EIHSpherical.boxplot(column=[['EyeInHead', 'Az'], ['EyeInHead','El']])
EIHSpherical.boxplot(column=[['EyeInHead', 'AzVel'], ['EyeInHead','ElVel']])

# Eye-to-ball vector in HCS
rbs = processedDataFrame['rotatedBallOnScreen']
bih_az = np.arctan(np.asarray(rbs['X']/rbs['Z'], dtype=float)) / np.pi * 180
bih_el = np.arctan(np.asarray(rbs['Y']/rbs['Z'], dtype=float)) / np.pi * 180
bih_az_vel = np.asarray(bih_az[1:] - bih_az[:-1]) * frameRate
bih_el_vel = np.asarray(bih_el[1:] - bih_el[:-1]) * frameRate
bih_az_vel = np.concatenate([[0], bih_az_vel])
bih_el_vel = np.concatenate([[0], bih_el_vel])
bih = pd.DataFrame({'Az' : bih_az, 'El': bih_el}, dtype=float)
columns = [('BallInHead', 'Az'), ('BallInHead', 'El')]
bih.columns = pd.MultiIndex.from_tuples(columns)
bih_vel = pd.DataFrame({'AzVel': bih_az_vel, 'ElVel': bih_el_vel},  dtype=float)
bih_vel.columns = pd.MultiIndex.from_product([['BallInHead'], bih_vel.columns])
BIHSpherical = pd.concat([bih, bih_vel], axis=1)
BIHSpherical.boxplot(column=[['BallInHead', 'Az'], ['BallInHead', 'El']])
BIHSpherical.boxplot(column=[['BallInHead', 'AzVel'], ['BallInHead', 'ElVel']])
#TODO filter the velocity data, make sure to exclude transition from end of one
#     trail to the beginning of the next trail

# BallOnRetina: ball position in Retina Frame of Reference (RFR/RCS)
bor = bih.values - eih.values
bor_vel = bih_vel.values - eih_vel.values
bor = pd.DataFrame(bor, columns=['Az', 'El'], dtype=float)
bor.columns = pd.MultiIndex.from_product([['BallOnRetina'], bor.columns])
bor_vel = pd.DataFrame(bor_vel, columns=['AzVel', 'ElVel'], dtype=float)
bor_vel.columns = pd.MultiIndex.from_product([['BallOnRetina'], bor_vel.columns])
BORSpherical = pd.concat([bor, bor_vel], axis=1)
BORSpherical.boxplot(column=[['BallOnRetina', 'Az'], ['BallOnRetina', 'El']])
BORSpherical.boxplot(column=[['BallOnRetina', 'AzVel'], ['BallOnRetina', 'ElVel']])

# Ball angular size in degree
ball2HeadVec = np.asarray(
    rawDataFrame['ballPos'].values - rawDataFrame['viewPos'].values, dtype=float)
ballDistancefromHead = np.sqrt(np.sum(np.power(ball2HeadVec, 2), axis=1))
ballRadius = 0.045
ballSizeDegs = np.arctan(ballRadius / ballDistancefromHead) / np.pi * 180
loomingRate = (ballSizeDegs[1:] - ballSizeDegs[:-1]) * frameRate

# Paddle spherical position in HCS
cycInverseMat = np.asarray(rawDataFrame['cycInverseMat'].values, dtype=float)
cycInverseMat = cycInverseMat.reshape((len(cycInverseMat), 4, 4))
paddlePosXYZ = np.asarray(rawDataFrame['paddlePos'], dtype=float)
paddlePosHomo = np.hstack([paddlePosXYZ, np.ones((len(paddlePosXYZ), 1))])
paddleHCS_XYZW = np.asarray(
    np.dot(cycInverseMat[i], paddlePosHomo[i]) for i in range(len(paddlePosXYZ)))
paddleHCS_XYZ = pd.DataFrame(paddleHCS_XYZW[:, :3], columns=[
                             'X', 'Y', 'Z'],  dtype=float)
pih_az = np.arctan(paddleHCS_XYZ['X'] / paddleHCS_XYZ['Z']) / np.pi * 180
pih_el = np.arctan(paddleHCS_XYZ['Y'] / paddleHCS_XYZ['Z']) / np.pi * 180
pih_az_vel = np.asarray(pih_az[1:].values - pih_az[:-1].values) * frameRate
pih_el_vel = np.asarray(pih_el[1:].values - pih_el[:-1].values) * frameRate
pih_az_vel = np.concatenate([[0], pih_az_vel])
pih_el_vel = np.concatenate([[0], pih_el_vel])
pih = pd.DataFrame({'Az' : pih_az, 'El': pih_el}, dtype=float)
pih.columns = pd.MultiIndex.from_product([['PaddleInHead'], pih.columns])
pih_vel = pd.DataFrame({'AzVel': pih_az_vel, 'ElVel': pih_el_vel},  dtype=float)
pih_vel.columns = pd.MultiIndex.from_product([['PaddleInHead'], pih_vel.columns])
PIHSpherical = pd.concat([pih, pih_vel], axis=1)
PIHSpherical.boxplot(column=[['PaddleInHead', 'Az'], ['PaddleInHead','El']])
PIHSpherical.boxplot(column=[['PaddleInHead', 'AzVel'], ['PaddleInHead','ElVel']])

paddle2HeadVec = np.asarray(
    rawDataFrame['viewPos'].values - rawDataFrame['paddlePos'].values, dtype=float)
paddleDistancefromHead = np.sqrt(np.sum(np.power(paddle2HeadVec, 2), axis=1))

# combine all individual DataFrames to a collection DataFrame which contains 
# all the data we need for ML experiments

















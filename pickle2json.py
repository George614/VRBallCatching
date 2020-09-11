# -*- coding: utf-8 -*-
"""
This script convert VRBallCatching data from pandas DataFrame to JSON format.

@author: George (Zhizhuo) Yang
"""

import json
import pickle
import pandas as pd
import numpy as np

fileTimeList = ['2016-4-19-14-4', '2016-4-22-11-57', '2016-4-27-13-28', '2016-4-28-10-57', '2016-4-29-11-56',
                '2016-5-3-12-52', '2016-5-4-13-3', '2016-5-5-13-7', '2016-5-6-11-2', '2016-5-6-13-4']

# pick the one subject here
fileTime = fileTimeList[0]
filePath = "D:/Datasets/VRBallCatching/" + fileTime + "/"
fileName = "exp_data-" + fileTime

sessionDict = pd.read_pickle(filePath + fileName + '.pickle')

rawDataFrame = sessionDict['raw']
processedDataFrame = sessionDict['processed']
calibDataFrame = sessionDict['calibration']
TrialInfo = sessionDict['trialInfo']

rawColumns = rawDataFrame.columns.to_list()
rawColumnsFlat = [name[0]+'_'+name[1] for name in rawColumns]
rawDF = rawDataFrame.set_axis(rawColumnsFlat, axis=1)
rawDF.to_json(filePath+'RawDataFrame.json', orient='records', indent=4)

processedColumns = processedDataFrame.columns.to_list()
processedColumnsFlat = [name[0]+'_'+name[1] for name in processedColumns]
processedDF = processedDataFrame.set_axis(processedColumnsFlat, axis=1)
processedDF.to_json(filePath+'ProcessedDataFrame.json', orient='records', indent=4)

TrialInfo.columns = TrialInfo.columns.get_level_values(0)
TrialInfo.to_json(filePath+'TrialInfo.json', orient='records', indent=4)

calibColumns = calibDataFrame.columns.to_list()
calibColumnsFlat = [name[0]+'_'+name[1] for name in calibColumns]
calibDF = calibDataFrame.set_axis(calibColumnsFlat, axis=1)
calibDF.to_json(filePath+'CalibDataFrame.json', orient='records', indent=4)

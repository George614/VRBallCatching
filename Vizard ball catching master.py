from __future__ import division, print_function

import sys
#sys.path.append("C:\\Python27")

import numpy as np
from PIL import Image as im
import os
import viz
import vizact
import vizshape
import vizmenu
import time
import pandas as pd


class myRoom:
    def __init__(self):
        
        self.topLight = []
        self.sideLight = []
        self.backLight = []
        self.floor = []
        self.frontWall = []
        self.leftWall = []
        self.rightWall = []
        self.backWall = []
        self.ballPlane = []
        self.ball = []
        self.paddle=[]
        self.cycEyeNode = []
        self.squash = []
        self.frameCounter = 25950
        self.rawDataFrame = []
        self.processedDataFrame = []
        self.trialInfoDataFrame = []
        self.calibDataFrame = []
        self.attachViewPortToHead = True
        self.saveImagesForDataSet = True
        self.saveImagesForRL = False
        self.includeBlankDuration = False
        self.renderGaze = False
        self.pause = False
        self.play = False
        self.forward = False
        self.backward = False
        self.viewHeight = 1.876298904418945
        self.linkExists = False
        self.visualizeModelOutput = False
        self.paddleCloneA = []
        self.paddleCloneB = []
        self.paddleCloneC = []
        self.paddleCloneD = []
        self.paddleCloneE = []
        self.paddleCloneF = []
        self.paddleCloneG = []
        self.modelOutputs = []

    
def readPickleFile(room, fileName):
    #df = pd.read_pickle(fileName)
    #df = pd.read_pickle("C:\\Users\\Administrator\\Downloads\\2016-5-3-12-52\\exp_data-2016-5-3-12-52.pickle")
    df = pd.read_pickle("py2_exp_data-2016-4-19-14-4.pickle")
    
    room.rawDataFrame = df['raw']
    room.processedDataFrame = df['processed']
    room.calibDataFrame = df['calibration']
    room.trialInfoDataFrame = df['trialInfo']
    
    #uncomment line 69 or 78 to reveal indice error!
    fileName = 'testDataSet.pkl'
    #tempData = pd.read_pickle(fileName)
    #room.testDataSet = tempData[:,44,:]
    #print('TestDataSize = ', room.testDataSet.shape)
    modelOffsetList = [0,5,10,15,20,25,30]
    #filePath = 'D:\Kamran Backup\Backup Before Windows Change\KamranWorksapce\DataGenerationVisualization\modelOutputs'
    #filePath = 'C:\Users\cisguest\Documents\Python Math Code'
    filePath = os.getcwd()
    modelOutput = list()
    #for i in modelOffsetList:
    #    tempData = pd.read_pickle(filePath+'\modelOutputs\modelOutput'+str(i)+'.pkl')
    #    modelOutput.append(tempData)
    #    print('OutDataSize = ', tempData.shape)
    #print('Number of Model Outputs = ', len(modelOutput))

    #room.modelOutputs = np.array(modelOutput)
    return room

def CreateTheRoom(room):


    viz.disable(viz.LIGHT0)

    room.topLight = viz.addLight()
    room.topLight.setPosition(0,4,0)
    room.topLight.setEuler( -45, 90 ,0 )

    room.topLight.spread(270)
    room.topLight.intensity(2)

    room.sideLight = viz.addLight()
    room.sideLight.setPosition(0,1,0)
    room.sideLight.setEuler(45, 0,-90)
    #see if needs to be put to 360 -room.sideLight.spread(270)
    room.sideLight.intensity(1.2)
    
    #room.backLight = viz.addLight()
    #room.backLight.setPosition(0,1,0)
    #room.backLight.setEuler(180,0,0)
    #room.backLight.spread(270)
    #room.backLight.intensity(2)

    #creates the floor plane to be 35x80
    #rotated around the Z axis(perpendicular to Y axis)
    room.floor = vizshape.addPlane(size=(35.0,80.0), axis=vizshape.AXIS_Y, cullFace=False)
    #makes the floor look like wood
    room.floor.texture(viz.addTexture('images/tile_wood.jpg'))
    #moves the floor +20 meters in the z direction
    room.floor.setPosition(0,0,20)

	#adds the wall(plane) farthest from the hand/person
#35x10 meters**2
    #rotated around the X axis (perpendicular to Z axis)
    room.frontWall = vizshape.addPlane(size=(35,10), axis=-vizshape.AXIS_Z, cullFace = False)
    #makes the front wall look like wall
    #room.frontWall.texture(viz.addTexture('images/tile_gray.jpg'))
    #moves the wall to match the edge of the
    room.frontWall.setPosition(0,5,25)
    #makes the wall appear white
    room.frontWall.color(viz.GRAY)

	 #adds the wall(plane) that when facing the frontWall, is to the camera's left
#wall is 80x10 meters**2
    #wall is rotated about the Y axis(perpendicular to X axis)
    room.leftWall = vizshape.addPlane(size=(80,10), axis=-vizshape.AXIS_X, cullFace = False)
    #makes the left wall look like wall
    room.leftWall.texture(viz.addTexture('images/tile_gray.jpg'))
    #shifts the wall to match the edge of the floor
    room.leftWall.setPosition(-17.5,5,20)
    #makes the wall appear white
    room.leftWall.color(viz.GRAY)

	#adds a wall(plane) that when facing the frontWall is to the camera's right
#wall is 80x10 meters**2
    #wall is rotated about the Y axis(perpendicular to X axis)
    room.rightWall = vizshape.addPlane(size=(80,10), axis=-vizshape.AXIS_X, cullFace = False)
    #makes the right wall look like wall
    room.rightWall.texture(viz.addTexture('images/tile_gray.jpg'))
    #shifts the wall to match the edge of the floor
    room.rightWall.setPosition(17.5,5,20)
    #makes the wall appear white
    room.rightWall.color(viz.GRAY)

	#adds a wall(plane) that when facing the frontWall is to the camera's back
#wall is 35x10 meters**2
    #wall is rotated about the X axis(perpendicular to Z axis)
    room.backWall = vizshape.addPlane(size=(35,10), axis=vizshape.AXIS_Z, cullFace = False)
    #shifts the wall to match the edge of the floor
    room.backWall.setPosition(0,5,-20)
    room.backWall.color(viz.GRAY)
    #adds texture to backWall
    #room.backWall.texture(viz.addTexture('images/tile_slate.jpg'))
    #makes the wall appear white
    room.backWall.color(viz.GRAY)

    #adds a ceiling(plane) that when facing the frontWall is to the camera's topside
    #wall is 35x80 meters**2
    #wall is rotated about the Z axis(perpendicular to Y axis)
    room.ceiling = vizshape.addPlane(size=(35.0,80.0), axis=vizshape.AXIS_Y, cullFace=False)
    #makes the ceiling appear Skyblue in color
    room.ceiling.color(viz.SKYBLUE)
    #shifts the ceiling to rest on top of the four walls
    room.ceiling.setPosition(0,10,20)

	#add a meter marker at 0 meters along the z axis of the room
	#meter0 = vizshape.addPlane(size = (5,.3), axis = vizshape.AXIS_Y, cullFace = False)
	#meter0.setPosition(0,.3, 0)
#makes the meter marker appear yellow
    #meter0.color(viz.WHITE)

    #adds a wall(plane) that when facing the frontWall is to the camera's back
    #wall is 35x10 meters**2
    #wall is rotated about the X axis(perpendicular to Z axis)
    room.ballPlane = vizshape.addPlane(size=(2,2), axis=vizshape.AXIS_Z, cullFace = False)
    #shifts the wall to match the edge of the floor
    room.ballPlane.setPosition(0,5,-20)
    #makes the wall appear white
    room.ballPlane.color(viz.WHITE)
    room.ballPlane.alpha(0.0)

    room.ball = vizshape.addSphere(radius = 0.04, color = viz.RED)
    room.paddle = vizshape.addCylinder(height = 0.03, radius = 0.15, color = viz.RED, axis = vizshape.AXIS_Z)
    room.paddle.alpha(1)
    room.cycEyeNode = vizshape.addCone(radius = 0.05, height = 0.17, color = viz.PURPLE, axis = vizshape.AXIS_Z)
    room.cycEyeNode.alpha(1)
    if (room.visualizeModelOutput == True):
        room.paddleCloneA = vizshape.addCylinder(height = 0.05, radius = 0.15, color = viz.ORANGE, axis = vizshape.AXIS_Z)
        room.paddleCloneA.alpha(.80)
        room.paddleCloneB = vizshape.addCylinder(height = 0.05, radius = 0.15, color = viz.ORANGE, axis = vizshape.AXIS_Z)
        room.paddleCloneB.alpha(.70)
        room.paddleCloneC = vizshape.addCylinder(height = 0.05, radius = 0.15, color = viz.ORANGE, axis = vizshape.AXIS_Z)
        room.paddleCloneC.alpha(.60)
        room.paddleCloneD = vizshape.addCylinder(height = 0.05, radius = 0.15, color = viz.ORANGE, axis = vizshape.AXIS_Z)
        room.paddleCloneD.alpha(.50)
        room.paddleCloneE = vizshape.addCylinder(height = 0.05, radius = 0.15, color = viz.ORANGE, axis = vizshape.AXIS_Z)
        room.paddleCloneE.alpha(.40)
        room.paddleCloneF = vizshape.addCylinder(height = 0.05, radius = 0.15, color = viz.ORANGE, axis = vizshape.AXIS_Z)
        room.paddleCloneF.alpha(.30)
        room.paddleCloneG = vizshape.addCylinder(height = 0.05, radius = 0.15, color = viz.ORANGE, axis = vizshape.AXIS_Z)
        room.paddleCloneG.alpha(.20)
    if ( room.renderGaze == True ):
        room.gazePoint = vizshape.addSphere(radius = 0.0005, color = viz.GREEN)
        room.gazePoint.setParent(room.cycEyeNode)
        
    room.male = viz.add('vcc_male.cfg') 
    room.male.alpha(0.0)
    armBone = room.male.getBone('Bip01 R UpperArm') 
    armBone.lock()  
    #armBone.setEuler(0, 0, 0) 

    armBone = room.male.getBone('Bip01 L UpperArm')
    armBone.lock()
    armBone.setEuler(-70,0,0)
    ForearmBone = room.male.getBone('Bip01 R Forearm')
    ForearmBone.lock()
    ForearmBone.setEuler(100,-90,155)

    hand = room.male.getBone('Bip01 R Hand')
    hand.lock()
    hand.setEuler(0, -90, 0.0)
    
    room.squash =  viz.addChild('Squash_Racquet.3ds')
    room.squash.scale(0.01,0.01,0.01)
    room.squash.setPosition(*hand.getPosition(mode = viz.ABS_GLOBAL)-np.array([.55,-0.2,-0.2]), mode = viz.ABS_GLOBAL)
    room.squash.setEuler([0,0,15])


    #room.squash.setQuat(hand.getQuat())
    return room

def FindIndex(Array,Value):
    
    Index =[]
    for index, number in enumerate(Array):
        if number == Value:
            Index.append(index)
        
    return Index

def CreateVisualObjects(room):

    global MarkerObject;

    MarkerObject = [];
    ColorList = [viz.WHITE, viz.GREEN,viz.BLUE,viz.YELLOW,viz.BLACK,viz.PURPLE,viz.GRAY,viz.RED]
    
    room.origin = vizshape.addAxes()
    room.origin.setPosition(0,0,0)
    
def Quaternion2Matrix(Q):
    Q = Q/np.linalg.norm(Q); # Ensure Q has unit norm
    
    # Set up convenience variables
    x = Q[0]; y = Q[1]; z = Q[2]; w = Q[3];
    w2 = w*w; x2 = x*x; y2 = y*y; z2 = z*z;
    xy = x*y; xz = x*z; yz = y*z;
    wx = w*x; wy = w*y; wz = w*z;
    
    M = np.array([[w2+x2-y2-z2 , 2*(xy - wz) , 2*(wy + xz) ,  0],
         [ 2*(wz + xy) , w2-x2+y2-z2 , 2*(yz - wx) ,  0 ],
         [ 2*(xz - wy) , 2*(wx + yz) , w2-x2-y2+z2 ,  0 ],
         [     0      ,       0     ,       0     ,  1 ]], dtype = float);
    return M;
    
def SetRotationAngle(angle):
    global alpha
    print('Screen Rotation Set to ', angle)
    alpha = angle*(np.pi/180)

        
def onTimer(num):
    #print("Visible")
#for counter in range(50,60):#TrialNumber):
    global counter, FrameNumber, GazeLine, LeftEyeShift, nearH, nearW, ballPlane, MarkerPos_XYZ_Matrix;
    global lEyeOffsetMatrix, lEyeRotationMatrix;
    global TrialStartIndex, TrialEndIndex;
    global room

    #df = pd.read_pickle("RL_Data.pkl")
    #print ('Flag = ',df['ReadyToReadData'].values[0])
    #print df.columns
    #print df
    #if (df['ReadyToReadData'].values[0] == 0):
        #print ('Vizard: Data Not Ready ==> Skip!\n\n')
    #    room.paddle.color(viz.YELLOW)
        # HACKED FOR NOW (KAMRAN)return
        
    #else:
    #    print ('\n\nYESSSSSSSSSSS')

    room.cycEyeNode.setPosition(*room.rawDataFrame.viewPos.values[room.frameCounter])
    room.cycEyeNode.setQuat(*room.rawDataFrame.viewQuat.values[room.frameCounter])
    room.ball.setPosition(*room.rawDataFrame.ballPos.values[room.frameCounter])
    #ball = vizshape.addSphere(radius = 0.03, color = viz.RED)
    #ball.setPosition(*room.rawDataFrame.ballPos.values[room.frameCounter])
    
    if (room.attachViewPortToHead == True):
        viz.MainView.setPosition(*room.rawDataFrame.viewPos.values[room.frameCounter])
        viz.MainView.setQuat(*room.rawDataFrame.viewQuat.values[room.frameCounter])

    if ( room.includeBlankDuration == True ):
        if (room.rawDataFrame.isBallVisibleQ.values[room.frameCounter]):
            room.ball.alpha(1)
            #ball.alpha(1)
        else:
            room.ball.alpha(0)
            #ball.alpha(0)
    #optimize framerate balance! use "if" statement to override current method not delete!
    if (room.visualizeModelOutput == True):
        room.paddle.setPosition(*room.rawDataFrame.paddlePos.values[room.frameCounter])
        room.paddleCloneA.setPosition(*room.modelOutputs[0,room.frameCounter,0:3])
        room.paddleCloneB.setPosition(*room.modelOutputs[1,room.frameCounter,0:3])
        room.paddleCloneC.setPosition(*room.modelOutputs[2,room.frameCounter,0:3])
        room.paddleCloneD.setPosition(*room.modelOutputs[3,room.frameCounter,0:3])
        room.paddleCloneE.setPosition(*room.modelOutputs[4,room.frameCounter,0:3])
        room.paddleCloneF.setPosition(*room.modelOutputs[5,room.frameCounter,0:3])
        room.paddleCloneG.setPosition(*room.modelOutputs[6,room.frameCounter,0:3])
        
    room.paddle.setPosition(*room.rawDataFrame.paddlePos.values[room.frameCounter])
    # room.paddle.setPosition(*[df['Hand_X'].values[0], df['Hand_Y'].values[0], df['Hand_Z'].values[0]])
    if ( room.renderGaze == True ):    
        room.gazePoint.setPosition(*room.processedDataFrame.rotatedGazePoint.values[room.frameCounter])
     # For Simplicity: We Assume that the Paddle is always aligned with Z Axis 
    room.paddle.setQuat(*room.rawDataFrame.paddleQuat.values[room.frameCounter])
    if (room.pause == True):
        room.frameCounter = room.frameCounter
    elif(room.play == True):
        room.frameCounter = room.frameCounter + 1
    elif (room.forward == True):
        room.frameCounter = room.frameCounter + 1
        room.pause = True
    elif (room.backward == True):
        room.frameCounter = room.frameCounter - 1
        room.pause = True


    if  (room.saveImagesForRL == True):
        viz.window.screenCapture('ImageForRL.jpg')
        df['ReadyToReadImage'].values[0] = 1
        df['ReadyToReadData'].values[0] = 0
        df.to_pickle("RL_Data.pkl")
        #room.paddle.color(viz.GREEN)
        print ('Yay')
        #hand = room.male.getBone('Bip01 R Hand')
        #hand.setPosition( *room.rawDataFrame.paddlePos.values[room.frameCounter], mode = viz.ABS_GLOBAL)# - np.array([0,-1.5,0]))
    viz.window.screenCapture('imageDataSet/image_'+str(room.frameCounter)+'.jpg' )

#class KeyEventClass(viz.EventClass): 
#    def __init__(self): 
#        viz.EventClass.__init__(self) 
#        #Add a key callback for this class. 
#        self.callback(viz.KEYDOWN_EVENT, self.onKeyDown) 
def keyDown(key):
    global linkExists, ballLink
    if (key == 'q'):
        print ('key q was pressed to set viewpoint to follow the ball')
        #link w/ball creation
        ballLink = viz.link(room.ball, viz.MainView)
        ballLink.preEuler([180,0,0])
        ballLink.preTrans([0,0,-0.5])
        linkExists = True
    if (key == 'p'):
        print ('key p was pressed to pause')
        room.pause = True
        room.play = False
        room.forward = False
        room.backward = False
    elif (key == 'l'):
        print ('key l was pressed to play')
        room.play = True
        room.pause = False
        room.forward = False
        room.backward = False
    elif (key == 'f'):
        print ('key f was pressed to next frame')
        room.forward = True
        room.backward = False
        room.play = False
        room.pause = False
    elif (key == 'b'): 
        print ('key b was pressed to back frame') 
        room.backward = True
        room.play = False
        room.pause = False
        room.forward = False
    if (key == 'h'):
        if (linkExists):
            print ('ballLink exists')
            ballLink.remove()
            linkExists = False
        print ('ballLink does not exist')
        print ('key h was pressed to set viewpoint to freecam')
        room.attachViewPortToHead = False
        viz.MainView.setEuler([0.0, 0.0, 0.0])
    elif (key == 'v'):
        if (ballLink is not None):
            ballLink.remove()
        print ('key v was pressed to set viewpoint to fixed-cam')
        room.attachViewPortToHead = True
    if (key == 'e'):
        if (ballLink is not None):
            ballLink.remove()
        room.viewHeight = room.viewHeight - 1
        print ('key e was pressed to lower viewpoint')
        viz.MainView.setPosition([0.27629128098487854, room.viewHeight, -3.3362717628479004])
    elif (key == 'r'):
        if (ballLink is not None):
            ballLink.remove()
        room.viewHeight = room.viewHeight + 1
        print ('key r was pressed to raise viewpoint')
        viz.MainView.setPosition([0.27629128098487854, room.viewHeight, -3.3362717628479004])

        
        

        

if __name__ == '__main__':
    
    global lEyeOffsetMatrix, lEyeRotationMatrix;
    global FrameNumber, counter, TrialStartIndex, TrialEndIndex;
    global nearW,nearH;
    global rawDataFrame, processedDataFrame, calibDataFrame, trialInfoDataFrame
    global linkExists, ballLink
    linkExists = False
    ballLink = None
    TimeInterval = 0.005
    nearH = 1.2497;
    nearW = 1.5622;
    viz.setMultiSample(4)
    viz.fov(110)
    viz.go()
    #ExtractDataFromMatFile('Exp_RawMat_MarkerPos2014-11-26-21-18.mat');
    #fileName = "C:\\Users\\Kamran Binaee\\Documents\\Python Scripts\\KamranWorksapce\\DataGenerationVisualization\\2016-4-19-14-4\\exp_data-2016-4-19-14-4.pickle"
    #fileName = "D:\Kamran Backup\Backup Before Windows Change\KamranWorksapce\DataGenerationVisualization\\2016-4-19-14-4\\exp_data-2016-4-19-14-4.pickle"
    #fileName = "C:\\Users\\cisguest\\Documents\\Python Math Code\\exp_data-2016-4-19-14-4.pickle"
    
    fileName = "\\2016-5-3-12-52\\exp_data-2016-5-3-12-52.pickle"
    room = myRoom()
    room = readPickleFile(room, fileName)
    #print ('Model Data Size  =', room.modelOutputs.shape)
    room = CreateTheRoom(room)
    #CreateVisualObjects()
    
    print ('Running Visualization Code ...\n\n\n')
    print ('Attach View to Head = ', room.attachViewPortToHead)
    print ('Save Images for RL = ', room.saveImagesForRL)
    print ('Save Images for Data Set = ', room.saveImagesForDataSet)
    print ('Ball Disappears = ', room.includeBlankDuration, '\n')
    if (room.attachViewPortToHead == False) :
        #sets where the camera view is located
        #viz.MainView.setPosition([-0.46132529973983765, 1.8138036012649536, -1.4800882935523987])
        viz.MainView.setPosition([0.27629128098487854, 1.9876298904418945, -3.3362717628479004])
        viz.MainView.setEuler([-18.816675186157227, 0.0, 0.0])
        #viz.MainView.setPosition([-1.8827998638153076, 2.381239414215088, 0.05993637815117836])
        #sets the angle at which the camera view is pointed
        viz.MainView.setEuler(3.1846203804016113, -0.0, 0.0)
    #lEyeOffsetMatrix = np.array([[1, 0, 0, -0.03],[0, 1, 0, 0], [0, 0, 1, 0],[0, 0, 0, 1]], dtype = float)
    #lEyeRotationMatrix = np.eye(4, dtype = float);
    #counter = 1
    #FrameNumber = TrialStartIndex[0] - 100;
    #FrameNumber = 1;
    #SetRotationAngle(1.6);
    #if the timer goes off go to the onTimer function
    value = np.array(room.rawDataFrame.viewPos.values[0])
    value = value + np.array([0.4,-1.4,0])
    #print('First Value',value)
    room.male.setPosition( value[0], value[1], value[2])# - np.array([0,-1.5,0]))
    
    viz.callback(viz.KEYDOWN_EVENT, keyDown)
    viz.callback(viz.TIMER_EVENT, onTimer)
    viz.starttimer(1, TimeInterval, viz.FOREVER)
    
    
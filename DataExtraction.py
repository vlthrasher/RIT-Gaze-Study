#reads the mat file
from __future__ import division
import os,random
import scipy.io as sio
import numpy as np
#import matplotlib.pyplot as plt
import ast


def ParseTextData():

    #datapath = '/Users/kamranbinaee/Documents/Python-Programming/Matlab2PythonProject';
    #fname = os.path.join(datapath,'DataPoints0.txt')
    
    txtFile = open("C:\Users\V\Documents\Internship\exp_data-2014-5-9-13-9.txt","r") #exp_data-2014-5-9-13-9.txt   Data2.txt
    values = np.array([],dtype = float);
    i = 0
    
    X_Matrix = np.array([], dtype = float);
    Y_Matrix = np.array([], dtype = float);
    Z_Matrix = np.array([], dtype = float);
    C_Matrix = np.array([], dtype = float);
    F_Matrix = np.array([], dtype = float);
    inCalibrate = np.array([], dtype = float);
    EventFlag = np.array([], dtype = float);
    TrialType = np.array([], dtype = str);
    Paddle_XYZ_Matrix = np.array([],  dtype = float);
    XYZ_Matrix = np.array([],  dtype = float);
    Quat_Matrix = np.array([], dtype = float);
    XYZ_Matrix.resize((1,3))
    Paddle_XYZ_Matrix.resize((1,3))
    Quat_Matrix.resize((1,4))
    
    print 'Parsing TextData in progress...'
    
    for aline in txtFile:
        Line = aline.split()
        for i in range(len(Line)):
            #print 'TextFile Parsing'
            if (Line[i] == 'frameTime'):
                #F_Matrix.append(float(Line[i+1]));
                F_Matrix = np.hstack((F_Matrix, Line[i+1]))
                #print 'F=\n', F_Matrix
            elif (Line[i] == 'inCalibrateBool'):
                inCalibrate = np.hstack((inCalibrate, Line[i+1]))
            elif (Line[i] == 'eventFlag'):
                EventFlag = np.hstack((EventFlag,Line[i+1]));
            elif (Line[i] == 'trialType'):
                TrialType = np.hstack((TrialType, Line[i+1]));
            elif (Line[i] == 'viewPos_XYZ'):
                XYZ_Matrix = np.vstack((XYZ_Matrix, np.array([Line[i+1], Line[i+2], Line[i+3]]) ));
            elif (Line[i] == 'paddlePos_XYZ'):
                Paddle_XYZ_Matrix = np.vstack((Paddle_XYZ_Matrix, np.array([Line[i+1], Line[i+2], Line[i+3]]) ));
            elif (Line[i] == 'viewQUAT_WXYZ'):
                Quat_Matrix = np.vstack((Quat_Matrix, np.array([Line[i+1], Line[i+2], Line[i+3], Line[i+4]])))
    
    txtFile.close()
    
    XYZ_Matrix = np.delete(XYZ_Matrix, 0, 0)
    Quat_Matrix = np.delete(Quat_Matrix, 0, 0)
    Paddle_XYZ_Matrix = np.delete(Paddle_XYZ_Matrix, 0, 0)
    
#    print 'Pos size=\n', XYZ_Matrix.shape
#    print 'F size=\n', F_Matrix.shape
#    print 'E size=\n', EventFlag.shape
#    print 'T size=\n', TrialType.shape
#    print 'Q size=\n', Quat_Matrix.shape
  
    print '...Text File Parsing Done!!'
    
    
    MatFile = {'XYZ_Pos':XYZ_Matrix,'FrameTime':F_Matrix,'EventFlag':EventFlag, 'TrialType':TrialType, 'Quat_Matrix':Quat_Matrix, 'paddlePos_XYZ':Paddle_XYZ_Matrix}
    sio.savemat('RawData.mat', MatFile)
    print 'RawData.mat File Saved'

def LoadMatFile(FileName):
    
    RawMatFile = sio.loadmat(FileName)
    hX = map(float, RawMatFile['paddlePos_XYZ'][:,0])
    hY = map(float, RawMatFile['paddlePos_XYZ'][:,1])
    hZ = map(float, RawMatFile['paddlePos_XYZ'][:,2])
    T = map(float, RawMatFile['FrameTime'])
    Event = map(float, RawMatFile['EventFlag'])
    bX = map(float, RawMatFile['ballPos_XYZ'][:,0])
    bY = map(float, RawMatFile['ballPos_XYZ'][:,1])
    bZ = map(float, RawMatFile['ballPos_XYZ'][:,2])

    Matrix = np.vstack((hX,hY))
    Matrix = np.vstack((Matrix,hZ))
    Matrix = np.vstack((Matrix,T))
    Matrix = np.vstack((Matrix,Event))
    Matrix = np.vstack((Matrix,bX))
    Matrix = np.vstack((Matrix,bY))
    Matrix = np.vstack((Matrix,bZ))
    print Matrix[:,25]    
    
    return Matrix

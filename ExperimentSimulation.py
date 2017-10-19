import LoadParameters
import DataExtraction
import os
import numpy as np
from configobj import ConfigObj


subNum = 1

class SubjectData(ConfigObj):

    def __init__(self, SubjectNumber):
	
        print 'Subject Data instantiation with',SubjectNumber
        configReader = ConfigObj('ProcessingPipline.cfg')
        general = configReader.get('general')
        #print general
        pi = np.pi
        self.subNum = SubjectNumber
        self.gazeFrameOffset = general['gazeFrameOffset']
        self.expTitle = general['expTitle']

        self.medFiltSize = general['medFiltSize']
        self.gaussFiltSize = general['gaussFiltSize']
        self.gaussSdev = general['gaussSdev']
        
        self.eyeScale = general['eyeScale']
        
        self.arrDegsX = float(general['arrDegsX'])
        self.arrDegsY = float(general['arrDegsY'])
        
        self.arrRadsX = (self.arrDegsX) * (pi/180)
        self.arrRadsY = (self.arrDegsY) * (pi/180)
        
        self.arrPixX = float(general['arrPixX'])
        self.arrPixY = float(general['arrPixY'])
        
        self.aspectRatio = self.arrPixX / self.arrPixY 
        
        self.nearH = 2 * np.tan( (self.arrDegsY*(pi/180)) /2 )
        self.nearW = self.nearH*self.aspectRatio
        
        self.eyeDiameter = general['eyeDiameter']
        self.eyeOffset = general['eyeOffset']
        
        # 1.11, 85 / 68
        self.eyeInScreenPosX = float(general['eyeInScreenPosX'])
        self.eyeInScreenPosY = float(general['eyeInScreenPosY'])
        self.eihCenterX = (self.eyeInScreenPosX-.5)*(self.arrDegsX)
        self.eihCenterY = (self.eyeInScreenPosY-.5)*(self.arrDegsY)
        
        self.ballDiameter = general['ballDiameter']
        
    ##==============================================================================
    #     Object parameters
    #     roomInfo = struct(...
    #         'frontWallDist',frontWallDist,...
    #         'backWallDist',backWallDist,...
    #         'roomWidth',roomWidth,...
    #         'roomHeight',roomHeight,...
    #         'targetHeight',1.5,...
    #         'targetRadius',3)
    ##==============================================================================
        self.racquetOffset = general['racquetOffset']# [0, 0, 0] # only for the racquet texture
        self.racquetSize = general['racquetSize'] #[.03, .1]
        
        self.c = np.array([.2, .2, .2, .2, .2], dtype = float).T
        
        self.colorList = general['colorList']#'rbckg'
        self.shapeList = general['shapeList']#'sdo'
        self.styleList = general['styleList']#':*-'
        
    ##==============================================================================
        self.movieList  = ['2014-5-9-13-9', '2014-5-9-13-10']
        
        self.numSubs = len(self.movieList)
        self.excludedSubs = general['excludedSubs']
        
        self.includedSubs = set(xrange(1,self.numSubs)) - set(self.excludedSubs)
        self.numIncluded = len(self.includedSubs)
    
        # Not Sure about this If statement (Kamran)   
        if self.subNum is not 0:
            
            self.movieName = self.movieList[self.subNum]
            self.dataFileString = 'Data/Extracted/' + str(self.movieName)
            self.processedDataFileString = str(self.dataFileString) + '-processed.mat'
            self.rawDataFileString = str(self.dataFileString) + '-raw.mat'
    
        print 'Movie Name is:\n', self.movieName
        print 'Data File String is:\n', self.dataFileString
        print 'Processed Data File String is:\n', self.processedDataFileString
        print 'raw Data File String is:\n', self.rawDataFileString
        
        ##  Exclude trials
        self.excludeTrialList = []
    
        # Not Sure about this If statement (Kamran)   
        if self.subNum is not 0:
            
            #movieName = movieList{subNum}
            self.rawDataFileString = 'Data/Extracted/' + str(self.movieList[self.subNum])
            #processedDataFileString = [dataFileString '-processed.mat']
        
            self.expTextDataFileString = 'Data/Extracted/exp_data-' + str(self.movieList[subNum]) + '.txt'
            self.eyeTextDataFileString = 'Data/Extracted/eye_data-' + str(self.movieList[subNum]) + '.txt'
        
        print 'exp Text Data File String is:\n', self.expTextDataFileString
        print 'eye Test Data File String is:\n', self.eyeTextDataFileString
        
        
    ##==============================================================================
    ##  Parameters for fixFinder
    ##==============================================================================    
    
        fixfinder = configReader.get('fixfinder')
        self.t_thresh = fixfinder['t_thresh'] #(1/60)*1000*4 # t_thresh in ms.  6 frames = 100 ms
        self.clump_space_thresh = fixfinder['clump_space_thresh'] #5
        self.clump_t_thresh = fixfinder['clump_t_thresh']#(1/60)*1000*3
        self.vel_thresh = fixfinder['vel_thresh']#40
        
        self.minThreshDist = fixfinder['minThreshDist']#1.5
        self.predPursThresh = fixfinder['predPursThresh']#100
    
    ##==============================================================================
    ##  Parameters for saccade finding algorithm
    ##==============================================================================        
        
        saccade = configReader.get('saccade')
        self.saccStartStopThresh = saccade['saccStartStopThresh']#20 ']# saccade acceleration threshold for start/stops
        self.saccMinFramesBeforeBounce = saccade['saccMinFramesBeforeBounce']#2 # sacc must peak this many frames before the bounce
        
        self.t_threshBeforeFix = saccade['t_threshBeforeFix']#(1/60)*1000*3  # "Blind spot" prior to a fix during which no visual info can be
        
        self.filterKernel = saccade['filterKernel']#[ -1, 0, 1, 2, 3, 2, 1, 0, -1 ]
        self.saccMinHeight = saccade['saccMinHeight']#100
        self.saccMaxFramesFromBounce = saccade['saccMaxFramesFromBounce']#3 # sacc must peak this many frames before the bounce
        self.v = saccade['v']# 20
        self.saccSearchWin  = saccade['saccSearchWin']#60
        
        self.t_threshSaccToFix =  saccade['t_threshSaccToFix']# (1/60)*1000*2 # max allowed time   between sacc and fix if they are to be considered part of a predicive sequence
        
    ##==============================================================================
    ##  Hand adjustment
    ##==============================================================================
        handadj = configReader.get('handadj')
        self.adjSearchWin = handadj['adjSearchWin']#60
        self.adjMinHeight = handadj['adjMinHeight']#20
        self.t_threshAdjMSAfterBounce = handadj['t_threshAdjMSAfterBounce']#125
        
    ##==============================================================================
    ##  Params for pursuit finding algorithm
    ##==============================================================================
        
        pursuit = configReader.get('pursuit')
        self.purs_degThresh = pursuit['purs_degThresh']#5
        self.purs_e2bChangeThresh_Low = pursuit['purs_e2bChangeThresh_Low']#.30 ']# lower gain threshold
        self.purs_e2bChangeThresh_High = pursuit['purs_e2bChangeThresh_High']#1.2 # higher gain threshold
        self.purs_durThresh = pursuit['purs_durThresh']#(1/60)*1000*3 # 50 ms
        self.purs_clump_t_thresh = pursuit['purs_clump_t_thresh']#(1/60)*1000*4
        self.catchupSaccMinAccel = pursuit['catchupSaccMinAccel']#20
        
    ##==============================================================================
    ##  Parmas for hand filtering - gaussian filter
    ##==============================================================================
        handfiltering = configReader.get('handfiltering')
        self.handFiltWidth = handfiltering['handFiltWidth']#5
        self.handFiltSD = handfiltering['handFiltSD']#2
        return

if __name__ == "__main__":
    #Subject_1 = SubjectData(1);
    #LoadParameters.CreateDirectories()
    DataExtraction.ParseTextData();
    [X, Y, Z, T] = DataExtraction.LoadMatFile('RawData.mat')        
    print 'XYZT', X[25], Y[25], Z[25], T[25]
    
    #LoadParameters.LoadParams()
    
    
    
    #print Subject_1.gazeFrameOffset, Subject_1.expTitle

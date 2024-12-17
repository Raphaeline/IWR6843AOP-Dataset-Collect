# General Library Imports
# PyQt Imports
# Local Imports
# Logger
# # Different methods to color the points 
COLOR_MODE_SNR = 'SNR'
COLOR_MODE_HEIGHT = 'Height'
COLOR_MODE_DOPPLER = 'Doppler'
COLOR_MODE_TRACK = 'Associated Track'

MAX_PERSISTENT_FRAMES = 30

from collections import deque
import numpy as np
import time
import string

from PySide2.QtCore import Qt, QThread
from PySide2.QtGui import QPixmap, QFont
import pyqtgraph.opengl as gl
import pyqtgraph as pg
from PySide2.QtWidgets import QGroupBox, QGridLayout, QLabel, QWidget, QVBoxLayout, QTabWidget, QComboBox, QCheckBox, QSlider, QFormLayout

from Common_Tabs.plot_3d import Plot3D
from Common_Tabs.plot_1d import Plot1D
from Demo_Classes.Helper_Classes.fall_detection import *
from demo_defines import *
from graph_utilities import get_trackColors, eulerRot
from gl_text import GLTextItem

from common.gui_threads import updateQTTargetThread3D
from gui_common import TAG_HISTORY_LEN

import logging

log = logging.getLogger(__name__)

from Demo_Classes.video_doorbell import VideoDoorbell

class TwoPassVideoDoorbell(VideoDoorbell):
    def __init__(self):
        VideoDoorbell.__init__(self)

    def setupGUI(self, gridLayout, demoTabs, device):
        super().setupGUI(gridLayout, demoTabs, device)
        modeSwitchBox = self.initModeSwitchPane()
        gridLayout.addWidget(modeSwitchBox,5,0,1,1)

    def updateGraph(self, outputDict):
        super().updateGraph(outputDict)
        # If we're in second pass mode and any of the boxes show a detection 
        if ('enhancedPresenceDet' in outputDict):
            if(self.modeSwitchLabel.text() == 'Second Pass Mode' and 2 in outputDict['enhancedPresenceDet']):
                self.modeSwitchLabel.setText('Camera On')
                self.modeSwitchLabel.setFont(QFont('Arial', 16))
                self.modeSwitchLabel.setStyleSheet("background-color: red; border: 1px solid black;")
                
        if("modeState" in outputDict):
            if(outputDict['modeState'] == 0): # First pass mode
                self.modeSwitchLabel.setText('First Pass Mode')
                self.modeSwitchLabel.setFont(QFont('Arial', 16))
                self.modeSwitchLabel.setStyleSheet("background-color: lightgreen; border: 1px solid black;") 
            elif(outputDict['modeState'] == 1): # Second Pass mode
                self.modeSwitchLabel.setText('Second Pass Mode')
                self.modeSwitchLabel.setFont(QFont('Arial', 16))
                self.modeSwitchLabel.setStyleSheet("background-color: yellow; border: 1px solid black;") 
        

           

    def initModeSwitchPane(self):
        modeSwitchBox = QGroupBox('Mode Switch Status')
        self.modeSwitchLabel = QLabel('Two Pass Mode Disabled')
        self.modeSwitchLabel.setFont(QFont('Arial', 16))
        self.modeSwitchLabel.setStyleSheet("background-color: lightgrey; border: 1px solid black;") 
        self.modeBoxLayout = QVBoxLayout()
        self.modeBoxLayout.addWidget(self.modeSwitchLabel)
        modeSwitchBox.setLayout(self.modeBoxLayout)
        return modeSwitchBox
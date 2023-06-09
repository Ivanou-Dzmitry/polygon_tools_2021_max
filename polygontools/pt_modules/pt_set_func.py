# This Python file uses the following encoding: utf-8
#******************************************************************************************************
# Created: polygon.by        
# Last Updated: 8 may 2020
# Version: 2021.0.0           
#
# Authors:
# Dzmitry Ivanou
# Dzmitry Dzrynou
#
# Much thanks to Yury Ruskevich, CGCode Telegram Channel and Alexander Plechkov for some good ideas an support.
#
#******************************************************************************************************
# MODIFY THIS AT YOUR OWN RISK

import os
import sys
import platform
from pymxs import runtime as rt
import importlib

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import *


#print (sys.path)
RootDir = ".."

if RootDir not in sys.path:
  sys.path.append( RootDir )

import pt_config_loader as cfgl
importlib.reload(cfgl)

#GUI    
class PT_Settings_Tab (QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)

        #set layoit
        self.tabSet_v_layout = QVBoxLayout(self)
        self.tabSet_v_layout.setAlignment(Qt.AlignTop)

        MaxWidth = 370
        
        currentDir = os.path.dirname(__file__)
        try:
            iconRusLang  = QPixmap(currentDir +"/icons/ruslang_icon.png")
            iconEngLang  = QPixmap(currentDir +"/icons/englang_icon.png")
            iconReset  = QPixmap(currentDir +"/icons/reset_icon.png")
        except:
            cmds.warning( "PolygonTools: Can't load icons for Settings Tab! Check icon files in pt_modules/icons directory.")
                
        self.gboxSet = QGroupBox("Units Setup")
        self.gboxSet.setMaximumWidth(MaxWidth)
        self.gboxSet_v_layout = QVBoxLayout()

        #Top Label
        self.lblInfo_01 = QLabel()

        #Units
        self.cboxSysUnits = QComboBox()
        self.cboxSysUnits.addItems(["meters","centimeters","millimeters"])
        
        #Units label
        self.lblSysUnits = QLabel("Working Units ")
        
        self.btnReset = QPushButton("Reset All Values to Default")
        self.btnReset.setStyleSheet("color:#000000;background-color:#E1E1E1;")
        self.btnReset.setMaximumWidth(MaxWidth)
        #self.btnReset.setMinimumWidth(200)
        self.btnReset.setMinimumHeight(30)
        self.btnReset.setIcon(iconReset)          
        
        self.lblSysInfo = QLabel("Python Info:")
        
        self.gboxConclusionLang = QGroupBox("Conclusion Language")
        self.gboxConclusionLang.setMaximumWidth(MaxWidth)
        self.gboxConclusionLang_v_layout = QVBoxLayout()
        
        #layout for buttons
        self.tabSet_h_layout_02 = QHBoxLayout()
        self.tabSet_h_layout_02.setAlignment(Qt.AlignLeft)

        #lang icons
        self.btnRusLang = QToolButton()
        self.btnRusLang.setCheckable(True)
        self.btnRusLang.setIcon(iconRusLang)
         
        self.btnEngLang = QToolButton() 
        self.btnEngLang.setIcon(iconEngLang)
        self.btnEngLang.setCheckable(True)        
        
        #add button to the layout
        self.tabSet_h_layout_02.addWidget(self.btnEngLang)
        self.tabSet_h_layout_02.addWidget(self.btnRusLang)        
        self.gboxConclusionLang_v_layout.addLayout(self.tabSet_h_layout_02)        
        
        self.gboxSysInfo = QGroupBox("System Info")
        self.gboxSysInfo.setMaximumWidth(375)
        self.gboxSysInfo_v_layout = QVBoxLayout()                
        
        #Add Widgets
        
        self.tabSet_v_layout.addWidget(self.lblInfo_01)
        
        self.tabSet_v_layout.addWidget(self.gboxSet)
        self.gboxSet.setLayout(self.gboxSet_v_layout)
        
        #Horiz Layout for Set        
        self.tabSet_h_layout_01 = QHBoxLayout()
        self.tabSet_h_layout_01.setAlignment(Qt.AlignLeft)
        
        self.gboxSet_v_layout.addLayout(self.tabSet_h_layout_01)
        
        self.tabSet_h_layout_01.addWidget(self.lblSysUnits)
        self.tabSet_h_layout_01.addWidget(self.cboxSysUnits)
        
        #conclusion
        self.gboxConclusionLang.setLayout(self.gboxConclusionLang_v_layout)
        self.tabSet_v_layout.addWidget(self.gboxConclusionLang)
        
        self.tabSet_v_layout.addWidget(self.gboxSysInfo)
        self.gboxSysInfo.setLayout(self.gboxSysInfo_v_layout)
        
        self.gboxSysInfo_v_layout.addWidget(self.lblSysInfo)
        self.lblSysInfo.setWordWrap(True)
        
        self.tabSet_v_layout.addWidget(self.btnReset)
        
        #get Pyton version
        self.lblSysInfo.setText("Python: " + (platform.sys.version))

        #SIGNALS
        self.cboxSysUnits.activated.connect(self.setWorkUnits)

        #change lang
        self.btnEngLang.pressed.connect(self.btnEngLangPressed)
        self.btnRusLang.pressed.connect(self.btnRusLangPressed)

        #reset
        self.btnReset.clicked.connect(self.btnResetPressed)

        #check Units
        self.checkUnits()

        #lang selector
        current_languge = cfgl.configLoader()[14]
        
        # check buttons
        if current_languge == "eng":
            self.btnRusLang.setChecked(False)
            self.btnEngLang.setChecked(True)
        elif current_languge == "rus":
            self.btnRusLang.setChecked(True)
            self.btnEngLang.setChecked(False)     

    #eng lang ON
    def btnEngLangPressed(self):
        
        self.btnRusLang.setChecked(False)

        #for press again
        if self.btnEngLang.isChecked() == True:
            self.btnRusLangPressed()
        
        #change lang
        path_config = cfgl.configLoader()[99:101]
        cfgl.ConfigWriter('Languge', 'current_languge', 'eng', path_config[0], path_config[1])
        
    #rus lang ON
    def btnRusLangPressed(self):
        
        self.btnEngLang.setChecked(False)

        #for press again
        if self.btnRusLang.isChecked() == True:
            self.btnEngLangPressed()

        #change lang
        path_config = cfgl.configLoader()[99:101]
        cfgl.ConfigWriter('Languge', 'current_languge', 'rus', path_config[0], path_config[1])


    #compare units in cfg and system
    def checkUnits(self):

        

        CustomSysUnits = cfgl.configLoader()[9]
    
        CurrentWorkUnits = str(rt.units.Systemtype)
        
        if CustomSysUnits != CurrentWorkUnits:

            rt.execute ("units.Systemtype = #" + CustomSysUnits)
            
            if CustomSysUnits == 'meters':
                self.cboxSysUnits.setCurrentIndex(0)

            if CustomSysUnits == 'centimeters':
                self.cboxSysUnits.setCurrentIndex(1)

            if CustomSysUnits == 'millimeters':
                self.cboxSysUnits.setCurrentIndex(2)

            print ("PolygonTools: Units changed to", CustomSysUnits)
            self.lblInfo_01.setText("Units changed to " + CustomSysUnits)
        else:

            if CustomSysUnits == 'meters':
                self.cboxSysUnits.setCurrentIndex(0)

            if CustomSysUnits == 'centimeters':
                self.cboxSysUnits.setCurrentIndex(1)

            if CustomSysUnits == 'millimeters':
                self.cboxSysUnits.setCurrentIndex(2)
            
            print ("PolygonTools: Units is", CustomSysUnits)
            self.lblInfo_01.setText("Units is " + CustomSysUnits)

    #change working units    
    def setWorkUnits(self):

        
        
        #load path and config        
        PathConfig = cfgl.configLoader()[99:101] 
        
        if self.cboxSysUnits.currentIndex() == 0:
            rt.execute ("units.Systemtype = #meters")
            self.lblInfo_01.setText("Units changed to meters")
            print (self.lblInfo_01.text())
            cfgl.ConfigWriter('Units', 'Custom_System_type_units', 'meters', PathConfig[0], PathConfig[1]) 
    
        if self.cboxSysUnits.currentIndex() == 1:
            rt.execute ("units.Systemtype = #centimeters")
            self.lblInfo_01.setText("Units changed to centimeters")
            print (self.lblInfo_01.text())
            cfgl.ConfigWriter('Units', 'Custom_System_type_units', 'centimeters', PathConfig[0], PathConfig[1]) 

        if self.cboxSysUnits.currentIndex() == 2:
            rt.execute ("units.Systemtype = #millimeters")
            self.lblInfo_01.setText("Units changed to millimeters")
            print (self.lblInfo_01.text())
            cfgl.ConfigWriter('Units', 'Custom_System_type_units', 'millimeters', PathConfig[0], PathConfig[1]) 

    def btnResetPressed(self):
            
            path_config = cfgl.configLoader()[99:101]  
            
            #restore default values
            cfgl.createDefaultConfig(path_config[1], path_config[0])

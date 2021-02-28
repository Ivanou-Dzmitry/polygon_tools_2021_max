#******************************************************************************************************
# Created: polygon.by        
# Last Updated: 12 may 2020
# Version: 2021.0.1
#
# Authors:
# Dzmitry Ivanou
# Dzmitry Dzrynou
#
# Much thanks to Yury Ruskevich, CGCode Telegram Channel and Alexander Plechkov for some good ideas an support. 
#
#******************************************************************************************************
# MODIFY THIS AT YOUR OWN RISK

from PySide2 import QtWidgets, QtCore, QtGui
import os
import sys
from pymxs import runtime as rt

import importlib

import pt_gen_func as genf
importlib.reload (genf)

import pt_set_func as setf
importlib.reload (setf)

import pt_uv_func as uvf
importlib.reload (uvf)

import pt_texel_func as tef
importlib.reload (tef)

import pt_tools_func as tools
importlib.reload (tools)

import pt_check_func as check
importlib.reload (check)

RootDir = ".."

if RootDir not in sys.path:
  sys.path.append( RootDir )

import pt_config_loader as cfgl
importlib.reload(cfgl)

class PTGUI (QtWidgets.QDockWidget):
    def __init__(self, parent=None):
        super(PTGUI, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setWindowTitle('PolygonTools 2021.0.0')
        #self.initUI()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        
        #main laout
        self.MainPTLayout = parent.layout()

        MainPTLayout = QtWidgets.QVBoxLayout()

        #tab widget    
        tabPt = QtWidgets.QTabWidget()
        tabPt.setObjectName("tabPt")  
        #min max size
        tabPt.setMaximumWidth(370)  
        tabPt.setMinimumWidth(370)  

        #add tabs
        tabGen = genf.PT_Gen_Tab()
        tabTex = tef.PT_Texel_Tab()
        tabUv = uvf.PT_UV_Tab()
        tabTools = tools.PT_Toools_Tab()
        tabSet = setf.PT_Settings_Tab()
        tabCheck = check.PT_Check_Tab()
            
        tabPt.addTab(tabGen, "General")
        tabPt.addTab(tabTex, "Texel")
        tabPt.addTab(tabUv, "UV")
        tabPt.addTab(tabTools, "Tools")
        tabPt.addTab(tabCheck, "Checker")
        tabPt.addTab(tabSet, "Settings")

        #cjperight label
        lblCopyright = QtWidgets.QLabel(u'\N{COPYRIGHT SIGN}' + " polygon.by, 2020 | e-mail: info@polygon.by")
        lblCopyright.setMaximumWidth(340)

        #Help Button
        btnHelp = QtWidgets.QPushButton("?")
        btnHelp.setMinimumWidth(23)
        btnHelp.setMaximumWidth(23)

        #bottom layout for copyright
        tabMain_h_layout_01 = QtWidgets.QHBoxLayout()
        tabMain_h_layout_01.setAlignment(QtCore.Qt.AlignLeft)

        #add label and button
        tabMain_h_layout_01.addWidget(lblCopyright)
        tabMain_h_layout_01.addWidget(btnHelp)

        #add widgets to main layout
        MainPTLayout.addWidget(tabPt)
        MainPTLayout.addLayout(tabMain_h_layout_01)
        
        PTWidget = QtWidgets.QWidget()
        PTWidget.setLayout(MainPTLayout)
        self.setWidget(PTWidget)

        #connections
        btnHelp.clicked.connect(helpOpen)

    def run(self):
        return self

    #delete procedures    
    def __del__(self):
        
        print ('\n', "PolygonTools Cleanup Operations", '\n')
        
        #unreg viewport functions
        rt.unregisterRedrawViewsCallback(genf.showDimensionInViewport)
        rt.unregisterRedrawViewsCallback(genf.showDimensionInViewport)

        print ("", '\n', "PolygonTools was Closed.", '\n')

#open brouser with help
def helpOpen():
    
    current_languge = cfgl.configLoader()[14]
    
    #link to proper help
    if current_languge == "eng":
        try:
            rt.ShellLaunch("https://docs.google.com/document/d/1_qMTk-jUeqsh-yDwB3fmzu23S18b-AzQf_dzyM2sSB0/edit?usp=sharing", "")
        except:
            print ("Can't open link. Open it manually - https://docs.google.com/document/d/1IWj53-MlLLP6MJPIJoCVVPzSr1cUAr-ijET6qgJqVDE/edit?usp=sharing")
    else:
        try:
            rt.ShellLaunch("https://docs.google.com/document/d/1IWj53-MlLLP6MJPIJoCVVPzSr1cUAr-ijET6qgJqVDE/edit?usp=sharing", "")
        except:
            print ("Can't open link. Open it manually - https://docs.google.com/document/d/1IWj53-MlLLP6MJPIJoCVVPzSr1cUAr-ijET6qgJqVDE/edit?usp=sharing")


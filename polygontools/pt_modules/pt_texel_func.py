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
import math
import time
from decimal import Decimal
from pymxs import runtime as rt
import random
import importlib

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import *

import pt_conclusion as conclusion
importlib.reload(conclusion)

import pt_gen_func as gen_func
importlib.reload(gen_func)

RootDir = ".."

if RootDir not in sys.path:
  sys.path.append( RootDir )
  
import pt_config_loader as cfgl
importlib.reload(cfgl)

class PT_Texel_Tab (QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)

        #Create Widgets
        self.tabTex_v_layout = QVBoxLayout(self)
        self.tabTex_v_layout.setAlignment(Qt.AlignTop)
        
        #icons
        CurrentDir = os.path.dirname(__file__)
        IconPath = (CurrentDir + "\icons")

        try:
            iconGetTex  = QPixmap(IconPath +"/gettexel_icon.png")
            iconCheckTex  = QPixmap(IconPath +"/checktexel_icon.png")
            iconSetTex  = QPixmap(IconPath +"/settexel_icon.png")
            iconCleanCheck  = QPixmap(IconPath +"/cleancheck_icon.png")
        except:
            cmds.warning( "PolygonTools: Can't load icons for Texel Tab! Check icon files in pt_modules/icons directory.")

        MaxWidth = 370
        
        #Top Label
        self.lblInfo_01 = QLabel()
        self.lblInfo_01.setWordWrap(True)
        self.lblInfo_01.setMargin(2)
                
        #groupbox Prepare
        self.gboxGetTexel = QGroupBox("Get Texel Density")
        self.gboxGetTexel.setMaximumWidth(MaxWidth)
        self.gboxGetTexel_v_layout = QVBoxLayout()
        
        #groupbox Prepare
        self.gboxSetTexel = QGroupBox("Set Texel Density")
        self.gboxSetTexel.setMaximumWidth(MaxWidth)
        self.gboxSetTexel_v_layout = QVBoxLayout()     
        
        self.chkUseInUVI = QCheckBox()
        self.chkUseInUVI.setText("Use texel value when checking texel density")
        self.chkUseInUVI.setChecked(True)
        
        #Map Res label
        self.lblMapRes = QLabel("Map size (px)")
        
        #System Units cmbox
        self.cboxTexRes = QComboBox()
        self.cboxTexRes.addItems(["64", "128", "256x128", "256", "512x256", "512", "1024x512", "1024", "2048x1024", "2048", "4096x2048", "4096", "8192"])
        self.cboxTexRes.setMinimumWidth(90)
        
        self.btnCalcTex = QPushButton("Get Texel")
        self.btnCalcTex.setStyleSheet("color:#000000;background-color:#E1E1E1;")
        self.btnCalcTex.setMinimumWidth(90)
        self.btnCalcTex.setMinimumHeight(30)
        self.btnCalcTex.setIcon(iconGetTex)
        
        #set tex button
        self.btnSetTex = QPushButton("Set Texel")
        self.btnSetTex.setStyleSheet("color:#000000;background-color:#E1E1E1;")
        self.btnSetTex.setMaximumWidth(90)
        self.btnSetTex.setMinimumHeight(30)
        self.btnSetTex.setIcon(iconSetTex)
        
        self.edtSetTex = QLineEdit()
        self.edtSetTex.setFixedWidth(50)
        self.edtSetTex.setMaxLength(4)
        self.edtSetTex.setText("400")
        
        self.lblSetTexel = QLabel("Desired texel (px/m) ")
        self.lblSetTexel.setMaximumWidth(98)
        
        self.lblMapSize = QLabel("Map size: ")

        #end set block
        
        self.lblTexel = QLabel("Texel: ")
        self.lblTexel.setMaximumWidth(MaxWidth)
        self.lblTexel.setStyleSheet('background-color: black; padding: 5px;')
        
        #groupbox Prepare
        self.gboxCheckTexel = QGroupBox("Check Texel Density")
        self.gboxCheckTexel.setMaximumWidth(MaxWidth)
        self.gboxCheckTexel_v_layout = QVBoxLayout()     

        self.lblInRangeInfo = QLabel("Texel has not been checked yet.")
        self.lblInRangeInfo.setWordWrap(True)
        
        #Progress Bar
        self.pbChekProgress = QProgressBar()
        self.pbChekProgress.setValue(0)
        self.pbChekProgress.setMaximumWidth(MaxWidth)
        
        self.lblTexel02 = QLabel("Texel")
        #self.lblTexel02.setMaximumWidth(25)
        self.lblTexel02.setMaximumWidth(75)
        self.edtCurTexel = QLineEdit()
        self.edtCurTexel.setFixedWidth(50)
        self.edtCurTexel.setMaxLength(4)
        self.edtCurTexel.setText("256")
        
        #Btn
        self.btnCheckTexel = QPushButton("Check Texel")
        self.btnCheckTexel.setStyleSheet("color:#000000;background-color:#E1E1E1;")
        self.btnCheckTexel.setMinimumWidth(100)
        self.btnCheckTexel.setMaximumWidth(100)
        self.btnCheckTexel.setMinimumHeight(30)
        self.btnCheckTexel.setIcon(iconCheckTex)
        
        self.lblDiff = QLabel("Range +/- (%)")
        self.lblDiff.setFixedWidth(75)
        
        #Diff spinbox
        self.spnDiff = QSpinBox()
        self.spnDiff.setMinimum(1)
        self.spnDiff.setMaximum(30)
        self.spnDiff.setValue(10)
        
        #Texel label
        self.lblAddCheckHeader = QLabel("Additional Checks")
        
        self.lblTinyIt = QLabel("Tiny Polygons (m" + u'\N{SUPERSCRIPT TWO}'+")")
        self.lblTinyIt.setFixedWidth(95)
        
        self.edtTinyIt = QLineEdit()
        self.edtTinyIt.setFixedWidth(50)
        self.edtTinyIt.setMaxLength(7)
        self.edtTinyIt.setText("0.0001")
        
        self.lblPolyTinyAr = QLabel("Count: ")
        #self.lblPolyTinyAr.setMaximumWidth(120)
        self.lblPolyTinyAr.setVisible(False)
        
        self.btnSelectTinyFace = QPushButton("Not checked yet")
        self.btnSelectTinyFace.setMaximumWidth(160)
        
        self.lblTinyPX = QLabel("Tiny UV Shells (px)")
        self.lblTinyPX.setFixedWidth(95)
        
        self.edtTinyPX = QLineEdit()
        self.edtTinyPX.setFixedWidth(50)
        self.edtTinyPX.setMaxLength(1)
        self.edtTinyPX.setInputMask("D")
        self.edtTinyPX.setText("1")
        
        self.lblUVTinyAr = QLabel("Count: ")
        #self.lblUVTinyAr.setMaximumWidth(120)
        self.lblUVTinyAr.setVisible(False)
        
        self.btnSelectTinyUVShell = QPushButton("Not checked yet")
        self.btnSelectTinyUVShell.setMaximumWidth(160)

        #Btn                
        self.btnCleanCheck = QPushButton("Clean Check")
        self.btnCleanCheck.setStyleSheet("color:#000000;background-color:#E1E1E1;")
        self.btnCleanCheck.setMaximumWidth(100)
        self.btnCleanCheck.setMinimumWidth(100)
        self.btnCleanCheck.setMinimumHeight(30)
        self.btnCleanCheck.setIcon(iconCleanCheck)        
        
        self.gboxTexConclusion = QGroupBox("Conclusion")
        self.gboxTexConclusion.setStyleSheet("color:#ffffff; background-color:#2b2b2b;")
        self.gboxTexConclusion.setMaximumWidth(MaxWidth)
        self.gboxTexConclusion.setMinimumHeight(170)
        self.gboxTexConclusion_v_layout = QVBoxLayout()

        #conclusion text here
        self.txtbrowTexConclusion = QTextBrowser()
        self.txtbrowTexConclusion.setHtml("")
            
        self.gboxTexConclusion_v_layout.addWidget(self.txtbrowTexConclusion) 
        
        #Add to layout
        self.tabTex_v_layout.addWidget(self.lblInfo_01)
        
        #add texel group box
        self.tabTex_h_layout = QHBoxLayout()
        self.tabTex_h_layout.setAlignment(Qt.AlignLeft)
        self.tabTex_h_layout.setContentsMargins(0,0,0,0)
        self.tabTex_h_layout.setSpacing(10)

        self.tabTex_h_layout.addWidget(self.lblMapRes)
        self.tabTex_h_layout.addWidget(self.cboxTexRes)
        self.tabTex_h_layout.addWidget(self.btnCalcTex)
        
        self.gboxGetTexel_v_layout.addLayout(self.tabTex_h_layout)
        
        self.gboxGetTexel_v_layout.addWidget(self.lblTexel)
        self.gboxGetTexel_v_layout.addWidget(self.chkUseInUVI)
        
        #add texel group box
        self.tabTex_v_layout.addWidget(self.gboxGetTexel)
        self.gboxGetTexel.setLayout(self.gboxGetTexel_v_layout)
        
        self.gboxSetTexel_v_layout.addWidget(self.lblMapSize)

        self.tabTex_h_Setlayout = QHBoxLayout()
        self.tabTex_h_Setlayout.setAlignment(Qt.AlignLeft)
        self.tabTex_h_Setlayout.setContentsMargins(0,0,0,0)
        self.tabTex_h_Setlayout.setSpacing(10)
        
        self.gboxSetTexel_v_layout.addLayout(self.tabTex_h_Setlayout)
        
        self.tabTex_h_Setlayout.addWidget(self.lblSetTexel)
        self.tabTex_h_Setlayout.addWidget(self.edtSetTex)
        self.tabTex_h_Setlayout.addWidget(self.btnSetTex)
        
        #add SET texel group box
        self.tabTex_v_layout.addWidget(self.gboxSetTexel)
        self.gboxSetTexel.setLayout(self.gboxSetTexel_v_layout)
        
        self.gboxCheckTexel_v_layout.addWidget(self.lblInRangeInfo)
        self.gboxCheckTexel_v_layout.addWidget(self.pbChekProgress)
        
        #add layout for CurTexel
        self.tabTex_h_layout_02 = QHBoxLayout()
        self.tabTex_h_layout_02.setAlignment(Qt.AlignLeft)
        self.tabTex_h_layout_02.setSpacing(10)
        self.gboxCheckTexel_v_layout.addLayout(self.tabTex_h_layout_02)
        
        self.tabTex_h_layout_02.addWidget(self.lblTexel02)
        self.tabTex_h_layout_02.addWidget(self.edtCurTexel)
        
        #add layout for lblDiff
        self.tabTex_h_layout_03 = QHBoxLayout()
        self.tabTex_h_layout_03.setAlignment(Qt.AlignLeft)
        self.tabTex_h_layout_03.setSpacing(10)
        self.gboxCheckTexel_v_layout.addLayout(self.tabTex_h_layout_03)
        
        self.tabTex_h_layout_03.addWidget(self.lblDiff)
        self.tabTex_h_layout_03.addWidget(self.spnDiff)
        
        #add layout for CurTexel
        self.tabTex_h_layout_05 = QHBoxLayout()
        self.tabTex_h_layout_05.setAlignment(Qt.AlignLeft)
        self.tabTex_h_layout_05.setSpacing(10)
        self.tabTex_h_layout_05.setContentsMargins(0,0,0,10)
        self.gboxCheckTexel_v_layout.addLayout(self.tabTex_h_layout_05)
        
        self.tabTex_h_layout_05.addWidget(self.btnCheckTexel)
        self.tabTex_h_layout_05.addWidget(self.btnCleanCheck)
        
        self.tex_h_line_02 = QFrame()
        self.tex_h_line_02.setFrameShape(QFrame.HLine)
        self.tex_h_line_02.setFrameShadow(QFrame.Sunken)
        self.gboxCheckTexel_v_layout.addWidget(self.tex_h_line_02)
        
        self.gboxCheckTexel_v_layout.addWidget(self.lblAddCheckHeader)
        
        #add layout for TinyIt
        self.tabTex_h_layout_04 = QHBoxLayout()
        self.tabTex_h_layout_04.setAlignment(Qt.AlignLeft)
        self.tabTex_h_layout_04.setSpacing(10)
        self.gboxCheckTexel_v_layout.addLayout(self.tabTex_h_layout_04)
        
        self.tabTex_h_layout_04.addWidget(self.lblTinyIt)
        self.tabTex_h_layout_04.addWidget(self.edtTinyIt)
        self.tabTex_h_layout_04.addWidget(self.lblPolyTinyAr)
        self.tabTex_h_layout_04.addWidget(self.btnSelectTinyFace)
        
        #add layout for TinyPX
        self.tabTex_h_layout_05 = QHBoxLayout()
        self.tabTex_h_layout_05.setAlignment(Qt.AlignLeft)
        self.tabTex_h_layout_05.setSpacing(10)
        self.gboxCheckTexel_v_layout.addLayout(self.tabTex_h_layout_05)
        
        self.tabTex_h_layout_05.addWidget(self.lblTinyPX)
        self.tabTex_h_layout_05.addWidget(self.edtTinyPX)
        self.tabTex_h_layout_05.addWidget(self.lblUVTinyAr)
        self.tabTex_h_layout_05.addWidget(self.btnSelectTinyUVShell)
                        
        #group Check
        self.tabTex_v_layout.addWidget(self.gboxCheckTexel)
        self.gboxCheckTexel.setLayout(self.gboxCheckTexel_v_layout)
        
        #conclusion
        self.gboxTexConclusion.setLayout(self.gboxTexConclusion_v_layout)
        
        #conclusion area
        self.tabTex_v_layout.addWidget(self.gboxTexConclusion)

        
        #------------- SIGNALS ----------------------------------
        self.cboxTexRes.activated.connect(self.textureResChange)

        #Calculate Texel
        self.btnCalcTex.clicked.connect(self.btnCalcTexClicked)

        #SetTexel
        self.btnSetTex.clicked.connect(self.btnSetTexelClicked)

        #changes in texel
        self.edtCurTexel.editingFinished.connect(self.checkTexelValue)

        self.edtSetTex.editingFinished.connect(self.checkDesiredTexel)

        #check texel
        self.btnCheckTexel.clicked.connect(self.btnCheckTexelClicked)

        #clean result
        self.btnCleanCheck.clicked.connect(self.btnCleanCheckClicked)    

        #sel tiny uv and geo
        self.btnSelectTinyFace.clicked.connect(self.btnSelectTinyFacesClicked)
        self.btnSelectTinyUVShell.clicked.connect(self.btnSelectTinyUVShellsClicked)

        #changes in Tiny Face
        self.edtTinyIt.textChanged.connect(self.tinyChanged)
        self.edtTinyIt.editingFinished.connect(self.tinyFinEdit)

        #changes in TinyPX
        self.edtTinyPX.editingFinished.connect(self.tinyPXFinEdit)

        #changes in diff
        self.spnDiff.editingFinished.connect(self.diffFinEdit)

        self.checkTexelValues()
        
        #arrays for mistakes
        self.tiny_uv_arr=[]
        self.tiny_geo_arr=[]
        
        self.btnSelectTinyFace.setDisabled(True)
        self.btnSelectTinyUVShell.setDisabled(True)
        
        self.checkSquareMap()
        
        self.lblInfo_01.setText("Texel operations not yet performed!")
        
        #lang selector
        current_languge = cfgl.configLoader()[14]
        self.txtbrowTexConclusion.setHtml( conclusion.texTabIntroConclusion(current_languge) )


    def showInfo(self, info_type, info_text):

        #trim lables
        if len(info_text) > 70:
            short_info_text = info_text[:70] + "..."
        else:
            short_info_text = info_text
        
        if info_type == "info":
            self.lblInfo_01.setText(short_info_text)
            self.lblInfo_01.setStyleSheet("background-color:#3D523D;")
            print ("\nPolygonTools:", info_text)
        
        if info_type == "warn":
            self.lblInfo_01.setText(short_info_text)
            self.lblInfo_01.setStyleSheet("background-color:#916666;")
            print ("\nPolygonTools:", info_text)

    #res changer
    def textureResChange(self):
        path_config = cfgl.configLoader()[99:101]
        current_resolution_value = str(self.cboxTexRes.currentIndex())
        cfgl.ConfigWriter('Texel', 'Map_resolution', current_resolution_value, path_config[0], path_config[1])
        
        #check Square or Not
        self.checkSquareMap()  

    #square map checker
    def checkSquareMap(self):
        try:
            mapres = int(self.cboxTexRes.currentText())
            
            self.btnSetTex.setEnabled(True)
            self.edtSetTex.setEnabled(True)
            self.lblMapSize.setText("Map size: " + self.cboxTexRes.currentText() + "px")
        except:
            self.btnSetTex.setEnabled(False)
            self.edtSetTex.setEnabled(False)
            self.lblMapSize.setText("Map size: Please select square map! Now it\'s " + self.cboxTexRes.currentText())


    def checkTexelValue(self):
        try:
            self.lblInfo_01.setText("")
            
            #Write to config
            path_config = cfgl.configLoader()[99:101]
            current_texel_value = self.edtCurTexel.text()
            cfgl.ConfigWriter('In-Range', 'Texel', current_texel_value, path_config[0], path_config[1])
            
        except:
            self.showInfo ("warn", "Please input correct Integer value in range 1-10000. Now default value (256) was returned.")
            self.edtCurTexel.setText("256")


    #on loading check
    def checkTexelValues(self):
        
        #current values
        current_texel = self.edtCurTexel.text()
        current_diff = str(self.spnDiff.value())
        current_tinyit = self.edtTinyIt.text()
        current_tinypx = self.edtTinyPX.text()
        current_desired_texel = self.edtSetTex.text()
        
        #load data from config
        data_from_config = cfgl.configLoader()[0:12]
        
        #values from config
        config_resolution = int(data_from_config[0])
        config_texel = data_from_config[1] 
        config_diff = data_from_config[2]
        config_tinyit = data_from_config[3]
        config_tinypx = data_from_config[4]
        config_desired_texel = data_from_config[11]
                         
        #compare values
        self.cboxTexRes.setCurrentIndex(config_resolution)
        
        #change values if need
        
        #setcurtexel
        if current_texel != config_texel:
             self.edtCurTexel.setText(config_texel)
        
        #set diff
        if current_diff != config_diff:
             self.spnDiff.setValue(int(config_diff))

        #set tinyit
        if current_tinyit != config_tinyit:
             self.edtTinyIt.setText(config_tinyit)

        #set tinypx
        if current_tinypx != config_tinypx:
             self.edtTinyPX.setText(config_tinypx)
        
        #set desired_texel     
        if current_desired_texel != config_desired_texel:
             self.edtSetTex.setText(config_desired_texel)

    #calc texel        
    def btnCalcTexClicked(self):

        

        #get current language
        current_languge = cfgl.configLoader()[14]
        
        SelectedTextureIndex = int(self.cboxTexRes.currentIndex())
        SelectedTextureArea = resolutionSelected(SelectedTextureIndex)

        #getselection
        try:
            selection_array = gen_func.checkSelection()

            sel_objects = selection_array[0]
            sel_editable_poly_objects = selection_array[1]
            sel_editable_poly_nodes = selection_array[3]

        except:
            print ("Please select something. Editable Poly object for example...")
        
        #if many selection - 1 obj selected
        if len(sel_editable_poly_nodes) > 1:

            #get node
            NodeName = sel_editable_poly_nodes[0]
            
            #select Node
            rt.select(NodeName)

            print ("PolygonTools: Random object selected to check Texel.")
        ObjectHasTransform = False  
        
        if len(sel_editable_poly_nodes) != 0:
            #0-randomPoly, uv_area[0], geo_area, cur_work_units, gp_ratio, 5-texel            
            texelData = calculateTexel(SelectedTextureArea, sel_editable_poly_nodes[0])

            #get scale transform
            ScaleXYZ = sel_editable_poly_nodes[0].scale                        
            if sum(ScaleXYZ) != 3.0:
                ObjectHasTransform = True            

        else:
            texelData = False
            
        if texelData != False:
        
            print ("PolygonTools: TEXEL STATISTICS\n"    )
    
            print ("\tUV-Face Area: "+ str(texelData[1]))  
            print ("\tGeo-Face Area: " + str(texelData[2]) + " meters" + u'\N{SUPERSCRIPT TWO}')     
            print ("\tTexture size: " + self.cboxTexRes.currentText() +" px") 
            print ("\tTexture area: " + str(SelectedTextureArea) +" px")
        
            #change edit and slider is Checker is ON
            if (texelData[5] == 0.0) and (self.chkUseInUVI.isChecked() ==True):
                self.edtCurTexel.setText("1")
            
            if self.chkUseInUVI.isChecked()==True:   
                self.edtCurTexel.setText(str(int(texelData[5])))        
            
            if ObjectHasTransform == False:
                self.lblTexel.setText("Texel: " + str(int(texelData[5])) + " px/meter | Current System Units is: " + texelData[3])
                self.lblTexel.setStyleSheet('background-color: black; padding: 5px;') 
            else:
                self.lblTexel.setText("Texel: " + str(int(texelData[5])) + " px/meter | Units: " + texelData[3] + " | Object with Scale Transform!")
                self.lblTexel.setStyleSheet('background-color: #9e0b0f; padding: 5px;')

            print ('\t', self.lblTexel.text(), '\n')

            if texelData[0] == False:
                self.lblInfo_01.setText("Texel successfully calculated for Selected polygon.")
                self.lblInfo_01.setStyleSheet("background-color:#3D523D;")
                #set conclusion text
                conclusion_text = conclusion.calcTexelConclusion(current_languge, int(texelData[5]), True)
            else:
                self.lblInfo_01.setText("Texel successfully calculated for Random polygon.")
                self.lblInfo_01.setStyleSheet("background-color:#916666;")
                #set conclusion text
                conclusion_text = conclusion.calcTexelConclusion(current_languge, int(texelData[5]), False)
                
            print (self.lblInfo_01.text()    )
    
            #conclusion output
            self.txtbrowTexConclusion.setHtml(conclusion_text)        
            
        else:
            self.lblInfo_01.setText("Can't Get Texel. Please select at least one Face on one Object!")
            self.lblInfo_01.setStyleSheet("background-color:#916666;")
            print (self.lblInfo_01.text())
            
            conclusion_text = conclusion.noSelection(current_languge, "check_texel")
            self.txtbrowTexConclusion.setHtml(conclusion_text) 


    #set texel
    def btnSetTexelClicked (self):

        

        #get current language
        current_languge = cfgl.configLoader()[14]

        SelectedTextureIndex = int(self.cboxTexRes.currentIndex())
        SelectedTextureArea = resolutionSelected(SelectedTextureIndex)
        MapResValue = self.cboxTexRes.currentText()

        #getselection
        try:
            selection_array = gen_func.checkSelection()

            sel_objects = selection_array[0]
            sel_editable_poly_objects = selection_array[1]
            sel_editable_poly_nodes = selection_array[3]

        except:
            print ("Please select something. Editable Poly object for example...")

        if len(sel_editable_poly_nodes) > 0:

            SelectedNodes = rt.selection	
            
            for i in range(len(sel_editable_poly_nodes)):

                NodeName = sel_editable_poly_nodes[i]

                rt.execute ("setCommandPanelTaskMode #modify")
                
                #select Node
                rt.select(NodeName)

                texel_data = calculateTexel(SelectedTextureArea, NodeName)

                Texel = texel_data[5]
                DesiredTexel = int(self.edtSetTex.text())
                Ratio = str((float(DesiredTexel/Texel)))

                rt.select(NodeName)

                rt.subobjectLevel = 4
                rt.execute ("max select all")
                rt.execute ("modPanel.addModToSelection (Unwrap_UVW ())")    
                rt.execute ("unwrapmod = modpanel.getcurrentobject(); unwrapmod.scaleSelectedCenter "  + Ratio + " 0")
                rt.execute ("macros.run \"Modifier Stack\" \"Convert_to_Poly\"")

                print (NodeName.name + ". Texel has been set to " + self.edtSetTex.text() + " px/m for map size " + MapResValue + "x" + MapResValue + "px\n")

            #check outside
            uvOutsideData = gen_func.uvRangeStat(sel_editable_poly_nodes)
            
            if uvOutsideData[1] != []:
                shapesOutside = False
            else:
                shapesOutside = True                                  
                                
            #conclusion output
            conclusion_text = conclusion.setTexelConclusion(current_languge, int(self.edtSetTex.text()), shapesOutside, len(sel_editable_poly_nodes))
            self.txtbrowTexConclusion.setHtml(conclusion_text)        
            
            self.lblInfo_01.setText("The number of objects on which the texel is changed: " + str(len(sel_editable_poly_nodes)) + "\n" + "Texel has been set to " + self.edtSetTex.text() + " px/m for map size " + MapResValue + "x" + MapResValue + "px")
            self.lblInfo_01.setStyleSheet("background-color:#3D523D;")
            print ("\nPolygonTools:", self.lblInfo_01.text())

            #return selection
            rt.select(SelectedNodes)

        else:
            self.lblInfo_01.setText("Can't Set Texel. Please select one Editable Poly Object.")
            self.lblInfo_01.setStyleSheet("background-color:#916666;")
            
            conclusion_text = conclusion.noSelection(current_languge, "set_texel")
            self.txtbrowTexConclusion.setHtml(conclusion_text) 


    def btnCheckTexelClicked(self):

        

        GreenBox =  ("<font color='#80ff80'>" + u'\N{Full Block}' + "</font> In-Range: ")
        BlueBox =  (u'\N{BOX DRAWINGS LIGHT VERTICAL}' + " <font color='#80c0ff'>" + u'\N{Full Block}' + "</font> Streched: ")
        RedBox =  (u'\N{BOX DRAWINGS LIGHT VERTICAL}' + "<font color='#ffc0c0'>" + u'\N{Full Block}' + "</font> Compressed: ")

        self.lblInfo_01.setText("")
        self.checkTexelValue()
        
        self.btnSelectTinyUVShell.setDisabled(True)
        self.btnSelectTinyFace.setDisabled(True)

        #lang
        current_languge = cfgl.configLoader()[14]        

        #getselection
        try:
            
            selection_array = gen_func.checkSelection()

            sel_objects = selection_array[0]
            sel_editable_poly_objects = selection_array[1]
            sel_editable_poly_nodes = selection_array[3]

        except:
            
            print ("Please select something. Editable Poly object for example...")

        if len(sel_editable_poly_nodes) > 0:
                        
            #turn on vertex color
            for i in range(len(sel_editable_poly_nodes)):
                sel_editable_poly_nodes[i].showVertexColors = True
            
            #get selected texture
            SelTexIndex = int(self.cboxTexRes.currentIndex())
            
            print ("PolygonTools: CHECK TEXEL DENSITY\n")
            
            current_time = time.strftime("%H:%M:%S ", time.localtime())
            print ("Check Start at", current_time, '\n')

            #texture area
            SelectedTextureIndex = int(self.cboxTexRes.currentIndex())
            SelectedTextureArea = resolutionSelected(SelectedTextureIndex)
            
            #get curent texel
            CurrentTexel = float(self.edtCurTexel.text())
                            
            #get curent diff
            DifferenceMargin = float(self.spnDiff.value())
                                                        
            #get current tiny
            TinyPolygonArea = float(self.edtTinyIt.text())            
            
            CurrentTinyUVValue = int(self.edtTinyPX.text())
            print ("Current Tiny UV:", CurrentTinyUVValue)
            
            SelectedResolution = self.cboxTexRes.currentText()  

            #main func
            #0-global_inrange_arr, global_streched_arr, global_compressed_arr, global_tiny_uv_arr, 4-global_tiny_geo_arr        
            check_texel_data = CheckTexel (sel_editable_poly_nodes, SelectedTextureIndex, CurrentTexel, DifferenceMargin, TinyPolygonArea, SelectedResolution, CurrentTinyUVValue, True)

            correct = []
            streched = []
            compressed = []
            
            self.tiny_uv_arr = []
            self.tiny_geo_arr = []
            
            for k in range(len(sel_editable_poly_nodes)):                
                for i in range(len(check_texel_data)):
                    if i == 0:
                        correct.append(len(check_texel_data[i][k]))
                    if i == 1:                        
                        streched.append(len(check_texel_data[i][k]))
                    if i == 2:
                        compressed.append(len(check_texel_data[i][k]))
                    if i == 3:
                        if check_texel_data[i][k] != [[], []]:
                            self.tiny_uv_arr.append(check_texel_data[i][k])                            
                    if i == 4:
                        if check_texel_data[i][k] != [[], []]:
                            self.tiny_geo_arr.append(check_texel_data[i][k])                

            self.pbChekProgress.setValue(100)
            
            TinyFace = False
            TinyUV = False
            
            if self.tiny_uv_arr == []:
                self.btnSelectTinyUVShell.setDisabled(True)
                self.btnSelectTinyUVShell.setText("Tiny UV Shells not detected!")
            elif self.tiny_uv_arr != [[[], []]] and len(sel_editable_poly_nodes) == 1:
                self.btnSelectTinyUVShell.setDisabled(False)
                self.btnSelectTinyUVShell.setText("Select " + str(len(self.tiny_uv_arr[0][1])) + " tiny UV Shell(s)")
                TinyUV = True
            elif self.tiny_uv_arr != [[[], []]]:
                self.btnSelectTinyUVShell.setText("Tiny UV Shells on " + str(len(self.tiny_uv_arr)) + " objects")
                self.btnSelectTinyUVShell.setDisabled(False)
                TinyUV = True
                        
            if self.tiny_geo_arr == []:
                self.btnSelectTinyFace.setDisabled(True)
                self.btnSelectTinyFace.setText("Tiny faces not detected!")
            elif self.tiny_geo_arr != [[[], []]] and len(sel_editable_poly_nodes) == 1:
                self.btnSelectTinyFace.setDisabled(False)
                self.btnSelectTinyFace.setText("Select " + str(len(self.tiny_geo_arr[0][1])) + " tiny face(s)")
                TinyFace = True
            elif self.tiny_geo_arr != [[[], []]]:
                self.btnSelectTinyFace.setText("Tiny faces on " + str(len(self.tiny_geo_arr)) + " objects")
                self.btnSelectTinyFace.setDisabled(False)
                TinyFace = True
                                                
            LongText = ("Check texel density complete! Number of checked objects: " + str(len(sel_editable_poly_objects)) + " See log for details.")
            self.showInfo("info", LongText)                

            self.lblInRangeInfo.setText(GreenBox + str(sum(correct)) + RedBox + str(sum(streched)) + BlueBox + str(sum(compressed)))
            print ("\nStatistics:", ("\n\tCorrect - " + str(sum(correct)) + "\n\tStreched - " + str(sum(streched)) + "\n\tCompressed - " + str(sum(compressed))))
            
            print ("\nObjects with Tiny geometry area:", len(self.tiny_geo_arr))
            
            print ("\nObjects with Tiny UV Shells:", len(self.tiny_uv_arr))

            current_time = time.strftime("%H:%M:%S ", time.localtime())
            print ("\nCheck complete at", current_time, '\n')

            conclusion_text = conclusion.checkTexelConclusion(current_languge, DifferenceMargin, correct, streched, compressed, TinyUV, TinyFace)
            self.txtbrowTexConclusion.setHtml(conclusion_text) 

            rt.select(sel_editable_poly_nodes)

        else:
            self.showInfo("warn", "Can't Check Texel. Please select Editable Poly object(s).")

            self.cleanTexelCheck("Check")

            conclusion_text = conclusion.noSelection(current_languge, "check_texel")
            self.txtbrowTexConclusion.setHtml(conclusion_text) 


    #clean check
    def btnCleanCheckClicked(self):

        

        #lang
        current_languge = cfgl.configLoader()[14]        

        #getselection
        try:
            selection_array = gen_func.checkSelection()
            sel_objects = selection_array[0]
            sel_editable_poly_objects = selection_array[1]

        except:
            print ("Please select something. Editable Poly object for example...")

        if len(sel_editable_poly_objects) > 0:            
            
            try:
                #turn off vertex color
                for i in range(len(sel_editable_poly_objects)):
                    rt.execute("$" + sel_editable_poly_objects[i] + ".showVertexColors = off")

                self.cleanTexelCheck("Clean")
                self.showInfo("info", "Check Texel Density results have been cleared!")

                conclusion_text = conclusion.CleanCheckClicked(current_languge, True)
                self.txtbrowTexConclusion.setHtml(conclusion_text)
            except:
                self.showInfo("warn", "There is nothing to clean! Try to clean after checking.")
                
                conclusion_text = conclusion.CleanCheckClicked(current_languge, False)
                self.txtbrowTexConclusion.setHtml(conclusion_text)
        else:
            self.showInfo("warn", "Can't clean check texel density results. Please select already checked Editable Poly object.")

            self.cleanTexelCheck("Check")
            
            conclusion_text = conclusion.noSelection(current_languge, "clean_check")
            self.txtbrowTexConclusion.setHtml(conclusion_text) 

        rt.execute ("redrawViews()")

    #clean
    def cleanTexelCheck(self, CleanType):

        if CleanType == "Clean":
            self.lblInRangeInfo.setText("Previous check results have been cleared!")

        if CleanType == "Check":
            self.lblInRangeInfo.setText("Texel has not been checked yet.")
        
        self.btnSelectTinyUVShell.setText("Not checked yet")
        self.btnSelectTinyFace.setText("Not checked yet")
        
        self.btnSelectTinyFace.setDisabled(True)
        self.btnSelectTinyUVShell.setDisabled(True)
        
        self.tiny_uv_arr = []
        self.tiny_geo_arr = []
        
        self.pbChekProgress.setValue(0)

    #desired
    def checkDesiredTexel(self):
        try:
            texel = (float(self.edtSetTex.text())/100)
            
            if (texel<0.01):
                self.setTexelWarningText()
            
            #Write to config
            path_config = cfgl.configLoader()[99:101]
            current_desired_texel = self.edtSetTex.text()
            cfgl.ConfigWriter('Texel', 'desired_texel', current_desired_texel, path_config[0], path_config[1])        
                            
        except:
            self.setTexelWarningText()        

    def setTexelWarningText(self):
            cmds.warning("Please input correct Integer value in range 1-9999. Now default value (400) was returned.")
            self.lblInfo_01.setText("Please input correct Integer value in range 1-9999. Now default value (400) was returned.")
            self.edtSetTex.setText("400")


    #select tiny Faces    
    def btnSelectTinyFacesClicked (self):

        
        
        current_languge = cfgl.configLoader()[14]

        #for selection
        obj_with_tiny_faces = []
        
        if len(self.tiny_geo_arr) == 1:
            
            NodeName = self.tiny_geo_arr[0][0][0] 
            Faces = self.tiny_geo_arr[0][1]

            if str(NodeName) != "None":
                
                try:
                    #select Node
                    rt.select(NodeName)
                    rt.execute ("subobjectLevel = 4")

                    #select faces
                    SelectedFaces = ','.join([str(elements) for elements in Faces])
                    rt.execute ("$.EditablePoly.SetSelection #Face #{" + SelectedFaces +"}")
                    print ("Polygon(s) with Tiny Faces was selected.\nTheir numbers:", SelectedFaces)
                    rt.execute ("actionMan.executeAction 0 \"272\"")

                    self.showInfo ("info", "Tiny Faces was selected.")

                    conclusion_text = conclusion.selectTinyConclusion(current_languge, "Face", True)
                    self.txtbrowTexConclusion.setHtml(conclusion_text)

                except:
                    
                    self.showInfo ("warn", "Can not select Tiny Faces. Object(s) is not Exists or other problems.")
                    self.btnSelectTinyFace.setDisabled(True)
                    self.btnSelectTinyFace.setText("Not checked yet")

                    conclusion_text = conclusion.selectTinyConclusion(current_languge, "Face", False)
                    self.txtbrowTexConclusion.setHtml(conclusion_text)                 
        else:
            #clear selection
            rt.clearSelection()
            
            for i in range(len(self.tiny_geo_arr)):

                NodeName = self.tiny_geo_arr[i][0][0]      
                try:
                    
                    obj_with_tiny_faces.append(NodeName )
                
                except:
                    
                    print ("\tCan't select polygon(s) with Tiny Faces", self.tiny_geo_arr[i][0][0] ,"is not Exists or other problems.")
                                
            if len(obj_with_tiny_faces) > 0:

                try:
                
                    rt.select(obj_with_tiny_faces)
                    print ("Object with Polygon(s) with Tiny Faces was selected! It's:")
                    for i in range(len(obj_with_tiny_faces)):
                        print ('\t', (str(i+1) + "."), obj_with_tiny_faces[i].name)
                    self.showInfo ("info", "Object with Polygon(s) with Tiny Faces was selected!")
                
                except:
                
                    print ("EXCEPTION in 'btnSelectTinyFacesClicked' function. Can't select Polygon(s) with Tiny Faces. Object(s) is not Exists or other problems.")
                    self.btnSelectTinyFace.setDisabled(True)      
                    self.btnSelectTinyFace.setText("Not checked yet")

                    conclusion_text = conclusion.selectTinyConclusion(current_languge, "Face", False)
                    self.txtbrowTexConclusion.setHtml(conclusion_text)                 

    #select tiny UV
    def btnSelectTinyUVShellsClicked (self):

        
        
        current_languge = cfgl.configLoader()[14]

        #for selection
        obj_with_tiny_uv = []
        
        if len(self.tiny_uv_arr) == 1:

            #ObjectName = self.tiny_uv_arr[0][0][0]
            NodeName = self.tiny_uv_arr[0][0][0] 
            Faces = self.tiny_uv_arr[0][1]

            if str(NodeName) != "None":
                
                try:
                    #select Node
                    rt.select(NodeName)

                    #select faces
                    SelectedFaces = ','.join([str(elements) for elements in Faces])
                    
                    rt.execute ("actionMan.executeAction 0 \"272\"")

                    #turn on modifier
                    rt.execute ("max modify mode")
                    
                    if len(NodeName.modifiers) == 0:
                        rt.execute ("modPanel.addModToSelection (Unwrap_UVW ()) ui:on")
                    
                    rt.execute ("$.modifiers[#unwrap_uvw].unwrap.move ()")
                    rt.execute ("subobjectLevel = 3")
                    rt.execute ("$.modifiers[#unwrap_uvw].unwrap6.selectFacesByNode #{" + SelectedFaces + "} $")
                                    
                    print ("Polygon(s) with Tiny UV Shells was selected.\nTheir numbers:", SelectedFaces)
                    
                    self.showInfo ("info", "Tiny UV Shells was selected.")

                    conclusion_text = conclusion.selectTinyConclusion(current_languge, "UV", True)
                    self.txtbrowTexConclusion.setHtml(conclusion_text) 
                
                except:
                
                    self.showInfo ("warn", "Can't select Tiny UV Shells. Object(s) is not Exists or other problems.")
                    self.btnSelectTinyUVShell.setDisabled(True)
                    self.btnSelectTinyUVShell.setText("Not checked yet")

                    conclusion_text = conclusion.selectTinyConclusion(current_languge, "UV", False)
                    self.txtbrowTexConclusion.setHtml(conclusion_text)                 
        
        else:
            #clear sel
            rt.clearSelection()
            
            for i in range(len(self.tiny_uv_arr)):
                       
                NodeName = self.tiny_uv_arr[i][0][0] 
                
                try:
                
                    obj_with_tiny_uv.append(NodeName)
                
                except:
                
                    print ("\tCan't select polygon(s) with Tiny Faces", self.tiny_uv_arr[i][0][0] ,"is not Exists or other problems.")
                                
            if len(obj_with_tiny_uv) > 0:
                
                try:
                
                    rt.select(obj_with_tiny_uv)
                    print ("Object with Polygon(s) with Tiny UV Shells was selected! It's:")
                    for i in range(len(obj_with_tiny_uv)):
                        print ('\t', (str(i+1) + "."), obj_with_tiny_uv[i].name)

                    self.showInfo ("info", "Object with Polygon(s) with Tiny UV Shells was selected!")
                
                except:
                
                    print ("EXCEPTIOn in 'btnSelectTinyUVShellsClicked' function. Can't select Polygon(s) with Tiny UV Shells. Object(s) is not Exists or other problems.")
                    self.btnSelectTinyUVShell.setDisabled(True)      
                    self.btnSelectTinyUVShell.setText("Not checked yet")

                    conclusion_text = conclusion.selectTinyConclusion(current_languge, "UV", False)
                    self.txtbrowTexConclusion.setHtml(conclusion_text)                 

    #Diff changes
    def diffFinEdit(self):
        #Write to config
        path_config = cfgl.configLoader()[99:101]
        current_diff_value = str(self.spnDiff.value())
        cfgl.ConfigWriter('In-Range', 'Difference', current_diff_value, path_config[0], path_config[1])

    #Tiny UV
    def tinyPXFinEdit(self):
        #Write to config
        path_config = cfgl.configLoader()[99:101]
        current_tiny_value = self.edtTinyPX.text()
        cfgl.ConfigWriter('In-Range', 'Tiny UV', current_tiny_value, path_config[0], path_config[1])

    #problems with Tiny I Fixer   
    def tinyWarning(self):
        self.showInfo ("warn", "Please input correct Float value in range 0.0001-1000. Now default value (0.0001) was returned.")
        self.edtTinyIt.setText("0.0001")            

    #Tiny Face   
    def tinyChanged(self):
        try:
            tiny_it = float(self.edtTinyIt.text())
            
            if (tiny_it < 0.0001) or (tiny_it > 1000):
                self.tinyWarning()
        except:
            self.tinyWarning()
    
    #Tiny Face
    def tinyFinEdit(self):
        try:
            tiny_it = float(self.edtTinyIt.text())
            
            if (tiny_it<0.0001) or (tiny_it>1000):
                self.tinyWarning()
            
            #Write to config
            path_config = cfgl.configLoader()[99:101]
            current_tinit_value = self.edtTinyIt.text()
            cfgl.ConfigWriter('In-Range', 'Tiny_it', current_tinit_value, path_config[0], path_config[1])
                            
        except:
            self.tinyWarning()



def CheckTexel (sel_editable_poly_nodes, SelectedTextureIndex, CurrentTexel, DifferenceMargin, TinyPolygonArea, SelectedResolution, CurrentTinyUVValue, Colorize):

    

    SelectedNodes = rt.selection

    #texture area
    SelectedTextureArea = resolutionSelected(SelectedTextureIndex)
    print ("Selected Texture Area:", SelectedTextureArea)
    
    #distortion value
    DistortionValue = (CurrentTexel/100)*DifferenceMargin
    print ("Tolerance from the current texel value:", DistortionValue, '\n')

    print ("Texel:")

    #hi texel range
    HiTexelValue = CurrentTexel + DistortionValue
    print ("\tHighest -", HiTexelValue)
    
    print ("\tCurrent -", CurrentTexel)
    
    #low texel range
    LowTexelValue = CurrentTexel - DistortionValue
    print ("\tLowest -", LowTexelValue, '\n')

    #get 1 pixel area for current map
    TinyPixelValue = Decimal(1.0/SelectedTextureArea)
    #print ("tinyPixelValue", tinyPixelValue     )
    print ("1 pixel area for " + SelectedResolution + " texture is " + str(TinyPixelValue )) 

    CurrentTinyHeightWidth  = ((1.0/math.sqrt(SelectedTextureArea)*CurrentTinyUVValue))
    print ("Tiny Height or Width:", CurrentTinyHeightWidth)

    print ("-----------------------------------------")
    
    #global arrays
    global_inrange_arr =[]
    global_streched_arr =[]
    global_compressed_arr =[]
    global_tiny_uv_arr = []
    global_tiny_geo_arr = []        

    #get selection
    SelNodes = rt.selection
    rt.execute("max modify mode")

    for i in range(len(sel_editable_poly_nodes)):
        
        NodeName = sel_editable_poly_nodes[i] 

        #select Node
        rt.select(NodeName)

        rt.subobjectLevel = 4
        rt.execute("$.EditablePoly.SetSelection #Face #{}")
        rt.subobjectLevel = 0

        #get polycount
        CurrentObjectPolycount = NodeName.faces.count
    
        #arrays for polygons            
        in_range_arr = []
        streched_arr = []
        compressed_arr = []

        #array for tiny uv
        tiny_uv_arr = [0] * 2
        for z in range(2):
            tiny_uv_arr[z] = [] * 1

        #array for tiny geo
        tiny_geo_arr = [0] * 2
        for z in range(2):
            tiny_geo_arr[z] = [] * 1
        
        error_arr = []

        #turn on modifier
        
        rt.execute ("modPanel.addModToSelection (Unwrap_UVW ())")
        
        for l in range(0, CurrentObjectPolycount): 
            
            SelectedFaceNumber = l + 1
            
            #selected face name
            SelectedFaceName = str(SelectedFaceNumber)
            
            rt.execute ("unwrapmod = modpanel.getcurrentobject(); unwrapmod.getarea #{" + SelectedFaceName + "} &mX &mY &mWidth &mHeight &AreaUVW &AreaGeom")
            
            SelectedFaceUVArea = rt.AreaUVW
            
            #UV Area
            DecimalUVArea = Decimal(rt.AreaUVW)

            #get geo area
            GeoArea = rt.AreaGeom

            #get width height
            HeightUVElement = rt.mHeight
            WidthUVElement = rt.mWidth
            
            #check area and W and H of uv and compare with user value
            if (DecimalUVArea < TinyPixelValue) or (HeightUVElement <= CurrentTinyHeightWidth ) or (WidthUVElement <= CurrentTinyHeightWidth):
                #add name
                if sel_editable_poly_nodes[i] not in tiny_uv_arr[0]:
                    tiny_uv_arr[0].append(sel_editable_poly_nodes[i] )
                #add face
                tiny_uv_arr[1].append(SelectedFaceName)

            #check geo area with user value
        
            if GeoArea <= TinyPolygonArea:
                #add name
                if sel_editable_poly_nodes[i] not in tiny_geo_arr[0]:
                    tiny_geo_arr[0].append(sel_editable_poly_nodes[i] )
                #add face
                tiny_geo_arr[1].append(SelectedFaceName)

            #get gpratio
            try:
                UVGeoRatio = math.sqrt(SelectedFaceUVArea/GeoArea)
            except:
                UVGeoRatio = 0
                error_arr.append(SelectedFaceNumber)

            #get texel
            TexelValue = math.ceil (UVGeoRatio*(math.sqrt(SelectedTextureArea)))

            #texel equal Inrange
            if (TexelValue <= HiTexelValue) and (TexelValue >= LowTexelValue):
                in_range_arr.append(SelectedFaceName)                
            
            #texel bigger Streched   
            if TexelValue > HiTexelValue:
                streched_arr.append(SelectedFaceName)
            
            #texel smaller Compressed
            if TexelValue < LowTexelValue:
                compressed_arr.append(SelectedFaceName)

        print ('\n', (str(i) + "."), "Information for", sel_editable_poly_nodes[i].name)

        Correct = ','.join([str(elements) for elements in in_range_arr])
        Streched = ','.join([str(elements) for elements in streched_arr])
        Compressed = ','.join([str(elements) for elements in compressed_arr])

        rt.select(sel_editable_poly_nodes[i]) 

        #paint polygons
        if Colorize == True:                                
            try:                
                rt.execute ("$.EditablePoly.SetSelection #Face #{" + Correct + "}")
                rt.execute ("$.SetFaceColor (color 32 255 32) #VertexColor")
            except:
                pass
            
            try:
                rt.execute ("$.EditablePoly.SetSelection #Face #{" + Streched + "}")
                rt.execute ("$.SetFaceColor (color 255 128 128) #VertexColor")
            except:
                pass   
    
            try:
                rt.execute ("$.EditablePoly.SetSelection #Face #{" + Compressed + "}")
                rt.execute ("$.SetFaceColor (color 32 255 255) #VertexColor")
            except:
                pass
                
        try:
            print ("\tIn-Range:", len(in_range_arr))
        except:
            print ("\tIn-Range: 0")
            
        try:
            print ("\tStreched:", len(streched_arr))
        except:
            print ("\tStreched: 0")

        try:
            print ("\tCompressed:", len(compressed_arr))
        except:
            print ("\tCompressed: 0")

        try:
            if tiny_uv_arr != [[], []]:
                print ("\tTiny UV Shells:", len(tiny_uv_arr[1]))
            else:
                print ("\tTiny UV Shells: 0")
        except:
            print ("\tTiny UV Shells: 0")

        try:
            if tiny_geo_arr != [[], []]:
                print ("\tTiny Faces:", len(tiny_geo_arr[1]))
            else:
                print ("\tTiny Faces: 0")
        except:
            print ("\tTiny Faces: 0")

        try:
            if len(error_arr) > 0:
                print ("\tProblem with geometry area of selected face! Object Name:", sel_editable_poly_nodes[i].name, "| Face # array:", error_arr)
        except:
            pass

        #to poly
        rt.execute ("macros.run \"Modifier Stack\" \"Convert_to_Poly\"")

        #global arrays
        global_inrange_arr.append ( in_range_arr )
        global_streched_arr.append ( streched_arr )
        global_compressed_arr.append ( compressed_arr )        
        global_tiny_uv_arr.append ( tiny_uv_arr )
        global_tiny_geo_arr.append ( tiny_geo_arr )         

    #return selection
    rt.select(SelectedNodes)

    return  global_inrange_arr, global_streched_arr, global_compressed_arr, global_tiny_uv_arr, global_tiny_geo_arr        


def calculateTexel(SelectedTextureArea, NodeName):

    

    #getselection
    if len(str(NodeName)) != 0:

        rt.execute ("setCommandPanelTaskMode #modify")
        
        SelectedFaces = rt.polyop.getFaceSelection(NodeName)
        
        SelectedFaceNumber = 0
        selected_faces = []
    
        for i in range(len(SelectedFaces)):
            if SelectedFaces[i] == True:
                selected_faces.append(i)
        
        #select or not
        if len(selected_faces) == 1:

            RandomPoly = False
            SelectedFaceNumber = selected_faces[0] + 1

        else: #random selector

            FacesCount = NodeName.faces.count
            
            if FacesCount == 1:
                RandInd = 1
            else:
                RandInd = str(random.randrange(1, FacesCount))                  
            
            rt.subobjectLevel = 4
            rt.execute ("$.EditablePoly.SetSelection #Face #{" + str(RandInd) + "}")
            SelectedFaceNumber = RandInd
            RandomPoly = True
        
        CurrentWorkUnits = str(rt.units.Systemtype)

        #turn on modifier
        rt.execute ("modPanel.addModToSelection (Unwrap_UVW ())")    
        rt.execute ("unwrapmod = modpanel.getcurrentobject(); unwrapmod.getarea #{" + str(SelectedFaceNumber) + "} &mX &mY &mWidth &mHeight &AreaUVW &AreaGeom")

        #to poly
        rt.execute ("macros.run \"Modifier Stack\" \"Convert_to_Poly\"")
        rt.execute ("subobjectLevel = 4")
        rt.execute ("$.EditablePoly.SetSelection #Face #{" + str(SelectedFaceNumber) + "}")

        #geometry-poly ratio
        GPRatio = math.sqrt(rt.AreaUVW/rt.AreaGeom) 

        #texel calculation
        Texel = math.ceil (GPRatio*(math.sqrt(SelectedTextureArea)))
        
        return RandomPoly, rt.AreaUVW, rt.AreaGeom, CurrentWorkUnits, GPRatio, Texel
    else:
        print ("Please select One Editable Poly object!")
        return False
    

def resolutionSelected(selected_texture_index):
    
    if selected_texture_index == 0:
        selected_texture_area = pow(64,2)
        
    if selected_texture_index == 1:
        selected_texture_area=pow(128,2)
        
    if selected_texture_index == 2:
        selected_texture_area=256*128
        
    if selected_texture_index == 3:
        selected_texture_area=pow(256,2)
        
    if selected_texture_index == 4:
        selected_texture_area=512*256
        
    if selected_texture_index == 5:
        selected_texture_area=pow(512,2)
        
    if selected_texture_index == 6:
        selected_texture_area=1024*512
        
    if selected_texture_index == 7:
        selected_texture_area=pow(1024,2)
        
    if selected_texture_index == 8:
        selected_texture_area=2048*1024
        
    if selected_texture_index == 9:
        selected_texture_area=pow(2048,2)
        
    if selected_texture_index == 10:
        selected_texture_area=4096*2048
        
    if selected_texture_index == 11:
        selected_texture_area=pow(4096,2)
        
    if selected_texture_index == 12:
        selected_texture_area=pow(8192,2)
    
    return selected_texture_area

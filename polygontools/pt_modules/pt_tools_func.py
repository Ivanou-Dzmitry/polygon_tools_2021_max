# This Python file uses the following encoding: utf-8
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

import os
import sys
import math 
from pymxs import runtime as rt
import random
import importlib

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import *

import pt_conclusion as conclusion
importlib.reload(conclusion)

import pt_conclusion as conclusion
importlib.reload(conclusion)

import pt_gen_func as gen_func
importlib.reload(gen_func)

import pt_uv_func as uvf
importlib.reload (uvf)

RootDir = ".."

if RootDir not in sys.path:
  sys.path.append( RootDir )
  
import pt_config_loader as cfgl
importlib.reload(cfgl)

#GUI    
class PT_Toools_Tab (QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        
        #set layoit
        self.tabTool_v_layout = QVBoxLayout(self)
        self.tabTool_v_layout.setAlignment(Qt.AlignTop)

        MaxWidth = 370
        
        #icons
        CurrentDir = os.path.dirname(__file__)
        IconPath = (CurrentDir + "\icons")

        try:
            iconFBXExport  = QPixmap(IconPath + "/fbxexport_icon.png")
            iconDelMat  = QPixmap(IconPath + "/delete_mat_icon.png")
            iconMateMat  = QPixmap(IconPath + "/mate_mat_icon.png")
            iconGlossMat  = QPixmap(IconPath + "/gloss_mat_icon.png")
            iconIntersect  = QPixmap(IconPath + "/intersection_icon.png")
            iconRetop  = QPixmap(IconPath + "/retop_icon.png")
            iconLod  = QPixmap(IconPath + "/lod_check_icon.png")
            iconRendPrev  = QPixmap(IconPath + "/render_prev_icon.png")
            iconNMMat  = QPixmap(IconPath + "/nm_mat_icon.png")
        except:
            cmds.warning( "PolygonTools: Can't load icons for Tools Tab! Check icon files in pt_modules/icons directory.")
        
        
        #label for info
        self.lblInfo_01 = QLabel("Select an object and click on the necessary tool.")
        self.lblInfo_01.setMargin(2)
        
        #Mat Tools Group
        self.gboxMats = QGroupBox("Materials")
        self.gboxMats.setMaximumWidth(MaxWidth)
        self.gboxMats.setMaximumHeight(100)
        self.gboxMats_h_layout = QHBoxLayout()
        
        self.btnDelMat = QPushButton("Delete")
        self.btnDelMat.setStyleSheet("color:#000000;background-color:#E1E1E1;")
        self.btnDelMat.setMinimumWidth(35)
        self.btnDelMat.setMinimumHeight(35)
        self.btnDelMat.setIcon(iconDelMat)

        self.btnGlossMat = QPushButton("Gloss")
        self.btnGlossMat.setStyleSheet("color:#000000;background-color:#E1E1E1;")
        self.btnGlossMat.setMinimumWidth(35)
        self.btnGlossMat.setMinimumHeight(35)
        self.btnGlossMat.setIcon(iconGlossMat)

        self.btnMateMat = QPushButton("Mate")
        self.btnMateMat.setStyleSheet("color:#000000;background-color:#E1E1E1;")
        self.btnMateMat.setMinimumWidth(35)
        self.btnMateMat.setMinimumHeight(35)
        self.btnMateMat.setIcon(iconMateMat)
        
        self.btnNMMat = QPushButton("NM")
        self.btnNMMat.setStyleSheet("color:#000000;background-color:#E1E1E1;")
        self.btnNMMat.setMinimumWidth(35)
        self.btnNMMat.setMinimumHeight(35)
        self.btnNMMat.setIcon(iconNMMat)


        #add elements
        self.gboxMats_h_layout.addWidget(self.btnDelMat)
        self.gboxMats_h_layout.addWidget(self.btnGlossMat)
        self.gboxMats_h_layout.addWidget(self.btnMateMat)
        self.gboxMats_h_layout.addWidget(self.btnNMMat)
        
        #st layout
        self.gboxMats.setLayout(self.gboxMats_h_layout)
        
        #Export Tools Group
        self.gboxExport = QGroupBox("Export")
        self.gboxExport.setMaximumWidth(MaxWidth)
        self.gboxExport.setMaximumHeight(100)
        self.gboxExport_h_layout = QHBoxLayout()
        self.gboxExport_h_layout.setAlignment(Qt.AlignLeft)
        
        self.btnFBXExp = QPushButton("To FBX")
        self.btnFBXExp.setStyleSheet("color:#000000;background-color:#E1E1E1;")
        self.btnFBXExp.setMinimumWidth(75)
        self.btnFBXExp.setMaximumWidth(75)
        self.btnFBXExp.setMinimumHeight(35)
        self.btnFBXExp.setIcon(iconFBXExport)
        
        self.gboxExport_h_layout.addWidget(self.btnFBXExp)
        
        self.gboxExport.setLayout(self.gboxExport_h_layout)
        
        #LOD Group
        self.gboxLOD = QGroupBox("LOD")
        self.gboxLOD.setMaximumWidth(MaxWidth)
        self.gboxLOD.setMaximumHeight(220)
        self.gboxLOD.setMinimumHeight(220)
        self.gboxLOD_h_layout = QHBoxLayout()
        self.gboxLOD_h_layout.setSizeConstraint(QLayout.SetMinimumSize)
        
        
        #left column
        self.gboxLOD_v_layout1 = QVBoxLayout()
        self.gboxLOD_v_layout1.setAlignment(Qt.AlignLeft)
        self.gboxLOD_v_layout1.setAlignment(Qt.AlignTop)

        #Rightn column
        self.gboxLOD_v_layout2 = QVBoxLayout()
        self.gboxLOD_v_layout2.setAlignment(Qt.AlignLeft)
        self.gboxLOD_v_layout2.setAlignment(Qt.AlignTop)

        #h for emulator
        self.gboxLOD_h_layout1 = QHBoxLayout()
        self.gboxLOD_h_layout1.setAlignment(Qt.AlignLeft)
        
        #h for button
        self.gboxLOD_h_layout2 = QHBoxLayout()
        self.gboxLOD_h_layout2.setAlignment(Qt.AlignRight)
        self.gboxLOD_h_layout2.setContentsMargins(0,66,0,0)
                
        self.lblDist = QLabel("Switch range")
        self.lblLOD0 = QLabel("LOD0")
        self.lblLOD4 = QLabel("LOD4")
        self.lblDistEmulation = QLabel("Virtual Distance")
        
        
        self.sldLOD = QSlider()
        self.sldLOD.setOrientation(Qt.Horizontal)
        self.sldLOD.setMinimumHeight(20)
        self.sldLOD.setMinimum(0)
        self.sldLOD.setMaximum(4)
        self.sldLOD.setTickInterval(1)
        self.sldLOD.setValue(0)
        self.sldLOD.setEnabled(False)

        self.lblLodDist = QLabel("Distance:")
        self.lblLodDist.setMinimumWidth(100)
        
        self.btnLODcheck = QToolButton()
        self.btnLODcheck.setText("LOD Check")
        self.btnLODcheck.setIcon(iconLod)
        self.btnLODcheck.setMinimumWidth(75)
        self.btnLODcheck.setCheckable(True)
                
        self.spnLOD1 = QSpinBox()
        self.spnLOD1.setFixedWidth(90)
        self.spnLOD1.setMinimum(5)
        self.spnLOD1.setMaximum(200)
        self.spnLOD1.setValue(10)
        self.spnLOD1.setSingleStep(5)
        self.spnLOD1.setPrefix("LOD1: ")
        self.spnLOD1.setSuffix("m")

        self.spnLOD2 = QSpinBox()
        self.spnLOD2.setFixedWidth(90)
        self.spnLOD2.setMinimum(10)
        self.spnLOD2.setMaximum(400)
        self.spnLOD2.setValue(20)
        self.spnLOD2.setSingleStep(10)
        self.spnLOD2.setPrefix("LOD2: ")
        self.spnLOD2.setSuffix("m")

        self.spnLOD3 = QSpinBox()
        self.spnLOD3.setFixedWidth(90)
        self.spnLOD3.setMinimum(20)
        self.spnLOD3.setMaximum(600)
        self.spnLOD3.setValue(30)
        self.spnLOD3.setSingleStep(10)
        self.spnLOD3.setPrefix("LOD3: ")
        self.spnLOD3.setSuffix("m")

        self.spnLOD4 = QSpinBox()
        self.spnLOD4.setFixedWidth(90)
        self.spnLOD4.setMinimum(30)
        self.spnLOD4.setMaximum(800)
        self.spnLOD4.setValue(40)
        self.spnLOD4.setSingleStep(10)
        self.spnLOD4.setPrefix("LOD4: ")
        self.spnLOD4.setSuffix("m")
        
        self.gboxLOD_v_layout1.addWidget(self.lblLodDist)
                
        self.gboxLOD_v_layout1.addWidget(self.lblDist)
        self.gboxLOD_v_layout1.addWidget(self.spnLOD1)
        self.gboxLOD_v_layout1.addWidget(self.spnLOD2)
        self.gboxLOD_v_layout1.addWidget(self.spnLOD3)
        self.gboxLOD_v_layout1.addWidget(self.spnLOD4)
        
        self.gboxLOD_v_layout2.addWidget(self.lblDistEmulation)
        self.gboxLOD_h_layout1.addWidget(self.lblLOD0)
        self.gboxLOD_h_layout1.addWidget(self.sldLOD)
        self.gboxLOD_h_layout1.addWidget(self.lblLOD4)
        
        self.gboxLOD_h_layout2.addWidget(self.btnLODcheck)
        
        self.gboxLOD_v_layout2.addLayout(self.gboxLOD_h_layout1)
        self.gboxLOD_v_layout2.addLayout(self.gboxLOD_h_layout2)
        
        self.gboxLOD_h_layout.addLayout(self.gboxLOD_v_layout1)
        self.gboxLOD_h_layout.addLayout(self.gboxLOD_v_layout2)
        
        self.gboxLOD.setLayout(self.gboxLOD_h_layout)
        
        #Intersect
        self.gboxIntersect = QGroupBox("Check Intersection")        
        self.gboxIntersect.setMaximumWidth(MaxWidth)
        self.gboxIntersect_h_layout = QHBoxLayout()
        self.gboxIntersect_h_layout.setAlignment(Qt.AlignLeft)
                
        #Common Tools Group
        self.gboxCommon = QGroupBox("Common")
        self.gboxCommon.setMaximumWidth(MaxWidth)
        self.gboxCommon.setMaximumHeight(100)
        self.gboxCommon_v_layout = QVBoxLayout()
        
        self.btnPrevRend = QPushButton("Render Preview")
        self.btnPrevRend.setStyleSheet("color:#000000;background-color:#E1E1E1;")
        self.btnPrevRend.setIcon(iconRendPrev)        
        self.btnPrevRend.setMinimumWidth(110)
        self.btnPrevRend.setMaximumWidth(110)
                
        #intersect gui
        self.lblFlyDist = QLabel("Depth (mm): ")
        self.lblFlyDist.setMaximumWidth(65)
        self.edtFlyDist = QLineEdit()
        self.edtFlyDist.setMaxLength(2)
        self.edtFlyDist.setMaximumWidth(40)

        self.btnCheckFly = QToolButton()
        self.btnCheckFly.setText("Check")
        self.btnCheckFly.setIcon(iconIntersect)
        self.btnCheckFly.setMaximumWidth(65)
        self.btnCheckFly.setCheckable(True)
        
        self.com_h_layout_01 = QHBoxLayout()
        self.com_h_layout_01.setAlignment(Qt.AlignLeft)
        self.com_h_layout_01.setContentsMargins(0,0,0,0)
        self.com_h_layout_01.setSpacing(10)

        self.gboxCommon_v_layout.addWidget(self.btnPrevRend)
        
        self.gboxIntersect_h_layout.addWidget(self.lblFlyDist)
        self.gboxIntersect_h_layout.addWidget(self.edtFlyDist)
        self.gboxIntersect_h_layout.addWidget(self.btnCheckFly)
        
        self.gboxCommon_v_layout.addLayout(self.com_h_layout_01)
        
        self.gboxCommon.setLayout(self.gboxCommon_v_layout)
        self.gboxIntersect.setLayout(self.gboxIntersect_h_layout)
        
        self.gboxToolConclusion = QGroupBox("Conclusion")
        self.gboxToolConclusion.setMaximumWidth(MaxWidth)
        self.gboxToolConclusion.setMinimumHeight(170)
        self.gboxToolConclusion_v_layout = QVBoxLayout()

        #conclusion text here
        self.txtbrowToolConclusion = QTextBrowser()
        self.txtbrowToolConclusion.setStyleSheet("color:#ffffff; background-color:#2b2b2b;")
        self.txtbrowToolConclusion.setHtml("")

        self.gboxToolConclusion_v_layout.addWidget(self.txtbrowToolConclusion) 
        
        #Add Base elements
        self.tabTool_v_layout.addWidget(self.lblInfo_01)        
        self.tabTool_v_layout.addWidget(self.gboxMats)
        self.tabTool_v_layout.addWidget(self.gboxExport)
        self.tabTool_v_layout.addWidget(self.gboxLOD)
        self.tabTool_v_layout.addWidget(self.gboxIntersect)
        #self.tabTool_v_layout.addWidget(self.gboxRetopo)
        self.tabTool_v_layout.addWidget(self.gboxCommon)      

        #conclusion
        self.gboxToolConclusion.setLayout(self.gboxToolConclusion_v_layout)
        
        #conclusion area
        self.tabTool_v_layout.addWidget(self.gboxToolConclusion)

        #SIGNALS
        self.btnDelMat.clicked.connect(self.btnDelMatClicked)
        self.btnGlossMat.clicked.connect(self.btnGlossMatClicked)        
        self.btnMateMat.clicked.connect(self.btnMateMatClicked)    
        self.btnNMMat.clicked.connect(self.btnNMMatClicked)    

        self.btnFBXExp.clicked.connect(self.btnFBXExpClicked)

        self.btnPrevRend.clicked.connect(self.btnPrevRendClicked)
        
        self.btnCheckFly.clicked.connect(self.btnCheckFlyClicked)
        
        self.edtFlyDist.editingFinished.connect(self.saveIntersetValue)

        #LOD
        self.spnLOD1.editingFinished.connect(self.lod1FinEdit)
        self.spnLOD2.editingFinished.connect(self.lod2FinEdit)
        self.spnLOD3.editingFinished.connect(self.lod3FinEdit)
        self.spnLOD4.editingFinished.connect(self.lod4FinEdit)

        self.btnLODcheck.clicked.connect(self.btnLODcheckClicked)  

        #Change lod Slider
        self.sldLOD.sliderReleased.connect(self.currentLOD)
        self.sldLOD.valueChanged.connect(self.lodSwitcher)
        self.sldLOD.sliderPressed.connect(self.lodsldPressed)

        #Func
        #intro text
        current_languge = cfgl.configLoader()[14]
        self.txtbrowToolConclusion.setHtml( conclusion.toolTabIntroConclusion(current_languge) )         

        self.checkToolsValues() 

        scene_data = getSceneObjects("pt_spline")        

        if scene_data[1] == True:
            self.btnCheckFly.setChecked(True)
        else:
            self.btnCheckFly.setChecked(False)

        self.LODDistance = 0
        self.sldPressed = False

        #true - struct damaged
        if checkLODLayerStructure() == True:
            self.lodDisable()
        else:
            self.checkLODValues()
            self.btnLODcheck.setChecked(True)
            self.sldLOD.setEnabled(True)


    def lodsldPressed(self):
        #set slider status
        self.sldPressed = True

    def showInfo(self, info_type, info_text):

        #trim lables
        if len(info_text) > 100:
            short_info_text = info_text[:100] + "..."
        else:
            short_info_text = info_text
        
        if info_type=="info":
            self.lblInfo_01.setText(short_info_text)
            self.lblInfo_01.setStyleSheet("background-color:#3D523D;")
            print ("PolygonTools:", info_text)
        
        if info_type=="warn":
            self.lblInfo_01.setText(short_info_text)
            self.lblInfo_01.setStyleSheet("background-color:#916666;")
            print( "PolygonTools: " + info_text )

        if info_type=="lod":
            self.lblInfo_01.setText(short_info_text)
            self.lblInfo_01.setStyleSheet("background-color:#3D523D;")
            
        if info_type=="fin":
            self.lblInfo_01.setText(short_info_text)
            self.lblInfo_01.setStyleSheet("background-color:#9E557A;")
            print ("PolygonTools:", info_text)

  #delete material    
    def btnDelMatClicked (self):
        
        current_languge = cfgl.configLoader()[14]        

        #getselection
        try:
            selection_array = gen_func.checkSelection()

            sel_objects = selection_array[0]
            sel_editable_poly_objects = selection_array[1]

        except:
            print ("Please select something. Editable Poly object for example...")


        if len(sel_editable_poly_objects) > 0:

            deleteMaterial(sel_editable_poly_objects)
                    
            self.showInfo ("info", "All materials removed from the object!")             
            self.txtbrowToolConclusion.setHtml( conclusion.toolOperationConclusion(current_languge, "DelMat") )          

        else:
            conclusion_text = conclusion.noSelection(current_languge, "del_mat")
            self.txtbrowToolConclusion.setHtml(conclusion_text) 

            self.showInfo ("warn", "Please select something for delete. Mesh object for example..")    


    #assign gloss
    def btnGlossMatClicked (self):
        
        current_languge = cfgl.configLoader()[14]        
        
        #getselection
        try:
            selection_array = gen_func.checkSelection()

            sel_objects = selection_array[0]
            sel_editable_poly_objects = selection_array[1]

        except:
            print ("Please select something. Editable Poly object for example...")


        if len(sel_editable_poly_objects) > 0:
            
            createGlossMaterial(sel_editable_poly_objects)

            self.showInfo ("info", "Gloss shader was asigned!")

            self.txtbrowToolConclusion.setHtml( conclusion.toolOperationConclusion(current_languge, "GlossMat") )          

        else:
            conclusion_text = conclusion.noSelection(current_languge, "gloss_mat")
            self.txtbrowToolConclusion.setHtml(conclusion_text) 

            self.showInfo ("warn", "Please select something for assign. Mesh object for example..")       

    #assign Mate
    def btnMateMatClicked (self):
        
        current_languge = cfgl.configLoader()[14]        
        
        #getselection
        try:
            selection_array = gen_func.checkSelection()

            sel_objects = selection_array[0]
            sel_editable_poly_objects = selection_array[1]

        except:
            print ("Please select something. Editable Poly object for example...")


        if len(sel_editable_poly_objects) > 0:
            
            createMateMaterial( sel_editable_poly_objects )

            self.showInfo ("info", "Mate shader was asigned!")           

            self.txtbrowToolConclusion.setHtml( conclusion.toolOperationConclusion(current_languge, "MateMat") )           

        else:
            conclusion_text = conclusion.noSelection(current_languge, "mate_mat")
            self.txtbrowToolConclusion.setHtml(conclusion_text) 

            self.showInfo ("warn", "Please select something for assign. Mesh object for example..")         

    def btnNMMatClicked (self):

        current_languge = cfgl.configLoader()[14] 

        #getselection
        try:
            selection_array = gen_func.checkSelection()

            sel_objects = selection_array[0]
            sel_editable_poly_objects = selection_array[1]

        except:
            print ("Please select something. Editable Poly object for example...")

        if len(sel_editable_poly_objects) > 0:            

            createNMMaterial(sel_editable_poly_objects)

            self.showInfo ("info", "NormalMap material was asigned!")           

            self.txtbrowToolConclusion.setHtml( conclusion.toolOperationConclusion(current_languge, "NMMat") )           

        else:
            conclusion_text = conclusion.noSelection(current_languge, "mate_mat")
            self.txtbrowToolConclusion.setHtml(conclusion_text) 

            self.showInfo ("warn", "Please select something for assign. Mesh object for example..")         

    #exp to fbx
    def btnFBXExpClicked (self):
        
        current_languge = cfgl.configLoader()[14]          

                   

        #getselection
        try:
            selection_array = gen_func.checkSelection()

            sel_objects = selection_array[0]
            sel_editable_poly_objects = selection_array[1]

        except:
            print ("Please select something. Editable Poly object for example...")

        FileDirectory = rt.maxFilePath
        
        CurrentSceneFileName = rt.execute ("getFilenameFile maxFileName")

        FullPathToFBXfile = FileDirectory + CurrentSceneFileName
        PathToSave = FileDirectory

        if len(sel_editable_poly_objects) > 0:
            
            if len(FullPathToFBXfile) == 0:
                self.showInfo ("warn", "Please save current scene before Export!")                        
                self.txtbrowToolConclusion.setHtml( conclusion.toolOperationConclusion(current_languge, "FBXExpProblem") )           
            else:
                if fbxExport(FullPathToFBXfile) == True:
                    self.showInfo ("info", "Export Complete! Path to FBX file: \n" + FileDirectory)
                    self.txtbrowToolConclusion.setHtml( conclusion.toolOperationConclusion(current_languge, "FBXExp") )  
                else:
                    self.showInfo ("warn", "Problems with export. Try exporting manually.")

        else:
            conclusion_text = conclusion.noSelection(current_languge, "fbx_exp")
            self.txtbrowToolConclusion.setHtml(conclusion_text) 
            
            self.showInfo ("warn", "Please select something for export. Editable Poly object for example..")    

    #render Preview    
    def btnPrevRendClicked(self):        

        current_languge = cfgl.configLoader()[14]
        
        #get dir
        FileDirectory = rt.maxFilePath

        #get scene name
        CurrentSceneFileName = rt.execute ("getFilenameFile maxFileName")

        #full path
        FullPathToJPGfile = FileDirectory + CurrentSceneFileName

        if len(FullPathToJPGfile) == 0:
            self.showInfo ("warn", "For Render Preview first of all please save scene!")                        
            self.txtbrowToolConclusion.setHtml( conclusion.toolOperationConclusion(current_languge, "RenderPreviewProblem") )           
        else:
            
            renderResult = renderPreview(FullPathToJPGfile)
            
            if renderResult == True:
                self.showInfo ("info", "Preview successfully saved to: \n" + FileDirectory)
                self.txtbrowToolConclusion.setHtml( conclusion.toolOperationConclusion(current_languge, "RenderPreview") ) 
            else:
                self.showInfo ("warn", 'Can\'t save preview!')



    def btnCheckFlyClicked (self):
                    
        current_languge = cfgl.configLoader()[14]        

        #getselection
        try:
            selection_array = gen_func.checkSelection()

            sel_objects = selection_array[0]
            sel_editable_poly_objects = selection_array[1]
            sel_editable_poly_nodes = selection_array[3]

        except:
            print ("Please select something. Editable Poly object for example...")

        PTSplineInScene = False
        scene_data = getSceneObjects("pt_spline")
        PTSplineInScene = scene_data[1]

        # button not pressed - no obj
        if (self.btnCheckFly.isChecked() == True) and (PTSplineInScene == False):

            if len(sel_editable_poly_objects) > 0:
                try:
                    #get radius and div 2
                    IntersectionRadius = ((float(self.edtFlyDist.text()))/1000)
                except:
                    self.edtFlyDist.setText("10")
                    IntersectionRadius = 0.01
                    print ("Invalid value out of range (1-99)! Value set to default - 10mm")
                    self.saveIntersetValue()            

                ExtrudeResult = openEdgesExtrude(sel_editable_poly_objects, IntersectionRadius)

                if ExtrudeResult == True:
                    self.showInfo ("info", "If you see the red lines - check the intersection between objects.") 
                    self.txtbrowToolConclusion.setHtml( conclusion.toolOperationConclusion(current_languge, "CheckIntersect") )      
                else:
                    self.showInfo ("warn", "There are NO Open Edges on the model!")
                    #conclusion
                    self.txtbrowToolConclusion.setHtml( conclusion.variousConclusion(current_languge, "OpenEdges") ) 
                    self.btnCheckFly.setChecked(False)

            else: #no selection
                conclusion_text = conclusion.noSelection(current_languge, "check_intersect")
                self.txtbrowToolConclusion.setHtml(conclusion_text) 
                
                self.showInfo ("warn", "Please select Editable Poly object(s)!")
                self.btnCheckFly.setChecked(False)

        # button pressed - obj present
        elif (self.btnCheckFly.isChecked() == False) and (PTSplineInScene == True): 

            array_to_delete = []   
            
            for i in range(len(scene_data[0])):
                if "pt_spline" in scene_data[0][i].name:
                    array_to_delete.append(scene_data[0][i])

            #select and delete
            rt.select(array_to_delete)
            rt.execute("delete $")
            
            self.showInfo ("info", "Previous intersection check was cleaned.")   
            rt.execute ("redrawViews()")
            rt.subObjectLevel = 0
            
            self.txtbrowToolConclusion.setHtml( conclusion.variousConclusion(current_languge, "IntersectClear") ) 
                    
        # button pressed - no obj (alredy deleted)
        elif (self.btnCheckFly.isChecked() == False) and (PTSplineInScene == False):                                                                
            
            self.showInfo ("info", "Previous intersection check already cleaned.")
            rt.execute ("redrawViews()")
            rt.subObjectLevel = 4
            
            self.txtbrowToolConclusion.setHtml( conclusion.variousConclusion(current_languge, "IntersectAlreadyClear") ) 


    #save value
    def saveIntersetValue(self):
        
        try:
            int(self.edtFlyDist.text())
            path_config = cfgl.configLoader()[99:101]            
            current_intersection_depth = self.edtFlyDist.text()
            cfgl.ConfigWriter('Tools', 'intersection_depth', current_intersection_depth, path_config[0], path_config[1])
        except:
            cmds.warning("intersection_depth: Invalid value or value out of range (1-99)! Value set to default - 10mm")
            path_config = cfgl.configLoader()[99:101]
            current_intersection_depth = '10'
            self.edtFlyDist.setText(current_intersection_depth)
            cfgl.ConfigWriter('Tools', 'intersection_depth', current_intersection_depth, path_config[0], path_config[1])


    def checkToolsValues(self):
            
            current_intersection_depth = self.edtFlyDist.text()
            
            #load data from config
            data_from_config = cfgl.configLoader()[12:14] 
            
            #For Intersection
            try:
                config_intersection_depth = data_from_config[0]
                int(config_intersection_depth)
                            
                #set intersect depth
                if current_intersection_depth != config_intersection_depth:
                    self.edtFlyDist.setText(config_intersection_depth)
                    
            except:
                self.saveIntersetValue()


    #run LOD check
    def btnLODcheckClicked (self):
    
        current_languge = cfgl.configLoader()[14]        

         

        rt.clearSelection()

        #check        
        if (self.btnLODcheck.isChecked() == True):
            createLODStructure()

            rt.registerRedrawViewsCallback(self.ShowDistanceToLODSInViewports)

            self.sldLOD.setEnabled(True)
            self.checkLODVis()

            self.showInfo ("info", "LOD layers created. Put LODs geometry to the appropriate Layers.")
            self.txtbrowToolConclusion.setHtml( conclusion.toolOperationConclusion(current_languge, "LOD") )

        
        if self.btnLODcheck.isChecked() == False:
            
            deleteLODStructure()

            self.showInfo ("fin", "LOD layers was deleted.")  

            rt.unregisterRedrawViewsCallback(self.ShowDistanceToLODSInViewports)

            self.lodDisable()


    def lodDisable(self):

        self.sldLOD.setValue(0)
        self.sldLOD.setEnabled(False)
        self.spnLOD1.setStyleSheet("")
        self.spnLOD2.setStyleSheet("")
        self.spnLOD3.setStyleSheet("")
        self.spnLOD4.setStyleSheet("")

        self.btnLODcheck.setChecked(False)

        self.lblLodDist.setText ("Distance: ")


    #edit lod values
    def lod1FinEdit(self):
        #write new values to config
        path_config = cfgl.configLoader()[99:101]
        currentlod1val = str(self.spnLOD1.value())
        cfgl.ConfigWriter('LOD_distance', 'lod1', currentlod1val, path_config[0], path_config[1])

        self.distChecker()
    
        
    def lod2FinEdit(self):
        #write new values to config
        path_config = cfgl.configLoader()[99:101]
        currentlod2val = str(self.spnLOD2.value())
        cfgl.ConfigWriter('LOD_distance', 'lod2', currentlod2val, path_config[0], path_config[1])

        self.distChecker()
    

    def lod3FinEdit(self):
        #write new values to config
        path_config = cfgl.configLoader()[99:101]
        currentlod3val = str(self.spnLOD3.value())
        cfgl.ConfigWriter('LOD_distance', 'lod3', currentlod3val, path_config[0], path_config[1])

        self.distChecker()
    

    def lod4FinEdit(self):
        #write new values to config
        path_config = cfgl.configLoader()[99:101]
        currentlod4val = str(self.spnLOD4.value())
        cfgl.ConfigWriter('LOD_distance', 'lod4', currentlod4val, path_config[0], path_config[1])

        self.distChecker()

    #LOD dist checker        
    def distChecker(self):
        
        #get start values
        lod1val = self.spnLOD1.value()
        lod2val = self.spnLOD2.value()
        lod3val = self.spnLOD3.value()
        lod4val = self.spnLOD4.value() 
        
        path_config = cfgl.configLoader()[99:101]
        
        #compare values and Write to File if they different
        if lod1val >= lod2val:
             self.spnLOD2.setValue(lod1val + 10) #next lod cant less then previous
             currentlod2val = str(self.spnLOD2.value())
             cfgl.ConfigWriter('LOD_distance', 'lod2', currentlod2val, path_config[0], path_config[1])
             
        lod2val = self.spnLOD2.value()    
                    
        if lod2val >= lod3val:
             self.spnLOD3.setValue(lod2val + 10)
             currentlod3val = str(self.spnLOD3.value())
             cfgl.ConfigWriter('LOD_distance', 'lod3', currentlod3val, path_config[0], path_config[1])
        
        lod3val = self.spnLOD3.value()

        if lod3val >= lod4val:
             self.spnLOD4.setValue(lod3val + 10)
             currentlod4val = str(self.spnLOD4.value())
             cfgl.ConfigWriter('LOD_distance', 'lod4', currentlod4val, path_config[0], path_config[1])


    def LODSwitcherONOFF (self, LODOn, LODa, LODb, LODc, LODd):
        
        
        
        if checkLODLayerStructure() == False:
            try:
                rt.LayerManager.getLayerFromName(LODOn).on = True
                rt.LayerManager.getLayerFromName(LODa).on = False
                rt.LayerManager.getLayerFromName(LODb).on = False
                rt.LayerManager.getLayerFromName(LODc).on = False
                rt.LayerManager.getLayerFromName(LODd).on = False
                rt.redrawViews()
            except:            
                self.lodDisable()
                print ("ERROR! The structure for checking lods is Damaged! Check function will be Disabled.")
                rt.unregisterRedrawViewsCallback(self.ShowDistanceToLODSInViewports)
        else:
            rt.unregisterRedrawViewsCallback(self.ShowDistanceToLODSInViewports)
            print ("ERROR! The structure for checking lods is Dаmaged! Check function will be Disabled.")
            self.lodDisable()


    def ShowDistanceToLODSInViewports(self):

        

        #get start values
        LOD1Val = int(self.spnLOD1.value())
        LOD2Val = int(self.spnLOD2.value())
        LOD3Val = int(self.spnLOD3.value())
        LOD4Val = int(self.spnLOD4.value())
                
        rt.execute ("DistMatrix = getViewTM()")
        rt.execute("DistToLOD = DistMatrix.row4.z")
        rt.execute("gw.updateScreen()")
        rt.execute ("WinWidth = (gw.getWinSizeX() / 2)")
        rt.execute(" gw.wText [WinWidth, 40, 0] (\"Distance: \" + (abs(DistToLOD)) as String) color: white")

        self.LODDistance = int(rt.DistToLOD)*-1
        if self.LODDistance  < 0:
            self.LODDistance = 0
        
        if checkLODLayerStructure() == False:
            if self.LODDistance < LOD1Val and (self.sldPressed == False):
                self.LODSwitcherONOFF("lod0", "lod1", "lod2", "lod3", "lod4")

            if self.LODDistance > LOD1Val and (self.sldPressed == False):
                self.LODSwitcherONOFF("lod1", "lod0", "lod2", "lod3", "lod4")

            if self.LODDistance > LOD2Val and (self.sldPressed == False):
                self.LODSwitcherONOFF("lod2", "lod1", "lod0", "lod3", "lod4")

            if self.LODDistance > LOD3Val and (self.sldPressed == False):
                self.LODSwitcherONOFF("lod3", "lod1", "lod2", "lod0", "lod4")

            if self.LODDistance > LOD4Val and (self.sldPressed == False):
                self.LODSwitcherONOFF("lod4", "lod1", "lod2", "lod3", "lod0")

            self.lblLodDist.setText ("Distance: " + str(self.LODDistance ))

            self.checkLODVis()
        else:
            rt.unregisterRedrawViewsCallback(self.ShowDistanceToLODSInViewports)
            print ("ERROR! The structure for checking lods is damaged! Check function will be disabled.")
            self.lodDisable()
    
        return self.LODDistance


    #check lod vis
    def checkLODVis(self):

        

        try:        
            #get lod visibility
            if checkLODLayerStructure() == False:
                try:
                    lod0vis = rt.LayerManager.getLayerFromName("lod0").on
                    lod1vis = rt.LayerManager.getLayerFromName("lod1").on
                    lod2vis = rt.LayerManager.getLayerFromName("lod2").on
                    lod3vis = rt.LayerManager.getLayerFromName("lod3").on
                    lod4vis = rt.LayerManager.getLayerFromName("lod4").on
                except:
                    pass
            else:
                pass
                    
            self.lblLodDist.setText("Distance: " + str(self.LODDistance))
            
            #change color and slider position
            if lod0vis == True:
                self.spnLOD1.setStyleSheet("")
                self.spnLOD2.setStyleSheet("")
                self.spnLOD3.setStyleSheet("")
                self.spnLOD4.setStyleSheet("")
                self.sldLOD.setValue(0)
                self.showInfo ("lod", "LOD 0 is displayed.")
        
            if lod1vis == True:
                self.spnLOD1.setStyleSheet("background-color:#005826;")
                self.spnLOD2.setStyleSheet("")
                self.spnLOD3.setStyleSheet("")
                self.spnLOD4.setStyleSheet("")
                self.sldLOD.setValue(1)
                self.showInfo ("lod", "LOD 1 is displayed.")

            if lod2vis == True:
                self.spnLOD1.setStyleSheet("")
                self.spnLOD2.setStyleSheet("background-color:#005826;")
                self.spnLOD3.setStyleSheet("")
                self.spnLOD4.setStyleSheet("")
                self.sldLOD.setValue(2)
                self.showInfo ("lod", "LOD 2 is displayed.")

            if lod3vis == True:
                self.spnLOD1.setStyleSheet("")
                self.spnLOD2.setStyleSheet("")
                self.spnLOD3.setStyleSheet("background-color:#005826;")
                self.spnLOD4.setStyleSheet("")
                self.sldLOD.setValue(3)
                self.showInfo ("lod", "LOD 3 is displayed.")
        
            if lod4vis == True:
                self.spnLOD1.setStyleSheet("")
                self.spnLOD2.setStyleSheet("")
                self.spnLOD3.setStyleSheet("")
                self.spnLOD4.setStyleSheet("background-color:#005826;")
                self.sldLOD.setValue(4)
                self.showInfo ("lod", "LOD 4 is displayed.")
        except:
            pass


    #current lod is        
    def currentLOD (self):

        
        
        self.sldPressed = False

        if checkLODLayerStructure() == False:            
            #set normal LOD values and reset styles
            try:
                rt.LayerManager.getLayerFromName("lod0").on = True
                rt.LayerManager.getLayerFromName("lod1").on = True
                self.spnLOD1.setStyleSheet("")
                rt.LayerManager.getLayerFromName("lod2").on = True
                self.spnLOD2.setStyleSheet("")
                rt.LayerManager.getLayerFromName("lod3").on = True
                self.spnLOD3.setStyleSheet("")
                rt.LayerManager.getLayerFromName("lod4").on = True
                self.spnLOD4.setStyleSheet("")
                
                self.checkLODVis()
            except:
                pass
        else:
            print ("ERROR! The structure for checking lods is Damaged! Check function will be Disabled.1")


    def lodSwitcher(self):

        
                
        LOD = self.sldLOD.value()
        
        #change visibility LODs only if Slider pressed
        if (LOD == 0) and (self.sldPressed  == True):
            try:
                rt.LayerManager.getLayerFromName("lod0").on = True
                rt.LayerManager.getLayerFromName("lod1").on = False
                rt.redrawViews()
            except:
                pass
        
        if (LOD == 1) and (self.sldPressed == True):
            try:
                rt.LayerManager.getLayerFromName("lod0").on = False
                rt.LayerManager.getLayerFromName("lod1").on = True
                rt.LayerManager.getLayerFromName("lod2").on = False
                rt.redrawViews()
            except:
                pass
            
        if (LOD == 2) and (self.sldPressed == True):
            try:
                rt.LayerManager.getLayerFromName("lod1").on = False
                rt.LayerManager.getLayerFromName("lod2").on = True
                rt.LayerManager.getLayerFromName("lod3").on = False
                rt.redrawViews()
            except:
                pass

        if (LOD == 3) and (self.sldPressed == True):
            try:
                rt.LayerManager.getLayerFromName("lod2").on = False
                rt.LayerManager.getLayerFromName("lod3").on = True
                rt.LayerManager.getLayerFromName("lod4").on = False
                rt.redrawViews()
            except:
                pass

        if (LOD == 4) and (self.sldPressed == True):
            try:
                rt.LayerManager.getLayerFromName("lod3").on = False
                rt.LayerManager.getLayerFromName("lod4").on = True
                rt.redrawViews()
            except:
                pass

    #lod val from file            
    def checkLODValues (self):

        

        #get start values
        currentlod1val = self.spnLOD1.value()
        currentlod2val = self.spnLOD2.value()
        currentlod3val = self.spnLOD3.value()
        currentlod4val = self.spnLOD4.value()
        
        data_from_config = cfgl.configLoader()[5:9]
        
        #get config values
        configlod1val = data_from_config[0]
        configlod2val = data_from_config[1]
        configlod3val = data_from_config[2]
        configlod4val = data_from_config[3]
        
        
        #set config values
        if currentlod1val != configlod1val:
            self.spnLOD1.setValue(int(configlod1val))
             
        if currentlod2val != configlod2val:
            self.spnLOD2.setValue(int(configlod2val))

        if currentlod3val != configlod3val:
            self.spnLOD3.setValue(int(configlod3val))

        if currentlod4val != configlod4val:
            self.spnLOD4.setValue(int(configlod4val))

        if checkLODLayerStructure() == False:
            rt.registerRedrawViewsCallback(self.ShowDistanceToLODSInViewports)
            self.checkLODVis()


def deleteMaterial (sel_editable_poly_objects):

    

    for i in range(len(sel_editable_poly_objects)):
        rt.execute ("$" + sel_editable_poly_objects[i] + ".material = undefined")
        rt.execute ("$" + sel_editable_poly_objects[i] + ".wirecolor = color (random 1 255)  (random 1 255)  (random 1 255)")
    
    rt.execute ("actionMan.executeAction -844228238 \"13\"")
    rt.execute ("redrawViews()")


def createMateMaterial(sel_editable_poly_objects):

    
    material_data = uvf.checkShaderIntegrity()

    #print (material_data[10])
    
    if material_data[10] == False:
        #mat for checker
        rt.execute ("PT_Matte_Material = Standard()")    
        rt.PT_Matte_Material.name = "PT_Matte_Material"
        rt.PT_Matte_Material.glossiness = 0

        #find free slot
        Slot = 0
        for i in range(0, 24):
            SlotName = str(rt.meditMaterials[i])
            if "- Default:" in SlotName:
                Slot = i
                break
            else:
                Slot = 0

        rt.meditmaterials[Slot] = rt.PT_Matte_Material
        print ("PolygonTools. Mate shader was created.")
    
    for i in range(len(sel_editable_poly_objects)):
        try:
            rt.execute ("$" + sel_editable_poly_objects[i] + ".material = meditmaterials[\"PT_Matte_Material\"]")
        except:
            pass
        try:
            rt.execute ("$" + sel_editable_poly_objects[i] + ".material = scenematerials[\"PT_Matte_Material\"]")
        except:
            pass
    
    rt.execute ("actionMan.executeAction -844228238 \"13\"")
    rt.execute ("redrawViews()")


def createGlossMaterial(sel_editable_poly_objects): 

    
    material_data = uvf.checkShaderIntegrity()

    #print material_data[11]
    
    if material_data[11] == False:

        #mat for checker
        rt.execute ("PT_Gloss_Material = Standard()")    
        rt.PT_Gloss_Material.name = "PT_Gloss_Material"
        rt.PT_Gloss_Material.glossiness = 50
        rt.PT_Gloss_Material.specularLevel = 100

        #find free slot
        Slot = 0
        for i in range(0, 24):
            SlotName = str(rt.meditMaterials[i])
            if "- Default:" in SlotName:
                Slot = i
                break
            else:
                Slot = 0

        rt.meditmaterials[Slot] = rt.PT_Gloss_Material
        print ("PolygonTools. Gloss shader was created.")

    for i in range(len(sel_editable_poly_objects)):
        try:
            rt.execute ("$" + sel_editable_poly_objects[i] + ".material = meditmaterials[\"PT_Gloss_Material\"]")
        except:
            pass
        try:
            rt.execute ("$" + sel_editable_poly_objects[i] + ".material = scenematerials[\"PT_Gloss_Material\"]")
        except:
            pass

    rt.execute ("actionMan.executeAction -844228238 \"13\"")
    rt.execute ("redrawViews()")
    

def createNMMaterial(sel_editable_poly_objects): 

    

    #get data
    material_data = uvf.checkShaderIntegrity()
    
    #if not created
    if material_data[12] == False:

        #mat for checker
        rt.execute ("PT_NM_Material = Standard()")    
        rt.PT_NM_Material.name = "PT_NM_Material"
        rt.PT_NM_Material.glossiness = 50
        rt.PT_NM_Material.specularLevel = 100
        rt.PT_NM_Material.bumpMapEnable = True
        rt.execute ("PT_NM_Material.bumpMap = Normal_Bump ()")
        rt.PT_NM_Material.bumpMapAmount = 100
        rt.PT_NM_Material.bumpMap.flipgreen = True
        rt.PT_NM_Material.bumpMap.method = 0

        #get root script dir
        rt.execute ("UserScriptsDir = getDir #userScripts")
        TempGetDirPath = rt.UserScriptsDir

        #change symbols
        GetDirPath = TempGetDirPath.replace ("\\", "/") + "/polygontools/pt_modules/"

        #create full name
        PathToNormalMapFile = GetDirPath + "pt_dummy_normal_map.png"
        
        try:
            rt.execute ("PT_NM_Material.bumpMap.normal_map = Bitmaptexture fileName:\"" + PathToNormalMapFile + "\"")
        except:
            print ("PolygonTools. Normal Map texture pt_dummy_normal_map.png not exist. Check files or try to re-install PolygonTools.")
            print ("Full Path to texture must be:", PathToNormalMapFile            )

        #find free slot if possible
        Slot = 0
        for i in range(0, 24):
            SlotName = str(rt.meditMaterials[i])
            if "- Default:" in SlotName:
                Slot = i
                break
            else:
                Slot = 0

        rt.meditmaterials[Slot] = rt.PT_NM_Material
        print ("PolygonTools. NM shader was created.")

    rt.execute ("actionMan.executeAction -844228238 \"12\"")
    rt.execute ("actionMan.executeAction -844228238 \"0\"")
    rt.execute ("actionMan.executeAction -844228238 \"5\"")

    #assign material
    for i in range(len(sel_editable_poly_objects)):
        try:
            rt.execute ("$" + sel_editable_poly_objects[i] + ".material = meditmaterials[\"PT_NM_Material\"]")
        except:
            pass
        try:
            rt.execute ("$" + sel_editable_poly_objects[i] + ".material = scenematerials[\"PT_NM_Material\"]")
        except:
            pass

    rt.execute ("redrawViews()")
    rt.execute ("actionMan.executeAction 0 \"63547\"")

    
def fbxExport(PathToFBXfile):

    

    FullPathToFBXfile = PathToFBXfile.replace ("\\", "/")

    PathWithoutExtension = FullPathToFBXfile.replace (".max", "")

    #print PathWithoutExtension

    #--Geometry------------------------------------------------------------------------
    rt.execute ("FBXExporterSetParam \"SmoothingGroups\" true")
    rt.execute ("FBXExporterSetParam \"NormalsPerPoly\" false")
    rt.execute ("FBXExporterSetParam \"TangentSpaceExport\" true")
    rt.execute ("FBXExporterSetParam \"SmoothMeshExport\" false")
    rt.execute ("FBXExporterSetParam \"Preserveinstances\" false")
    rt.execute ("FBXExporterSetParam \"SelectionSetExport\" false")
    rt.execute ("FBXExporterSetParam \"GeomAsBone\" false")
    rt.execute ("FBXExporterSetParam \"ColladaTriangulate\" true")
    rt.execute ("FBXExporterSetParam \"PreserveEdgeOrientation\" true")
    #--Animation------------------------------------------------------------------------
    rt.execute ("FBXExporterSetParam \"Animation\" false")
    #--Cameras------------------------------------------------------------------------
    rt.execute ("FBXExporterSetParam \"Cameras\" false")
    #--Lights------------------------------------------------------------------------
    rt.execute ("FBXExporterSetParam \"Lights\" false")
    #--Embed Media--------------------------------------------------------------------
    rt.execute ("FBXExporterSetParam \"EmbedTextures\" false")
    #--Units----------------------------------------------------------------------------
    #--Axis Conversion-----------------------------------------------------------------
    rt.execute ("FBXExporterSetParam \"AxisConversionMethod\" \"Fbx_Root\"")
    rt.execute ("FBXExporterSetParam \"UpAxis\" \"Y\" ")
    #--UI----------------------------------------------------------------
    rt.execute ("FBXExporterSetParam \"ShowWarnings\" true")
    rt.execute ("FBXExporterSetParam \"GenerateLog\" false")
    #--FBX File Format----------------------------------------------------------------
    rt.execute ("FBXExporterSetParam \"ASCII\" true")
    rt.execute ("FBXExporterSetParam \"FileVersion\" \"FBX201800\"")

    try:
        rt.execute ("exportFile \"" + PathWithoutExtension + "\" #noPrompt selectedOnly:true using:FBXEXP")
        rt.execute ("messagebox \"Export to FBX successfully complete!\" title:\"Polygon Tools 2\" ")
        return True
    except:
        return False

def openEdgesExtrude(sel_editable_poly_objects, IntersectionRadius):

    
    rt.execute ("max modify mode")
    
    #get selection
    SelectedNodes = rt.selection

    ObjWithoutOpenEdges = False

    for i in range(len(sel_editable_poly_objects)):
        
        rt.execute ("select $" + sel_editable_poly_objects[i])
        rt.execute ("subobjectLevel = 3")
        rt.execute ("actionMan.executeAction 0 \"40021\"")			
        rt.execute ("SelectedEdgesCount = $" + sel_editable_poly_objects[i] + ".EditablePoly.GetSelection #Edge; SelectedEdgesCount = SelectedEdgesCount as Array")   

        if len(rt.SelectedEdgesCount) > 0:

            SplineName = sel_editable_poly_objects[i] + "_pt_spline"

            rt.execute ("select $" + sel_editable_poly_objects[i])
            rt.execute ("$.EditablePoly.createShape \"" + SplineName + "\" off $")

            rt.execute ("select $" + SplineName)
            rt.execute ("$" + SplineName + ".render_displayRenderMesh = true")
            rt.execute ("$" + SplineName + ".render_thickness = " + str(IntersectionRadius) )
            rt.execute ("$" + SplineName + ".render_sides = 4")
            rt.execute ("$" + SplineName + ".wirecolor = color 255 0 0")
            
            rt.execute ("$" + SplineName + ".material = Standard ()")
            rt.execute ("$" + SplineName + ".material.name = \"PT_Spline\"")
            rt.execute ("$" + SplineName + ".material.selfIllumAmount = 100")
            
            
            rt.execute ("$" + SplineName + ".showVertexColors = on")
            rt.execute ("$" + SplineName + ".vertexColorsShaded = on")
            rt.execute ("convertto $" + SplineName + " editable_poly")
            rt.execute ("subobjectLevel = 4")			
            rt.execute ("actionMan.executeAction 0 \"40021\"")
            rt.execute ("$" + SplineName + ".SetFaceColor (color 255 0 0) #VertexColor")
            rt.execute ("subobjectLevel = 0")
            
            rt.execute ("actionMan.executeAction 0 \"550\"")

        else:
            print (sel_editable_poly_objects[i], "There are no open edges on the model.")
            ObjWithoutOpenEdges = True

    #return selection
    rt.select(SelectedNodes)

    if (len(sel_editable_poly_objects) == 1) and (ObjWithoutOpenEdges == True):
        return False
    else:
        return True

#get all scene objects
def getSceneObjects (Name):
    
    #get all scene ojects Before Rename
    SceneObjects = rt.objects
    
    #renamer
    for i in range(len(SceneObjects)):
        try:
            ObjectClass = str(SceneObjects[i].name)
        except:            
            SceneObjects[i].name = "pt_renamed_object_" + str(i)
            print ('\t', "Name Errors Detected! Auto-renamed object:", SceneObjects[i].name)

    #get all scene ojects After Rename
    SceneObjects = rt.objects

    NameInScenePresence = False

    #finde specify name
    for i in range(len(SceneObjects)):
        if Name in SceneObjects[i].name:
            NameInScenePresence = True

    return SceneObjects, NameInScenePresence

#LOD layers creatoe
def createLODStructure():

    for i in range(0, 5):
        LayerName = "lod" + str(i)
        LayerObjectName = "LOD" + str(i)
        
        if rt.LayerManager.getLayerFromName(LayerName) == None:
            LayerObjectName = rt.LayerManager.newLayer()
            LayerObjectName.setname(LayerName)
        else:
            print (LayerName, "layer already created!")

    print ("\nPolygonTools. LOD layers structure was sucessfyly created on scene.\n")

#delete LOD layetr structure
def deleteLODStructure():

    

    try:
        for i in range(0, 5):
            LayerName = "lod" + str(i)
            rt.LayerManager.deleteLayerHierarchy(LayerName, forceDelete = True)
    except:
        print ('\n', "PolygonTools. The structure for checking LOD's is damaged. Please delete layers manually!")


def checkLODLayerStructure():

    

    LayerError = False

    try:
        for i in range(0, 5):
            LayerName = "lod" + str(i)
            rt.LayerManager.getLayerFromName(LayerName).on
    except:
        LayerError = True
    
    return LayerError


def  renderPreview(Path):

    

    try:
        FullPath = Path.replace ("\\", "/")
        PathWithoutExtension = FullPath.replace (".max", "")

        rt.execute ("actionMan.executeAction 0 \"550\"")
        rt.execute ("max zoomext sel all")
        rt.execute ("viewport.setType #view_persp_user")
        rt.execute ("img = gw.getViewportDib()")
        rt.execute ("img.filename = \"" + PathWithoutExtension + "_preview.jpg\"; save img")
        rt.execute ("messagebox \"Render preview complete.\" title:\"Polygon Tools 2\"")

        return True
    except:
        return False
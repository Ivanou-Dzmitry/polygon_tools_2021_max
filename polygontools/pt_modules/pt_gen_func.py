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
import threading
import random
import sys
from pymxs import runtime as rt

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import *

import importlib

import pt_conclusion as conclusion
importlib.reload(conclusion)

RootDir = ".."

if RootDir not in sys.path:
  sys.path.append( RootDir )

import pt_config_loader as cfgl
importlib.reload(cfgl)

#General Tab
class PT_Gen_Tab (QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)

        self.tabGen_v_layout = QVBoxLayout(self)
        self.tabGen_v_layout.setAlignment(Qt.AlignTop)

        MaxWidth = 370

        #Top Labels
        self.lbInfo01 = QLabel()        
        self.lbInfo01.setMaximumWidth(MaxWidth)
        self.lbInfo01.setText('Welcome to Polygon Tools!')
        self.lbInfo01.setMargin(2)
        
        self.lbInfo02 = QLabel()
        self.lbInfo02.setMaximumWidth(MaxWidth)
        self.lbInfo02.setMargin(2)

        #Progress Bar
        self.pbChekProgress = QProgressBar()
        self.pbChekProgress.setMaximumWidth(MaxWidth)
        self.pbChekProgress.setRange(0, 100)
        
        #Elements
        
        #icons
        CurrentDir = os.path.dirname(__file__)
        IconPath = (CurrentDir + "\icons")

        try:
            iconMesh = QPixmap(IconPath +"/mesh_icon.png")
            iconScene = QPixmap(IconPath +"/scene_icon.png")
            iconViewport = QPixmap(IconPath +"/viewport_icon.png")
            iconStat = QPixmap(IconPath +"/stat_icon.png")
            self.iconDim = QPixmap(IconPath +"/dim_icon.png")
            self.iconDimXForm = QPixmap(IconPath +"/dim_transform_icon.png")
            iconZeroA = QPixmap(IconPath +"/zero_area_icon.png")
            iconNoSG = QPixmap(IconPath +"/nosg_icon.png")
            iconMrgdSG = QPixmap(IconPath +"/mergedsg_icon.png")
        except:
            print ("PolygonTools: Can't load icons for General Tab! Check icon files in pt_modules/icons directory.")
                
        #groupbox Prepare
        self.gboxPrepare = QGroupBox("Prepare for Feedback")
        self.gboxPrepare.setMaximumWidth(MaxWidth)
        self.gboxPrepare_v_layout = QVBoxLayout()     
                
        #Prepare buttons        
        self.btnPrepScene = QPushButton("Scene")
        self.btnPrepScene.setStyleSheet("color:#000000;background-color:#E1E1E1;")
        self.btnPrepScene.setMaximumWidth(85)
        self.btnPrepScene.setMinimumWidth(85)
        self.btnPrepScene.setMinimumHeight(35)
        self.btnPrepScene.setIcon(iconScene)
        
        self.btnPrepView = QPushButton("Viewports")
        self.btnPrepView.setStyleSheet("color:#000000;background-color:#E1E1E1;")
        self.btnPrepView.setMaximumWidth(85)
        self.btnPrepView.setMinimumWidth(85)
        self.btnPrepView.setMinimumHeight(35)
        self.btnPrepView.setIcon(iconViewport)
                
        self.btnPrepMesh = QPushButton("Mesh")
        self.btnPrepMesh.setStyleSheet("color:#000000;background-color:#E1E1E1;")
        self.btnPrepMesh.setMaximumWidth(85)
        self.btnPrepMesh.setMinimumWidth(85)
        self.btnPrepMesh.setMinimumHeight(35)
        self.btnPrepMesh.setIcon(iconMesh)

        #groupbox Statistics
        self.gboxStatistics = QGroupBox("Statistics")
        self.gboxStatistics.setMaximumWidth(MaxWidth)
        self.gboxStatistics_v_layout = QVBoxLayout()     
        
        #Statistics labels      
        self.lblShapes = QLabel("Editable Poly Objects: ")
        self.lblpolycount = QLabel("Polygons: ")
        self.lbltriscount = QLabel("Triangles: ")
        self.lblvertcount = QLabel("Vertices: ")
        self.lblJointsCount = QLabel("Bones: ")
        self.lblUVVert = QLabel("UV-vertices: ")
        self.lblMatIDQ = QLabel("Materials: ")
        self.lblUVUt = QLabel("Total UV-Utilization: ")
        self.lblUVUtAvg = QLabel("Average UV-Utilization: ")
        self.lblUVO = QLabel("Overlaps: ")
        self.lblUVarea = QLabel("UV in [0,1]: ")
        self.lblMapChanQ = QLabel("Map Channels: ")
        self.lblSmoothGroupCount = QLabel("Smoothing groups: ")
        self.lblIDCount = QLabel("Material ID's: ")
        
        #forUVutil
        self.lblUVUtilPic = QLabel()
        self.lblUVUtilPic.setFixedSize(120, 100)
        
        self.pixmap = QPixmap(QSize(100,100))
        self.colorBlack = QColor()

        self.colorBlack.setRgb(0,0,0,255)
        self.pixmap.fill(self.colorBlack)
        
        self.lblUVUtilPic.setPixmap(self.pixmap)
        
        self.gboxGenConclusion = QGroupBox("Conclusion")
        self.gboxGenConclusion.setMaximumWidth(MaxWidth)
        self.gboxGenConclusion.setStyleSheet("color:#ffffff; background-color:#2b2b2b;")
        self.gboxGenConclusion.setMinimumHeight(170)
        self.gboxGenConclusion_v_layout = QVBoxLayout()
        
        #conclusion text here
        self.txtbrowGenConclusion = QTextBrowser()
        self.txtbrowGenConclusion.setHtml("")
            
        self.gboxGenConclusion_v_layout.addWidget(self.txtbrowGenConclusion) 

        self.btnZeroPolySelector = QPushButton()
        self.btnZeroPolySelector.setMinimumWidth(18)
        self.btnZeroPolySelector.setMaximumWidth(22)
        self.btnZeroPolySelector.setToolTip("Select Zero-Faces")
        self.btnZeroPolySelector.setDisabled(True)
        self.btnZeroPolySelector.setIcon(iconZeroA)

        #layout for zero poly
        self.poly_h_layout = QHBoxLayout()
        self.poly_h_layout.addWidget(self.lblpolycount)
        self.poly_h_layout.addWidget(self.btnZeroPolySelector)

        self.btnZeroSGSelector = QPushButton()
        self.btnZeroSGSelector.setMinimumWidth(18)
        self.btnZeroSGSelector.setMaximumWidth(22)
        self.btnZeroSGSelector.setToolTip("Select Polygons Without SG")
        self.btnZeroSGSelector.setIcon(iconNoSG)

        self.btnMergeSGSelector = QPushButton()
        self.btnMergeSGSelector.setMinimumWidth(18)
        self.btnMergeSGSelector.setMaximumWidth(22)
        self.btnMergeSGSelector.setToolTip("Select Polygons With Merged SG")
        self.btnMergeSGSelector.setIcon(iconMrgdSG)

        #layout for sg
        self.sg_h_layout = QHBoxLayout()

        self.sg_h_layout.addWidget(self.lblSmoothGroupCount)
        self.sg_h_layout.addWidget(self.btnZeroSGSelector)
        self.sg_h_layout.addWidget(self.btnMergeSGSelector)
        
        #Add labels to groupbox
        self.gboxStatistics_v_layout.addWidget(self.lblShapes)
        self.gboxStatistics_v_layout.addLayout(self.poly_h_layout) #for poly
        self.gboxStatistics_v_layout.addWidget(self.lbltriscount)
        self.gboxStatistics_v_layout.addWidget(self.lblvertcount)
        self.gboxStatistics_v_layout.addWidget(self.lblJointsCount)
        self.gboxStatistics_v_layout.addWidget(self.lblUVVert)
        self.gboxStatistics_v_layout.addWidget(self.lblMatIDQ)
        self.gboxStatistics_v_layout.addWidget(self.lblUVO)
        self.gboxStatistics_v_layout.addWidget(self.lblUVarea)
        self.gboxStatistics_v_layout.addWidget(self.lblMapChanQ)
        self.gboxStatistics_v_layout.addLayout(self.sg_h_layout) #for sg
        self.gboxStatistics_v_layout.addWidget(self.lblIDCount)
        self.gboxStatistics_v_layout.addWidget(self.lblUVUt)
        self.gboxStatistics_v_layout.addWidget(self.lblUVUtAvg)
        self.gboxStatistics_v_layout.addWidget(self.lblUVUtilPic)
        
        # Horizontal layout 2 for buttons
        self.tabGen_h_layout_02 = QHBoxLayout()
        self.tabGen_h_layout_02.setAlignment(Qt.AlignLeft)
        
        self.gboxStatistics_v_layout.addLayout(self.tabGen_h_layout_02)
        
        self.btnGetStat = QPushButton("Get Statistics")
        self.btnGetStat.setStyleSheet("color:#000000;background-color:#E1E1E1;")
        self.btnGetStat.setToolTip("Statistics")
        self.btnGetStat.setMinimumWidth(110)
        self.btnGetStat.setIcon(iconStat)
        
        self.btnGetDim = QToolButton()
        self.btnGetDim.setText("Show Dimension")
        self.btnGetDim.setToolTip("Show Dimension")
        self.btnGetDim.setIcon(self.iconDim) 
        self.btnGetDim.setCheckable(True)

        self.btnMergeSGSelector.setEnabled(False)
        self.btnZeroSGSelector.setEnabled(False)

        #2 buttons
        self.tabGen_h_layout_02.addWidget(self.btnGetStat)
        self.tabGen_h_layout_02.addWidget(self.btnGetDim)
        self.tabGen_h_layout_02.addWidget(self.btnZeroPolySelector)
        self.tabGen_h_layout_02.addWidget(self.btnZeroSGSelector)
        self.tabGen_h_layout_02.addWidget(self.btnMergeSGSelector)

        #add gbox stat to layout
        self.gboxStatistics.setLayout(self.gboxStatistics_v_layout)
        
        #conclusion
        self.gboxGenConclusion.setLayout(self.gboxGenConclusion_v_layout)
        
        #Add to Layout
        
        #labels
        self.tabGen_v_layout.addWidget(self.lbInfo01)
        self.tabGen_v_layout.addWidget(self.lbInfo02)
        
        #set progress bar to layout
        self.tabGen_v_layout.addWidget(self.pbChekProgress)
        self.pbChekProgress.setValue(0)
        
        self.prep_h_layout_01 = QHBoxLayout()
        self.prep_h_layout_01.setAlignment(Qt.AlignLeft)
        
        #Add horizontal elements - buttons prepare    
        self.prep_h_layout_01.addWidget(self.btnPrepMesh)
        self.prep_h_layout_01.addWidget(self.btnPrepScene)
        self.prep_h_layout_01.addWidget(self.btnPrepView)
        
        self.gboxPrepare_v_layout.addLayout(self.prep_h_layout_01)
        
        self.gboxPrepare.setLayout(self.gboxPrepare_v_layout)
        
        #add Group Box
        self.tabGen_v_layout.addWidget(self.gboxPrepare)
    
        #Statistics area
        self.tabGen_v_layout.addWidget(self.gboxStatistics)
        
        #conclusion area
        self.tabGen_v_layout.addWidget(self.gboxGenConclusion)

        #-------SIGNALS-----------
        
        #Mesh Prepare
        self.btnPrepMesh.clicked.connect(self.btnPrepMeshClicked)

        #Scene Prepare
        self.btnPrepScene.clicked.connect(self.btnPrepSceneClicked)

        #Viewport Prepare
        self.btnPrepView.clicked.connect(self.btnPrepViewClicked)

        #Get Statistics
        self.btnGetStat.clicked.connect(self.getStatistics)

        #select zero faces
        self.btnZeroPolySelector.clicked.connect(self.selectZeroFaces)

        #select zero SG
        self.btnZeroSGSelector.clicked.connect(self.selectPolyNoSG)

        #select MergedSG
        self.btnMergeSGSelector.clicked.connect(self.selectMergedSG)

        #GetDimension
        self.btnGetDim.pressed.connect(self.btnGetDimPressed)        

        #-----------------------------

        #lang selector
        cfgl.configLoader()

        current_languge = cfgl.configLoader()[14]
        self.txtbrowGenConclusion.setHtml( conclusion.genTabIntroConclusion(current_languge) )

        self.ObjectWithZeroFaces = []
        self.merged_sg = []
        self.no_sg = []

    #clean values
    def valueCleaner(self, what_clear):
    
        #1 clear stat
        if what_clear == '1':
            self.SimpleActionResponce('123', '', '', '')
            self.pbChekProgress.setValue(0)
            self.lblShapes.setText('Editable Poly Objects: ')
            self.lblpolycount.setText('Polygons: ')
            self.lbltriscount.setText('Triangles: ')
            self.lblvertcount.setText('Vertices: ')
            self.lblJointsCount.setText('Bones: ')
            self.lblUVVert.setText('UV-vertices: ')
            self.lblMatIDQ.setText("Materials: ")
            self.lblUVO.setText("Overlaps: ")
            self.lblMapChanQ.setText("Map Channels: ")
            self.lblUVUt.setText ("Total UV-Utilization: ")
            self.lblUVUtAvg.setText ("Average UV-Utilization: ")
            self.lblUVarea.setText ("UV in [0,1]: ")
            self.lblSmoothGroupCount.setText ("Smoothing groups: ")
            self.lblIDCount.setText("Material ID's: ")
            self.pixmap.fill(self.colorBlack)
            self.lblUVUtilPic.setPixmap(self.pixmap)
            self.btnZeroPolySelector.setDisabled(True)
            self.btnMergeSGSelector.setEnabled(False)
            self.btnZeroSGSelector.setEnabled(False)

            #style to default
            self.lblShapes.setStyleSheet("")
            self.lblpolycount.setStyleSheet("")
            self.lblUVVert.setStyleSheet("")
            self.lblMatIDQ.setStyleSheet("")
            self.lblUVarea.setStyleSheet("")
            self.lblSmoothGroupCount.setStyleSheet("")
            self.lblUVUt.setStyleSheet("")
            self.lblMapChanQ.setStyleSheet("")
            self.lbltriscount.setStyleSheet("")
            self.lblUVO.setStyleSheet("")
            self.lblIDCount.setStyleSheet("")
            
            #clear conclusion
            self.txtbrowGenConclusion.setHtml("")
            
        if what_clear == '2':
            self.lbInfo01.setStyleSheet("")
            self.lbInfo02.setStyleSheet("")

    #Responce and trim
    def SimpleActionResponce(self, config, label_01, label_02, label_03):
        
        #trim lables
        if len(label_01) > 67:
            short_label_01 = label_01[:67] + "..."
        else:
            short_label_01 = label_01

        if len(label_02) > 67:
            short_label_02 = label_02[:67] + "..."
        else:
            short_label_02 = label_02

        if config == '1':
            self.lbInfo01.setText(short_label_01)
            print ('\n', 'PolygonTools:\n' + label_01, '\n')
        
        if config == '2':
            self.lbInfo02.setText(short_label_02)
            print ('\n', 'PolygonTools:\n' + label_02, '\n')
            
        if config == '12':
            
            self.lbInfo01.setText(short_label_01)
            
            print ('\nPolygonTools:')
            
            if label_01 != '':
                print ('\t', label_01)
        
            self.lbInfo02.setText(short_label_02)
            
            if label_02 != '':
                print ('\t', label_02, '\n')

    #Prepare Mesh
    def btnPrepMeshClicked(self):

        #clear values
        self.valueCleaner("1")
        self.valueCleaner("2")
        
        self.pbChekProgress.setValue(0)
        
        self.lbInfo01.setText("Prepare Oject in Progress...")
        self.lbInfo02.setText("")

        #get current language
        current_languge = cfgl.configLoader()[14]        

        try:
            
            selection_array = checkSelection()
            sel_objects = selection_array[0]
            sel_editable_poly_objects = selection_array[1]
            sel_bones = len(selection_array[2])
            sel_editable_poly_nodes = selection_array[3]

        except:
            
            self.SimpleActionResponce('12', "Please select something. Editable Poly object for example...", '', '')

        if len(sel_editable_poly_objects) > 0:

            self.pbChekProgress.setValue(0)		

            #runPrepare
            conclusion_data = prepareMesh(sel_editable_poly_objects)

            #get all info about scene name
            scene_name_data = sceneName()
            
            #add scene name info
            conclusion_data.append(scene_name_data[3])

            #set conclusion text
            conclusion_text = conclusion.prepMeshConclusion(current_languge, conclusion_data)
            
            #conclusion output
            self.txtbrowGenConclusion.setHtml(conclusion_text)       

            #sceneName
            self.SimpleActionResponce('2', '', scene_name_data[1], '') 
            self.lbInfo02.setStyleSheet(scene_name_data[2])                 

            self.pbChekProgress.setValue(100)		

            print ("")

            #final text
            if len(sel_editable_poly_objects) == 1:                
                self.SimpleActionResponce('1', (sel_editable_poly_objects[0] + " was prepared!"), '', '')
                self.lbInfo01.setStyleSheet("background-color:#3D523D;")
            else:
                self.SimpleActionResponce('1', (str(len(sel_editable_poly_objects)) + " objects was prepared!"), '', '')
                self.lbInfo01.setStyleSheet("background-color:#3D523D;")

        else:
            self.SimpleActionResponce('12', "Please select something. Editable Poly object for example...", '', '')   
            conclusion_text = conclusion.noSelection(current_languge, "prepare_mesh")
            self.txtbrowGenConclusion.setHtml(conclusion_text)
            self.valueCleaner("2")            
    

    #Prepare scene
    def btnPrepSceneClicked(self):

        #clear values
        self.valueCleaner("1")
        self.valueCleaner("2")

        #get current language
        current_languge = cfgl.configLoader()[14]        

        self.pbChekProgress.setValue(0)

        #prepare scene batch
        conclusion_data = prepareScene()

        #get all info about scene name
        scene_name_data = sceneName()

        #strip path
        localTexturePathFix()

        #add scene name info
        conclusion_data.append(scene_name_data[3])

        #set conclusion text
        conclusion_text = conclusion.prepSceneConclusion(current_languge, conclusion_data)

        #conclusion output
        self.txtbrowGenConclusion.setHtml(conclusion_text)
    
        #sceneName
        self.SimpleActionResponce('2', '', scene_name_data[1], '') 
        self.lbInfo02.setStyleSheet(scene_name_data[2])
            
        self.SimpleActionResponce('1', 'Scene was successfully prepared!', '', '')
        self.lbInfo01.setStyleSheet("background-color:#3D523D;")
    

    #Prepare viewport
    def btnPrepViewClicked(self):

        #clear values
        self.valueCleaner("1")
        self.valueCleaner("2")
    
        self.pbChekProgress.setValue(0)
    
        self.valueCleaner("2")
        
        #prepare batch
        conclusion_data = prepareViewport()
                
        #get current language
        current_languge = cfgl.configLoader()[14]
        
        #set conclusion text
        conclusion_text = conclusion.prepViewportConclusion(current_languge, conclusion_data)
        
        #conclusion output
        self.txtbrowGenConclusion.setHtml(conclusion_text)        
        
        self.pbChekProgress.setValue(100)

        self.SimpleActionResponce('1', 'Viewports was successfully prepared!', '', '')
        self.lbInfo01.setStyleSheet("background-color:#3D523D;")


    def getStatistics(self):

        #clear values
        self.valueCleaner("1")
        self.valueCleaner("2")

        #get current language
        current_languge = cfgl.configLoader()[14]

        stat_conclusion_data = []
        
        try:            
            selection_array = checkSelection()
            
            sel_objects = selection_array[0]
            sel_editable_poly_objects = selection_array[1]            
            sel_bones = len(selection_array[2])
            sel_editable_poly_nodes = selection_array[3]

        except:

            self.SimpleActionResponce('12', "Please select something. Editable Poly object for example...", '', '')

        if len(sel_editable_poly_objects) > 0:

            #UnsupportedObjects, TotalPoly, TotalTris, TotalVert, TotalUVvert, all_objects_polycount, problems_list, object_with_transform
            geo_stat_data = geoStat(sel_objects, sel_editable_poly_objects)

            #0 - poly and no poly
            if geo_stat_data[0] > 0:
                self.lblShapes.setStyleSheet("color:#f26522;")
                self.lblShapes.setText('Editable Poly Objects: ' + str(len(sel_editable_poly_objects)) + " | Not Poly: "+ str(geo_stat_data[0]))
                stat_conclusion_data.append(str(geo_stat_data[0]))
            else:
                self.lblShapes.setText("Editable Poly Objects: " + str(len(sel_editable_poly_objects)))
                stat_conclusion_data.append(True)

            print ('\n', "POLYCOUNT"            )
            #Polygons
            self.lblpolycount.setText('Polygons: ' + str(geo_stat_data[1]))
            print ('\t', self.lblpolycount.text())
            self.pbChekProgress.setValue(10)

            #Tris
            self.lbltriscount.setText('Triangles: ' + str(geo_stat_data[2]))
            print ('\t', self.lbltriscount.text())
            self.pbChekProgress.setValue(20)
            
            #Vertices
            self.lblvertcount.setText('Vertices: ' + str(geo_stat_data[3]))
            print ('\t', self.lblvertcount.text())
            self.pbChekProgress.setValue(30)
            
            #Bones
            self.lblJointsCount.setText('Bones: ' + str(sel_bones))

            #2 - UV Chan Probl 
            if len(geo_stat_data[6]) == 0:
                self.lblUVVert.setText('UV-vertices: ' + str(geo_stat_data[4]))
                print ('\t', self.lblUVVert.text())
                self.pbChekProgress.setValue(40)
                stat_conclusion_data.append(True)
            else:
                self.lblUVVert.setStyleSheet("color:#f26522;")
                self.lblUVVert.setText('UV-vertices: ' + str(geo_stat_data[4]) + " | UV Channel problems detected! See log.")
                print ('\t', self.lblUVVert.text(), "Objects with problems:", geo_stat_data[6])
                self.pbChekProgress.setValue(40)
                stat_conclusion_data.append(False)

            #3 - if has transform
            if len(geo_stat_data[7]) > 0:
                self.lblShapes.setStyleSheet("color:#f26522;")
                self.lblShapes.setText(self.lblShapes.text() + " | " + str(len(geo_stat_data[7])) + " has transformation.")

                print ('\n', "Objects that have a Transformation:")
                for i in range(len(geo_stat_data[7])):
                    print ('\t', (str(i+1) + "."), geo_stat_data[7][i])
                
                stat_conclusion_data.append(False)
            else:
                stat_conclusion_data.append(True)

            # 0-one_mat, many_mat, no_mat, unique_mat, 4-unsup_mat
            #run materials stat
            print ('\n', "MATERIALS")
            mat_stat_data = matStat(sel_editable_poly_nodes)

            ObjectsCount = len(sel_editable_poly_objects)
                        
            #4 - materials
            if mat_stat_data[5][0] == len(sel_editable_poly_objects) and ObjectsCount == 1:
                self.lblMatIDQ.setText("Materials: " + str(len(mat_stat_data[0])))            
                stat_conclusion_data.append(True)
            elif  mat_stat_data[5][0] == len(sel_editable_poly_objects) and ObjectsCount > 1:
                self.lblMatIDQ.setText("Materials: " + str(len(mat_stat_data[0])) + " objects has 1.")
                stat_conclusion_data.append(True)
            elif mat_stat_data[5][0] == 0 and mat_stat_data[5][2] > 0 and ObjectsCount == 1: #one obj no mat
                self.lblMatIDQ.setStyleSheet("color:#f26522;")
                self.lblMatIDQ.setText("Materials: No materials assigned to object! | See log for details.")
                stat_conclusion_data.append(False)
            elif mat_stat_data[5][0] == 0 and mat_stat_data[5][2] == ObjectsCount: #many obj no mat
                self.lblMatIDQ.setStyleSheet("color:#f26522;")
                self.lblMatIDQ.setText("Materials: no materials assigned")
                stat_conclusion_data.append(False)
            elif mat_stat_data[5][0] > 0 and mat_stat_data[5][2] > 0 and mat_stat_data[5][1] > 0 and ObjectsCount > 1: #many obj one mat and zero
                self.lblMatIDQ.setStyleSheet("color:#f26522;")
                self.lblMatIDQ.setText("Materials: " + str(mat_stat_data[5][0]) + " obj. has 1 | " + str(mat_stat_data[5][1]) + " - many | " + str(mat_stat_data[5][2]) + " - zero | See log.")
                stat_conclusion_data.append(False)
            elif mat_stat_data[5][0] > 0 and mat_stat_data[5][2] > 0 and ObjectsCount > 1: #many obj one mat and zero
                self.lblMatIDQ.setStyleSheet("color:#f26522;")
                self.lblMatIDQ.setText("Materials: " + str(mat_stat_data[5][0]) + " obj. has 1 | " + str(mat_stat_data[5][2]) + " - zero | See log.")
                stat_conclusion_data.append(False)
            else:
                self.lblMatIDQ.setStyleSheet("color:#f26522;")
                self.lblMatIDQ.setText("Materials: " + str(mat_stat_data[5][0]) + " objects has 1 | " + str(mat_stat_data[5][1]) + " - many | See log.") #many obj one mat and many
                stat_conclusion_data.append(False)

            print ('\n', self.lblMatIDQ.text())

            self.pbChekProgress.setValue(50)
                
            #GET OVERLAP
            #object_geo_area, object_uv_area, objects_with_uv_overlaps, full_uv_overlap, objects_with_zero_area
            print ('\n', "OVERLAPS")
            overlap_stat_data = overlapStat(sel_editable_poly_nodes, geo_stat_data[5])

            #5  overlaps
            if len(overlap_stat_data[3]) == 0:
                self.lblUVO.setText("Overlaps: 0")
                stat_conclusion_data.append(True)
            else:
                self.lblUVO.setText("Overlaps: present in " + str(len(overlap_stat_data[3])) + " objects")
                stat_conclusion_data.append(False)

            print ('\t', self.lblUVO.text(),'\n')

            if len(overlap_stat_data[3]) != 0:
                print ("List of objects with 100% overlap:")
                for i in range(len(overlap_stat_data[3])):
                    print ('\t', (str(i+1) + "."), overlap_stat_data[3][i])

            if len(overlap_stat_data[3]) > 0:
                self.lblUVO.setStyleSheet("color:#f26522;") 
                self.lblUVO.setText(self.lblUVO.text() + " | "+ str(len(overlap_stat_data[3])) + " - has 100%.")
                print ("\nNote: " + str(len(overlap_stat_data[3])) + " objects has 100% overlap.")
                stat_conclusion_data.append(str(len(overlap_stat_data[3])))
            else:
                stat_conclusion_data.append(True)
                pass

            self.pbChekProgress.setValue(60)

            # 0-uv_outside, 1-unique_shape_outside
            #run UV 1-0 range stat
            print ('\n', "UV-RANGE")
            uvrange_stat_data = uvRangeStat(sel_editable_poly_nodes)
            
            #6 - uv in 1
            if len(uvrange_stat_data[0]) == 0 and len(sel_editable_poly_objects) > 1:
                self.lblUVarea.setText ("UV in [0,1]: True for " + str(len(sel_editable_poly_objects)) + " object(s).")
                print ('\t', self.lblUVarea.text())
                stat_conclusion_data.append(True)
            elif len(uvrange_stat_data[0]) == 0 and len(sel_editable_poly_objects)==1:
                self.lblUVarea.setText ("UV in [0,1]: True")
                print ('\t', self.lblUVarea.text()                )
                stat_conclusion_data.append(True)
            elif len(uvrange_stat_data[0]) > 0:
                self.lblUVarea.setStyleSheet("color:#f26522;")
                self.lblUVarea.setText ("UV in [0,1]: False for " + str(len(uvrange_stat_data[0])) + " object(s) from " + str(len(sel_editable_poly_objects)))
                print ('\n', self.lblUVarea.text())
                stat_conclusion_data.append(False)
            
            self.pbChekProgress.setValue(70)

            #MAP CHANNEL
            #one_uv_set, many_uv_sets   
            print ('\n', "MAP CHANNELS")
            uvset_stat_data = uvSetStat(sel_editable_poly_nodes)

            #7 - map channels
            if len(uvset_stat_data[1]) == 0 and len(sel_editable_poly_objects) > 1:
                self.lblMapChanQ.setText(str(len(uvset_stat_data[0])) + " objects has one Map Channel.")
                print ('\t', self.lblMapChanQ.text())
                stat_conclusion_data.append(True)
            elif len(uvset_stat_data[1]) == 0 and len(sel_editable_poly_objects) == 1:
                self.lblMapChanQ.setText("Map Channels: 1")
                print ('\t', self.lblMapChanQ.text())
                stat_conclusion_data.append(True)
            else:
                self.lblMapChanQ.setStyleSheet("color:#f26522;")
                self.lblMapChanQ.setText(str(len(uvset_stat_data[0])) + " objects has one | " + str(len(uvset_stat_data[1])) + " objects > then one Map Channels.")
                print ('\t', self.lblMapChanQ.text())
                stat_conclusion_data.append(False)            

            self.pbChekProgress.setValue(80)

            # 0-obj_without_problems, obj_with_merged_sg, obj_without_sg, obj_with_many_sg, sg_count, 5 - sg_check_result, many_id, 7-normal_id, 8 - objects_poly_problems
            print ('\n', "SMOOTHING GROUPS, MATERIAL ID's and SMALL POLYGONS")
            smooth_group_data = smoothingGroupsCheck(sel_editable_poly_nodes)
            
            SmoothCheckResult = (', '.join(smooth_group_data[5]))

            self.merged_sg = smooth_group_data[1]
            self.no_sg = smooth_group_data[2]

            if len(self.merged_sg) > 0:
                self.btnMergeSGSelector.setEnabled(True)
            if len(self.no_sg) > 0:
                self.btnZeroSGSelector.setEnabled(True)

            #8 - SG
            if len(smooth_group_data[0]) == 1 and len(smooth_group_data[1]) == 0 and len(smooth_group_data[2]) == 0 and len(smooth_group_data[3]) == 0:
                self.lblSmoothGroupCount.setText ("Smoothing groups: " + str(len(smooth_group_data[4])))
                stat_conclusion_data.append(True)
            elif len(smooth_group_data[0]) > 1 and len(smooth_group_data[1]) == 0 and len(smooth_group_data[2]) == 0 and len(smooth_group_data[3]) == 0:
                self.lblSmoothGroupCount.setText ("Smoothing groups: " + str(len(smooth_group_data[0])) + " objects don't have problems with SG")
                stat_conclusion_data.append(False)
            elif len(smooth_group_data[0]) >= 1 and len(smooth_group_data[5]) > 1:
                self.lblSmoothGroupCount.setStyleSheet("color:#f26522;")
                self.lblSmoothGroupCount.setText ("Smoothing groups: " + str(len(smooth_group_data[0])) + " obj. - OK. Other has problems | See log")
                stat_conclusion_data.append(False)
            else:
                self.lblSmoothGroupCount.setStyleSheet("color:#f26522;")
                self.lblSmoothGroupCount.setText ("Smoothing groups: found " + SmoothCheckResult + " SG | See log")
                stat_conclusion_data.append(False)

            print ('\n', self.lblSmoothGroupCount.text())

            self.pbChekProgress.setValue(90)          

            #9 - ID
            if len(smooth_group_data[7]) == 1 and len(sel_editable_poly_objects)==1:
                self.lblIDCount.setText("Material ID's: 1")
                stat_conclusion_data.append(True)
            elif len(smooth_group_data[7]) == len(sel_editable_poly_objects):
                self.lblIDCount.setText("Material ID's: " + str(ObjectsCount) + " objects has 1")
                stat_conclusion_data.append(True)
            elif len(smooth_group_data[7]) > 0 and len(smooth_group_data[6]) > 0:
                self.lblIDCount.setStyleSheet("color:#f26522;")
                self.lblIDCount.setText("Material ID's: " + str(len(smooth_group_data[7])) + " objects has 1 | " + str(len(smooth_group_data[6])) + " more then 1." )
                stat_conclusion_data.append(False)
            elif len(smooth_group_data[7]) == 0 and len(smooth_group_data[6]) > 0:
                self.lblIDCount.setStyleSheet("color:#f26522;")
                self.lblIDCount.setText("Material ID's: " + str(len(smooth_group_data[6])) + " object(s) has more then 1." )
                stat_conclusion_data.append(False)

            print ('\n', self.lblIDCount.text())

            self.ObjectWithZeroFaces = smooth_group_data[8]

            #10 - poly problems
            if len(smooth_group_data[8]) > 0 and len(smooth_group_data[9]) == 0:
                self.lblpolycount.setStyleSheet("color:#f26522;")
                self.lblpolycount.setText('Polygons: ' + str(geo_stat_data[1]) + " | " + str(len(smooth_group_data[8])) + " obj. has tiny polygons!")
                self.btnZeroPolySelector.setDisabled(False)
                stat_conclusion_data.append(False)
            elif len(smooth_group_data[8]) > 0 and len(smooth_group_data[9]) > 0:
                self.lblpolycount.setStyleSheet("color:#f26522;")
                self.lblpolycount.setText('Polygons: ' + str(geo_stat_data[1]) + " | " + str(len(smooth_group_data[8])) + " obj. has tiny pol." + " | " + str(len(smooth_group_data[9])) + " invisible pol. found! See log.")
                self.btnZeroPolySelector.setDisabled(False)
                stat_conclusion_data.append(False)
            elif len(smooth_group_data[8]) == 0 and len(smooth_group_data[9]) > 0:
                self.lblpolycount.setStyleSheet("color:#f26522;")
                self.lblpolycount.setText('Polygons: ' + str(geo_stat_data[1]) + " | " + str(len(smooth_group_data[9])) + " invisible polygons found! See log.")
                self.btnZeroPolySelector.setDisabled(False)
                stat_conclusion_data.append(False)
            elif len(smooth_group_data[8]) == 0 and len(smooth_group_data[9]) == 0:
                stat_conclusion_data.append(True)

            self.pbChekProgress.setValue(95)
            
            print ('\n', "UV UTILIZATION", '\n', "Per Object:")
            
            all_uv_areas =[]

            self.pbChekProgress.setRange(1, ObjectsCount)

            #selected nodes
            SelectedNodes = rt.selection
            
            #UVarea - check LOW UV-utilization
            for i in range(len(sel_editable_poly_nodes)):
                
                self.pbChekProgress.setValue(i)

                one_obj_arr = []
                one_obj_arr.append(sel_editable_poly_nodes[i])

                #one obj util
                UVAreaSum = uvUtilStat(one_obj_arr)
                if len(sel_editable_poly_nodes[i].name) == 0:
                    print ('\t', str(i+1) + ".", "noname object #" + str(i), "-", UVAreaSum[0], "%"                )
                else:
                    print ('\t', str(i+1) + ".", sel_editable_poly_nodes[i].name, "-", UVAreaSum[0], "%"                )
                
                if UVAreaSum[0] > 0:                    
                    all_uv_areas.append(UVAreaSum[0])

            #return selection
            rt.select(selection_array[3])
            uvutil_stat_data = uvUtilStat(sel_editable_poly_nodes)
        
            #total util
            self.lblUVUtilPic.setPixmap(uvutil_stat_data[1])                 
                
            uvarea_sum = sum(all_uv_areas)
            final_uv_area = uvutil_stat_data[0]
            
            try:
                uvarea_avg = int(sum(all_uv_areas)/len(all_uv_areas))
                self.lblUVUtAvg.setText ("Average UV-Utilization: " + str(uvarea_avg) + "%")  
            except:
                print ("UV Area Array values:", sum(all_uv_areas), "/", len(all_uv_areas) )
                print ("Can't calculate average UV-Utilization. Maybe problems with UV layout.")
                self.lblUVUtAvg.setText ("Average UV-Utilization: not available. See log")

            self.lblUVUtilPic.setPixmap(uvutil_stat_data[1])
            final_uv_area = uvutil_stat_data[0]

            #UV ranges
            dangerous_uv_range = range(95,101)
            ideal_uv_range = range(67,95)
            medium_uv_range = range(50,66)
            low_uv_range = range(1,49)
        
            #if 1 obj        
            if (len(sel_editable_poly_objects) == 1):
                self.lblUVUtAvg.setEnabled(False)
            else:
                self.lblUVUtAvg.setEnabled(True)

            #11 - UV Util                        
            if (final_uv_area in ideal_uv_range):
                self.lblUVUt.setStyleSheet("")
                self.lblUVUt.setText ("Total UV-Utilization: " + str(final_uv_area) + "%")     
                stat_conclusion_data.append(True)
                   
            if final_uv_area in medium_uv_range:
                self.lblUVUt.setStyleSheet("")
                self.lblUVUt.setText ("Total UV-Utilization: " + str(final_uv_area) + "% | Try to do more efficiently!")
                stat_conclusion_data.append(True)                

            if (final_uv_area in low_uv_range):
                self.lblUVUt.setStyleSheet("color:#f26522;")
                self.lblUVUt.setText ("Total UV-Utilization: " + str(final_uv_area) + "% | Low!")
                stat_conclusion_data.append(False)
                                
            if (final_uv_area in dangerous_uv_range):
                self.lblUVUt.setStyleSheet("color:#f26522;")
                self.lblUVUt.setText ("Total UV-Utilization: >" + str(final_uv_area) + "% | Check padding, overlap, range!")
                stat_conclusion_data.append(False)

            if final_uv_area == 0:
                self.lblUVUt.setStyleSheet("color:#f26522;")
                self.lblUVUt.setText ("Total UV-Utilization: not available. Error in uvUtilStat function. See Log!")
                stat_conclusion_data.append(False)

            print ('\n', self.lblUVUt.text())
            print ('\n', self.lblUVUtAvg.text()            )

            self.pbChekProgress.setRange(1, 100)
            self.pbChekProgress.setValue(100)

            #set conclusion text
            conclusion_text = conclusion.statConclusion(current_languge, stat_conclusion_data)
            #conclusion output
            self.txtbrowGenConclusion.setHtml(conclusion_text)                    

            if len(sel_editable_poly_objects) == 1:
                self.SimpleActionResponce('12', "Statistics was successfully obtained for 1 object", 'Processed object is ' + sel_editable_poly_objects[0], '')
                self.lbInfo01.setStyleSheet("background-color:#3D523D;")
            else:
                self.SimpleActionResponce('12', ("Statistics was successfully obtained for " + str(len(sel_editable_poly_objects)) + ' Editable Poly objects.'), '', '')
                self.lbInfo01.setStyleSheet("background-color:#3D523D;")

        else:
            self.SimpleActionResponce('12', "Please select something. Editable Poly object for example...", '', '')   
            conclusion_text = conclusion.noSelection(current_languge, "statisctics")
            self.txtbrowGenConclusion.setHtml(conclusion_text)

    #select zero faces
    def selectZeroFaces(self):

        #for selection
        obj_wit_zero_face = []

        current_languge = cfgl.configLoader()[14]

        #one obj
        if len(self.ObjectWithZeroFaces) == 1:

            #ObjectName = self.ObjectWithZeroFaces[0][0][0]

            NodeName = self.ObjectWithZeroFaces[0][0][0]
            Faces = self.ObjectWithZeroFaces[0][1]

            if str(NodeName) != "<Deleted scene node>":
                
                #select Node
                rt.select(NodeName)
                rt.subObjectLevel = 4

                SelectedFaces = ', '.join([str(elements) for elements in Faces])

                rt.execute("$.EditablePoly.SetSelection #Face #{" + SelectedFaces +"}")
                print ("Polygon(s) with very small area (Zero-Area) was selected.\nTheir numbers:\n", SelectedFaces)
                rt.actionMan.executeAction(0, "272")                

                #conclusion
                self.txtbrowGenConclusion.setHtml(conclusion.sgConclusion(current_languge, "PolyZeroArea")) 

            else:
                self.btnZeroPolySelector.setDisabled(True)
                self.txtbrowGenConclusion.setHtml(conclusion.sgErrorConclusion(current_languge))
                print ("PolygonTools. Can't select polygon(s) with Zero-Area. Object(s) is not Exists or other problems.")
        
        else: #many obj
            
            #clear sel
            rt.clearSelection()
            
            for i in range(len(self.ObjectWithZeroFaces)):

                NodeName = self.ObjectWithZeroFaces[i][0][0]                 

                try:
                    obj_wit_zero_face.append(NodeName)
                except:
                    print ("PolygonTools. Can't select polygon(s) with Zero-Area. Object", self.ObjectWithZeroFaces[i][0][0] ,"is not Exists or other problems.")
                            
            if len(obj_wit_zero_face) > 0:
                
                try:
                    rt.select(obj_wit_zero_face)
                    rt.execute ("redrawViews()")

                    print ("Object with Polygon(s) with very small area was selected! It's:")
                    for m in range(len(obj_wit_zero_face)):
                        if len(obj_wit_zero_face[m].name) == 0:
                            print ('\t', (str(m + 1) + "."), "noname object #" + str(m))
                        else: 
                            print ('\t', (str(m + 1) + "."), obj_wit_zero_face[m].name                    )

                    self.btnZeroPolySelector.setDisabled(False)

                    #conclusion
                    self.txtbrowGenConclusion.setHtml(conclusion.sgConclusion(current_languge, "ObjectsZeroArea")) 

                except:
                    print ("PolygonTools. Can't select polygon(s) with Zero-Area. Object(s) is not Exists or other problems.")
                    self.txtbrowGenConclusion.setHtml(conclusion.sgErrorConclusion(current_languge))
                    self.btnZeroPolySelector.setDisabled(True)

#******************

    #select zero SG
    def selectPolyNoSG (self):

        current_languge = cfgl.configLoader()[14]

        #for selection
        obj_wit_zero_sg = []

        if len(self.no_sg) == 1:

            #ObjectName = self.no_sg[0][0][0]
            NodeName = self.no_sg[0][0][0]
            Faces = self.no_sg[0][1]

            if str(NodeName) != "<Deleted scene node>":
                #select Node
                rt.select(NodeName)
                rt.subObjectLevel = 4

                SelectedFaces = ', '.join([str(elements) for elements in Faces])
                rt.execute("$.EditablePoly.SetSelection #Face #{" + SelectedFaces +"}")
                print ("PolygonTools. Polygon(s) without Smoothing Group was selected.\nTheir numbers:\n", SelectedFaces)

                #wireframe and filled selection
                rt.actionMan.executeAction(0, "272")
                rt.actionMan.executeAction(0, "371")

                #conclusion
                self.txtbrowGenConclusion.setHtml(conclusion.sgConclusion(current_languge, "PolyNoSG")) 
            else:
                print ("PolygonTools. Can't select Polygon(s) with Merged Smoothing Groups. Object(s) is not Exists, Deleted or has other problems.")
                self.txtbrowGenConclusion.setHtml(conclusion.sgErrorConclusion(current_languge))
                self.btnZeroSGSelector.setEnabled(False) 

        else:

            #clear sel
            rt.clearSelection()

            for i in range(len(self.no_sg)):
                
                NodeName = self.no_sg[i][0][0]
                
                try:
                    obj_wit_zero_sg.append(NodeName)
                except:
                    print ("PolygonTools. Can't select polygon(s) without Smoothing Groups", self.no_sg[i][0][0] ,"is not Exists or other problems.")
                    self.txtbrowGenConclusion.setHtml(conclusion.sgErrorConclusion(current_languge))
                    self.btnZeroSGSelector.setEnabled(False)  
                            
            if len(obj_wit_zero_sg) > 0:
                
                try:

                    rt.select(obj_wit_zero_sg)
                    rt.execute ("redrawViews()")

                    print ("Object with Polygon(s) without Smoothing Group was selected! It's:")

                    for m in range(len(obj_wit_zero_sg)):
                        if len(obj_wit_zero_sg[m].name) == 0:
                            print ('\t', (str(m + 1) + "."), "noname object #" + str(m))
                        else: 
                            print ('\t', (str(m + 1) + "."), obj_wit_zero_sg[m].name                    )
                                    
                    #conclusion
                    self.txtbrowGenConclusion.setHtml(conclusion.sgConclusion(current_languge, "ObjNoSG"))

                except:
                    print ("PolygonTools. Can't select Polygon(s) without Smoothing Group. Object(s) is not Exists or other problems.")
                    self.txtbrowGenConclusion.setHtml(conclusion.sgErrorConclusion(current_languge))
                    self.btnZeroSGSelector.setEnabled(False) 

#****************************#

    #select MergedSG
    def selectMergedSG (self):

        current_languge = cfgl.configLoader()[14]
        
        #for selection
        obj_with_merged_sg = []
        
        if len(self.merged_sg) == 1:

            NodeName = self.merged_sg[0][0][0]
            Faces = self.merged_sg[0][1]

            #if obj exists
            if str(NodeName) != "<Deleted scene node>":
                #select Node
                rt.select(NodeName)
                rt.subObjectLevel = 4

                SelectedFaces = ','.join([str(elements) for elements in Faces])
                rt.execute("$.EditablePoly.SetSelection #Face #{" + SelectedFaces +"}")
                print ("PolygonTools. Polygon(s) with Merged Smoothing Group was selected.\nTheir numbers:\n", SelectedFaces)
                
                #wireframe and filled selection
                rt.actionMan.executeAction(0, "272")
                rt.actionMan.executeAction(0, "371")

                #conclusion
                self.txtbrowGenConclusion.setHtml(conclusion.sgConclusion(current_languge, "PolyWithMergedSG"))
                
            else:
                print ("PolygonTools. Can't select Polygon(s) with Merged Smoothing Groups. Object(s) is not Exists, Deleted or has other problems.")
                self.txtbrowGenConclusion.setHtml(conclusion.sgErrorConclusion(current_languge))
                self.btnMergeSGSelector.setEnabled(False)

        else:

            #clear sel
            rt.clearSelection()
            
            for i in range(len(self.merged_sg)):
               
                NodeName = self.merged_sg[i][0][0]
                
                try:
                    obj_with_merged_sg.append(NodeName)
                except:
                    print ("PolygonTools. Can't select polygon(s) with Merged Smoothing Groups. Object", self.merged_sg[i][0][0] ,"is not Exists, Deleted or other problems.")
                    self.txtbrowGenConclusion.setHtml(conclusion.sgErrorConclusion(current_languge))
                    self.btnMergeSGSelector.setEnabled(False)
                            
            if len(obj_with_merged_sg) > 0:

                try:
                    rt.select(obj_with_merged_sg)
                    rt.execute ("redrawViews()")

                    print ("Object with Polygon(s) with Merged Smoothing Groups was selected! It's:")
                    
                    for m in range(len(obj_with_merged_sg)):
                        if len(obj_with_merged_sg[m].name) == 0:
                            print ('\t', (str(m + 1) + "."), "noname object #" + str(m))
                        else: 
                            print ('\t', (str(m + 1) + "."), obj_with_merged_sg[m].name                    )
                    
                    #conclusion
                    self.txtbrowGenConclusion.setHtml(conclusion.sgConclusion(current_languge, "ObjWithMergedSG"))

                except:
                    print ("PolygonTools. Can't select Polygon(s) with Merged Smoothing Groups. Object(s) is not Exists, Deleted or other problems.")
                    self.txtbrowGenConclusion.setHtml(conclusion.sgErrorConclusion(current_languge))
                    self.btnMergeSGSelector.setEnabled(False)


    #get dimension of object
    def btnGetDimPressed(self):

        self.pbChekProgress.setValue(0)
        
        #get current language
        current_languge = cfgl.configLoader()[14]

        try:
            
            selection_array = checkSelection()
            sel_objects = selection_array[0]
            sel_editable_poly_objects = selection_array[1]
            sel_bones = len(selection_array[2])

        except:
            
            self.SimpleActionResponce('12', "Please select something. Editable Poly object for example...", '', '')

        ObjectHasTransform = False            

        if len(sel_editable_poly_objects) == 1:

            if self.btnGetDim.isChecked():            
                self.btnGetDim.setText("Show Dimension")
                self.SimpleActionResponce('12', 'Show Dimension is OFF', '', '')    
                self.txtbrowGenConclusion.setHtml( conclusion.genTabIntroConclusion(current_languge) )
                self.btnGetDim.setIcon(self.iconDim)    

                rt.unregisterRedrawViewsCallback(showDimensionInViewport)

            else:    
                self.btnGetDim.setText("Hide Dimension")
                self.SimpleActionResponce('12', "Show Dimension is ON", '', '')

                NodeName = rt.getNodeByName( sel_editable_poly_objects[0] )
                
                #get scale transform
                ScaleXYZ = NodeName.scale
                        
                if sum(ScaleXYZ) != 3.0:
                    self.btnGetDim.setIcon(self.iconDimXForm) 
                    ObjectHasTransform = True            

                rt.registerRedrawViewsCallback(showDimensionInViewport)

                #set conclusion text
                conclusion_text = conclusion.dimensionConclusion(current_languge, ObjectHasTransform)
                
                #conclusion output
                self.txtbrowGenConclusion.setHtml(conclusion_text)        
        
        else:
            
            rt.unregisterRedrawViewsCallback(showDimensionInViewport)
            self.SimpleActionResponce('12', "Please select One Editable Poly object for example...", '', '') 
            self.btnGetDim.setChecked(True)  
            conclusion_text = conclusion.noSelection(current_languge, "dimension")
            self.txtbrowGenConclusion.setHtml(conclusion_text)


def showDimensionInViewport():

    SelectedObjectsCount = rt.selection.count

    if SelectedObjectsCount == 1:
        
        #set line style
        rt.execute("gw.setColor #line gray")
        rt.execute("gw.setTransform($.transform)")

        _bboxLocal = rt.execute ("nodeGetBoundingBox $ $.transform")
        
        #get transform
        _bboxMin = _bboxLocal[0] 
        _bboxMax = _bboxLocal[1]

        #get parts of transform
        _bboxWidth = abs(_bboxMax[0] - _bboxMin[0])
        _bboxHeight = abs(_bboxMax[1] - _bboxMin[1])
        _bboxLength = abs(_bboxMax[2]- _bboxMin[2])

        bboxPoints = []
        temp_a = []

        temp_a = [_bboxMin[0], _bboxMin[1], _bboxMin[2]]
        bboxPoints.append(temp_a)

        temp_a = [_bboxMin[0] + _bboxWidth, _bboxMin[1], _bboxMin[2]]
        bboxPoints.append(temp_a)

        temp_a = [_bboxMin[0], _bboxMin[1] + _bboxHeight, _bboxMin[2]]
        bboxPoints.append(temp_a)

        temp_a = [_bboxMin[0] + _bboxWidth, _bboxMin[1] + _bboxHeight, _bboxMin[2]]
        bboxPoints.append(temp_a)

        temp_a = [_bboxMax[0] - _bboxWidth, _bboxMax[1], _bboxMax[2]]
        bboxPoints.append(temp_a)

        temp_a = [_bboxMax[0], _bboxMax[1] - _bboxHeight, _bboxMax[2]]
        bboxPoints.append(temp_a)

        temp_a = [_bboxMax[0] - _bboxWidth,  _bboxMax[1] - _bboxHeight, _bboxMax[2]]
        bboxPoints.append(temp_a)

        temp_a = [_bboxMax[0], _bboxMax[1], _bboxMax[2]]
        bboxPoints.append(temp_a)

        p = []

        for n in range(len(bboxPoints)):
            StrVal = str(bboxPoints[n])
            Point3Val = rt.execute ("gw.wTransPoint " + StrVal )
            tmp_a = [Point3Val[0], Point3Val[1], Point3Val[2]]
            p.append(tmp_a)

        for n in range(len(p)):
            StrVal = str(p[n])
            rt.execute("gw.wMarker " + StrVal + "#xMarker color:gray")

        draw_array = []

        draw_array.append(p[0])
        draw_array.append(p[1])
        draw_array.append(p[3])
        draw_array.append(p[2])
        draw_array.append(p[0])
        draw_array.append(p[6])
        draw_array.append(p[4])
        draw_array.append(p[7])
        draw_array.append(p[5])
        draw_array.append(p[6])
        draw_array.append(p[0])
        draw_array.append(p[1])
        draw_array.append(p[5])
        draw_array.append(p[7])
        draw_array.append(p[3])
        draw_array.append(p[2])
        draw_array.append(p[4])

        #create array
        p_array = ','.join([str(elements) for elements in draw_array])

        rt.execute("gw.wPolyline #(" + p_array + ") false")

        #get scale Z
        sizeColor = "white"
        ScaleValueZ = rt.execute("$.scale.z")

        if ScaleValueZ != 1.0:
            sizeColor = "red"

        ValXHeight = str(bboxPoints[6][0] + (bboxPoints[7][0] - bboxPoints[6][0])/2)
        ValYHeight = str(bboxPoints[6][1] + (bboxPoints[7][1] - bboxPoints[6][1])/2)
        ValZHeight = str(bboxPoints[6][2])
        rt.execute("gw.wText (gw.wTransPoint [" + ValXHeight  + "," + ValYHeight  + "," + ValZHeight  + "] )(\"Height: \" + units.formatValue " + str(_bboxLength) + ")" + "color:" + sizeColor )

        #get scale X
        sizeColor = "white"
        ScaleValueX = rt.execute("$.scale.x")

        if ScaleValueX != 1.0:
            sizeColor = "red"

        ValXLenght = str(bboxPoints[0][1])
        ValYLenght = str(bboxPoints[0][1] + (bboxPoints[2][1] - bboxPoints[0][1])/2)
        ValZLenght = str(bboxPoints[0][2])
        rt.execute("gw.wText (gw.wTransPoint [" + ValXLenght + "," + ValYLenght + "," + ValZLenght + "] )(\"Lenght: \" + units.formatValue " + str(_bboxHeight) + ")" + "color:" + sizeColor )

        #get scale Y
        sizeColor = "white"
        ScaleValueY = rt.execute("$.scale.y")

        if ScaleValueY != 1.0:
            sizeColor = "red"

        ValXWidth = str(bboxPoints[0][1] + (bboxPoints[2][1] - bboxPoints[0][1])/2)
        ValYWidth = str(bboxPoints[0][1])
        ValZWidth = str(bboxPoints[0][2])
        rt.execute("gw.wText (gw.wTransPoint [" + ValXWidth + "," + ValYWidth + "," + ValZWidth + "] )(\"Width: \" + units.formatValue " + str(_bboxWidth) + ")" + "color:" + sizeColor )

        rt.execute("gw.enlargeUpdateRect #whole")
        rt.execute("gw.updateScreen()")


#procedure check selection object type and objects count    
def checkSelection():

    print ("----------------------------------", '\n', "Selection information:")
    
    #arrays for objects
    all_sel_objects = []
    editable_poly_objects = []
    bones_objects = []

    editable_poly_nodes = []
    other_nodes = []

    #selected obj
    SelectedObjectsCount = rt.selection.count

    if SelectedObjectsCount > 0:
        
        #selected nodes
        SelectedNodes = rt.selection

        for c in SelectedNodes:
            
            #temp name                    
            try:
                TempObjectName = str(c.name)
            
                #rename if zero name
                if len(c.name) == 0:
                    c.name = "pt_renamed_object_" + str(random.randrange(1, 1000)) #random rename
                    TempObjectName = c.name
                    print ('\t', "Object has been automatically renamed because he didn’t have a name! New name:", c.name)
            except:
                c.name = "pt_renamed_object_" + str(random.randrange(1, 1000)) #random rename
                TempObjectName = c.name
                print ('\t', "Some Kind Name Errors Detected! Object has been automatically renamed. New Name:", c.name)

            #rename if bad symbols
            if "\'" in TempObjectName:    
                ObjectName = TempObjectName.replace("\'", "")
                c.name = ObjectName
                print ("ATTENTION! Object with name", TempObjectName, "was renamed. Because incorrect characters were used. New name:", ObjectName)
            else:
                ObjectName = TempObjectName

            #all selected objects    
            all_sel_objects.append(ObjectName)
        
            #class names
            ObjectType = str(rt.classOf(c))
            
            #poly objects
            if ObjectType == "Editable_Poly":
                editable_poly_objects.append(ObjectName)
                editable_poly_nodes.append(c)            
            #bones
            elif ObjectType == "BoneGeometry":
                bones_objects.append(ObjectName)		
                other_nodes.append(c)
            else:
                other_nodes.append(c)

            if len(other_nodes) > 0:
                for i in range(len(other_nodes)):
                    rt.deselect (other_nodes[i])
    
    print ('\t', "1. Total Selected Objects -", SelectedObjectsCount)
    print ('\t', "2. Editable Poly Objects -", len(editable_poly_objects))
    print ('\t', "3. Bones -", len(bones_objects))
    print ("----------------------------------")

    return all_sel_objects, editable_poly_objects, bones_objects, editable_poly_nodes

#geometry sttistics
def geoStat(total_objects, editable_poly_objects):

    UnsupportedObjects = 0
    all_objects_polycount = []

    TotalPoly = 0    
    TotalTris = 0
    TotalVert = 0
    TotalUVvert = 0    

    UnsupportedObjects = len(total_objects) - len(editable_poly_objects)

    #empty array
    problems_list = []

    object_with_transform = []

    for i in range(len(editable_poly_objects)):
        
        ObjectName = editable_poly_objects[i]
        NodeName = rt.getNodeByName( ObjectName )

        #get faces
        CurrentObjectsFacesCount = NodeName.faces.count

        #total poly
        TotalPoly = TotalPoly + CurrentObjectsFacesCount
        all_objects_polycount.append(CurrentObjectsFacesCount)

        #get transform XYZ
        ScaleXYZ = NodeName.scale

        if sum(ScaleXYZ) != 3.0:
            object_with_transform.append(ObjectName)

        #get tris
        CurrentObjectsTrisCount = NodeName.mesh.numfaces
        TotalTris = TotalTris + CurrentObjectsTrisCount
        
        #get vertex
        CurrentObjectsVertexCount = NodeName.vertices.count
        TotalVert = TotalVert + CurrentObjectsVertexCount

        #get UV-vertex
        try:
            CurrentObjectsUVVertexCount = rt.polyop.getNumMapVerts(NodeName, 1)
            TotalUVvert = TotalUVvert + CurrentObjectsUVVertexCount
        except:
            problems_list.append(ObjectName)
            TotalUVvert = 0

    return UnsupportedObjects, TotalPoly, TotalTris, TotalVert, TotalUVvert, all_objects_polycount, problems_list, object_with_transform

#overlap statistics
def overlapStat(sel_editable_poly_nodes, all_objects_polycount):

    UVOverlap = 0
    objects_with_uv_overlaps = []
    full_uv_overlap = []
    object_uv_area = []
    object_geo_area = []
    objects_with_zero_area = []
    
    #get selection
    SelectedNodes = rt.selection

    rt.execute("max modify mode")

    for i in range(len(sel_editable_poly_nodes)):
            
        NodeName = sel_editable_poly_nodes[i]

        #select Node
        rt.select(NodeName)

        #sel all polygons
        rt.subObjectLevel = 4
        rt.execute ("max select all")
        
        try: 
            #assign Unvrap
            rt.modPanel.addModToSelection (rt.Unwrap_UVW ())

            #set UV Channel
            UVChannel = "1"
            rt.execute ("$.unwrap_uvw.unwrap.setMapChannel " + UVChannel)

            rt.execute ("$.modifiers[#unwrap_uvw].selectOverlappedFaces()")

            #select overlap
            OverlapFaces = rt.execute ("($.Unwrap_UVW.getSelectedFaces()).numberSet")

            UVOverlap = OverlapFaces
        except:
            print ("WARNING! " + sel_editable_poly_nodes[i].name + " | UVChannel: " + UVChannel + " - Zero-polygon found!")
            UVOverlap = 0

        if UVOverlap != 0:
            objects_with_uv_overlaps.append(UVOverlap)

        #if 100% overlap
        if UVOverlap == all_objects_polycount[i]:
            full_uv_overlap.append(sel_editable_poly_nodes[i].name)

        #del modifier
        rt.execute ("macros.run \"Modifier Stack\" \"Convert_to_Poly\"")

        #return obj mode
        rt.subObjectLevel = 0

    #return selection
    rt.select(SelectedNodes)

    return object_geo_area, object_uv_area, objects_with_uv_overlaps, full_uv_overlap, objects_with_zero_area

#uvsets statistics
def uvSetStat (sel_editable_poly_nodes):

    TotalMapChannels = 0
    one_map_channel = []
    many_map_channels = []    

    for i in range(len(sel_editable_poly_nodes)):
        
        #get node
        ObjectNode = sel_editable_poly_nodes[i]   
        ObjectName = sel_editable_poly_nodes[i].name

        #get current Map ChannelsCount
        TotalMapChannels = rt.polyop.getNumMaps(ObjectNode)

        if TotalMapChannels == 2:
            one_map_channel.append(sel_editable_poly_nodes[i])
        else:
            many_map_channels.append(sel_editable_poly_nodes[i])
            
    return one_map_channel, many_map_channels  


def uvRangeStat(sel_editable_poly_nodes):

    uv_outside = []

    #unique shapes with UV outside
    unique_shape_outside = []

    uvChannels = [1]
    uvVertexCount = 0

    for i in range(len(sel_editable_poly_nodes)):
        
        #ObjectName = editable_poly_objects[i]
        #get node by name
        ObjectNode = sel_editable_poly_nodes[i]
        ObjectName = sel_editable_poly_nodes[i].name   

        for k in range(1, len(uvChannels) + 1):
            try:
                #UV vertex count
                CurrentObjectsUVVertexCount = rt.polyop.getNumMapVerts(ObjectNode, k)
            except:
                CurrentObjectsUVVertexCount = 0
                print ("WARNING! " + ObjectName + " | Map Channel: " + str(k) + " - Zero-polygon found!")
            
            for l in range(1, CurrentObjectsUVVertexCount):
                
                #get point 3 data
                Point3 = rt.polyop.getMapVert(ObjectNode, 1, l)

                #compare x-y coords
                if Point3[0] > 1.0 or Point3[1] > 1.0 or Point3[0] < 0 or Point3[1] < 0:                    
                    uv_outside.append(ObjectNode)

    #remove doubles
    uv_outside = list(dict.fromkeys(uv_outside))

    for iz in uv_outside:
            #if iz not in unique_shape_outside:
        unique_shape_outside.append(iz)

    #remove doubles
    unique_shape_outside = list(dict.fromkeys(unique_shape_outside))
    
    if len(unique_shape_outside) > 0:
        
        print ("List of objects with UV not in [0,1] range:")
        
        for i in range(len(unique_shape_outside)):
            if len(unique_shape_outside[i].name ) == 0:
                print ('\t', (str(i+1) + "."), "noname object #" + str(i))
            else: 
                print ('\t', (str(i+1) + "."), unique_shape_outside[i].name )

    return uv_outside, unique_shape_outside


#material statistics
def matStat(sel_editable_poly_nodes):

    #mat var
    one_mat = []
    many_mat = []
    no_mat = []
    unique_mat = []

    #unsupported materials
    unsup_mat = []
    mat_summary = []

    print ("List of Materials on Scene:")
    for i in range(len(sel_editable_poly_nodes)):
                
        NodeName = sel_editable_poly_nodes[i]

        CurrentMat = NodeName.material       

        try:
            #get mat class
            MaterialClass = str(rt.classOf(CurrentMat))
            
            #get mat name
            MaterialName =  str(NodeName.material.name)
            
            if MaterialName not in unique_mat:
                unique_mat.append(MaterialName)

        except:

            MaterialClass = "None"
            MaterialName = "None"

        print ('\t', (str(i+1) + "."), NodeName.name , "| Material Class:", MaterialClass, "| Name:", MaterialName        )

        if MaterialClass == "Multimaterial":
            
            MaterialsList = NodeName.material.materialList
            
            print ('\t\t', "Multi/Sub-Object '" + MaterialName  + "' sub-materials list:")
            
            for k in range(len(MaterialsList)):
                
                #get sub mat
                SubMat = MaterialsList[k]
                
                if SubMat != None:
                    SubMatClass = rt.classOf(MaterialsList[k])
                    SubMatName = SubMat.name
                    print ('\t\t', (str(k+1) + "."), "Material Class:", SubMatClass, "| Name:", SubMatName)
                else:
                    SubMatClass = "None"
                    SubMatName = "None"
                                
        if MaterialClass == "None":
            no_mat.append(NodeName)
        elif MaterialClass == "Standardmaterial":
            one_mat.append(NodeName)
        elif MaterialClass == "Multimaterial":
            many_mat.append(NodeName)
        else:
            unsup_mat.append(NodeName)

    mat_summary.append(len(one_mat))
    mat_summary.append(len(many_mat))
    mat_summary.append(len(no_mat))
    mat_summary.append(len(unique_mat))
    mat_summary.append(len(unsup_mat))

    return one_mat, many_mat, no_mat, unique_mat, unsup_mat, mat_summary


def smoothingGroupsCheck(sel_editable_poly_nodes):

    all_smg = []

    obj_without_problems = []
    obj_with_merged_sg = []
    obj_without_sg = []
    obj_with_many_sg = []

    sg_check_result = []

    normal_id = []
    many_id = []

    objects_poly_problems = []

    invisible_polygons = []

    SmallArea = 0.001

    #Smooth group array
    for x in range (0, 31):
        sg = pow(2, x)
        all_smg.append(sg)    

    for k in range(len(sel_editable_poly_nodes)):
        
        #ObjectName = editable_poly_objects[k]
        NodeName = sel_editable_poly_nodes[k]

        #get faces
        CurrentObjectsFacesCount = NodeName.faces.count

        #array for SG
        pol_without_sg = []
        pol_with_merged_sg = []
        sg_count = []
        id_count = []

        #array for zeropoly
        small_polygons = [0] * 2
        for z in range(2):
            small_polygons[z] = [] * 1

        #array for merged_sg
        merged_sg = [0] * 2
        for z in range(2):
            merged_sg[z] = [] * 1

        #array for merged_sg
        without_sg = [0] * 2
        for z in range(2):
            without_sg[z] = [] * 1

        for i in range(1, CurrentObjectsFacesCount + 1):

            CurrentSmoothGroup = rt.polyop.getFaceSmoothGroup (NodeName, i)
            
            #Get ID            
            try:
                CurrentID = rt.polyop.getFaceMatID (NodeName, i)
            except:
                invisible_polygons.append(i)
            
            CurrentPolArea = rt.polyop.getFaceArea (NodeName, i)

            #no sg
            if CurrentSmoothGroup == 0:
                if NodeName not in without_sg[0]:
                    without_sg[0].append(NodeName)
                without_sg[1].append(i)
            
            #norm sg
            if (CurrentSmoothGroup != 0) and (CurrentSmoothGroup in all_smg) and (CurrentSmoothGroup not in sg_count):
                sg_count.append(CurrentSmoothGroup)
            
            #merged sg
            if (CurrentSmoothGroup != 0) and (CurrentSmoothGroup not in all_smg):
                if NodeName not in merged_sg[0]:
                    merged_sg[0].append(NodeName)
                merged_sg[1].append(i)
            
            #ID count
            if CurrentID not in id_count:
                id_count.append(CurrentID)

            #very small area
            if CurrentPolArea < SmallArea:
                #add name
                if NodeName not in small_polygons[0]:
                    small_polygons[0].append(NodeName)
                #add face
                small_polygons[1].append(i)
                 
        #add No SG
        if len(without_sg[0]) > 0:
            obj_without_sg.append (without_sg)
            
        #add MERGED SG
        if len( merged_sg[0] ) > 0:            
            obj_with_merged_sg.append( merged_sg )

        #ADD too many SG
        if len(sg_count) >= 16:
            obj_with_many_sg.append(NodeName)
        
        #add normal
        if len(without_sg[0]) == 0 and len(merged_sg[0]) == 0 and len(sg_count) < 16:
            obj_without_problems.append(NodeName)

        #mat id
        if len(id_count) > 1:
            many_id.append(NodeName)
        else:
            normal_id.append(NodeName)

        #all objects with problems (obj name - polygon number)
        if len(small_polygons[0]) > 0:
            objects_poly_problems.append( small_polygons )

        #result generator
        if len(obj_with_merged_sg) > 0:
            result1 = "merged"
            if result1 not in sg_check_result:
                sg_check_result.append(result1)
        #no sg
        if len(obj_without_sg) > 0:
            result2 = "zero"
            if result2 not in sg_check_result:
                sg_check_result.append(result2)
        #to many
        if len(obj_with_many_sg) > 0:
            result3 = "many"
            if result3 not in sg_check_result:
                sg_check_result.append(result3)


    #print small
    if len(objects_poly_problems) > 0:
        print ('\n', "List of Objects with polygons without polygons with VERY Small Area:")
        for m in range(len(objects_poly_problems)):
            if len(objects_poly_problems[m][0][0].name) == 0:
                print ('\t', str(m+1) + ".", "noname object #" + str(i), "has", len(objects_poly_problems[m][1]), "very small polygon(s)."               )
            else:
                print ('\t', str(m+1) + ".", objects_poly_problems[m][0][0].name, "has", len(objects_poly_problems[m][1]), "very small polygon(s).")

    #print (Many Mat ID)
    if len(many_id) > 0:
        print ('\n', "List of Objects with many Materials ID's:")
        for m in range(len(many_id)):
            if len(many_id[m].name) == 0:
                print ('\t', str(m+1) + ".", "noname object #" + str(m))
            else:
                print ('\t', str(m+1) + ".", many_id[m].name)

    #print (merged)
    if len(obj_with_merged_sg) > 0:
        print ('\n', "List of Objects with polygons with merged Smoothing Groups:")
        for m in range(len(obj_with_merged_sg)):
            if len(obj_with_merged_sg[m][0][0].name) == 0:
                print ('\t', str(m+1) + ".", "noname object #" + str(m), "has", len(obj_with_merged_sg[m][1]), "polygon(s) with Merged SG."            )
            else:
                print ('\t', str(m+1) + ".", obj_with_merged_sg[m][0][0].name, "has", len(obj_with_merged_sg[m][1]), "polygon(s) with Merged SG.")

    #print (NO SG)
    if len(obj_without_sg) > 0:
        print ('\n', "List of Objects with polygons without Smoothing Groups:")
        for m in range(len(obj_without_sg)):
            if len(obj_without_sg[m][0][0].name) == 0:
                print ('\t', str(m+1) + ".", "noname object #" + str(m), "has", len(obj_without_sg[m][1]), "polygon(s) without SG.")
            else:
                print ('\t', str(m+1) + ".", obj_without_sg[m][0][0].name, "has", len(obj_without_sg[m][1]), "polygon(s) without SG.")

    #print (NO SG)
    if len(obj_with_many_sg) > 0:
        print ('\n', "List of Objects with too many Smoothing Groups:")
        for m in range(len(obj_with_many_sg)):
            if len(obj_with_many_sg[m].name) == 0:
                print ('\t', str(m+1) + ".", "noname object #" + str(m))
            else:
                print ('\t', str(m+1) + ".", obj_with_many_sg[m].name)

    if len(invisible_polygons) > 0:
        print ('\n', "Invisible polygon(s)#:")
        for m in range(len(invisible_polygons)):
            print (str(m+1) + ".", invisible_polygons[m])
        
        print ("They present in model but you can't see they! It's magic of 3ds max!")

    return obj_without_problems, obj_with_merged_sg, obj_without_sg, obj_with_many_sg, sg_count, sg_check_result, many_id, normal_id, objects_poly_problems, invisible_polygons

#uv stat
def uvUtilStat(sel_editable_poly_nodes):

    #selected nodes
    SelectedNodes = rt.selection

    #0 object from array
    ObjectName = sel_editable_poly_nodes[0].name

    if len(sel_editable_poly_nodes) == 1:
        #NodeName = rt.getNodeByName( ObjectName )
        rt.select(sel_editable_poly_nodes[0])
        
    Pixmap = QPixmap(QSize(100,100))
    colorWhite = QColor()
    colorBlack = QColor()
    ColorRed = QColor()

    colorWhite.setRgb(255,255,255,255)
    colorBlack.setRgb(0,0,0,255)
    ColorRed.setRgb(255,0,0,255)
    Pixmap.fill(colorBlack)    
        
    bmp_size = 100

    try:

        rt.execute("modPanel.addModToSelection (Unwrap_UVW ())")

        sel_editable_poly_nodes[0].modifiers[0].renderuv_width = bmp_size
        sel_editable_poly_nodes[0].modifiers[0].renderuv_height = bmp_size
        sel_editable_poly_nodes[0].modifiers[0].renderuv_fillmode = 1
        sel_editable_poly_nodes[0].modifiers[0].renderuv_showoverlap = False
        sel_editable_poly_nodes[0].modifiers[0].renderuv_seamColor = rt.color(255,255,255)
        sel_editable_poly_nodes[0].modifiers[0].renderuv_fillColor = rt.color(255,255,255)
        sel_editable_poly_nodes[0].modifiers[0].renderuv_showframebuffer = False

        #random for name
        RandInd = str(random.randrange(1000))

        TempGetDirPath = rt.execute ("GetDir #temp")

        #change symbols
        GetDirPath = TempGetDirPath.replace ("\\", "/")
        
        #name
        UVFileName = GetDirPath + "\\pt_uvrender_" + str(RandInd) + ".bmp"

        #render UV
        sel_editable_poly_nodes[0].modifiers[0].unwrap5.renderUV(UVFileName)
        sel_editable_poly_nodes[0].modifiers[0].renderuv_showframebuffer = True

        #convert to poly
        rt.execute ("macros.run \"Modifier Stack\" \"Convert_to_Poly\"")
        
        #load pic to pixmap
        Pixmap.load(UVFileName)
        img = Pixmap.toImage()

        BlackPixelCount = 0

        #pixel count
        for i in range(0,100):
            for j in range(0,100):
                Color = QColor()
                Color = QColor.fromRgb(img.pixel(i,j))
                if Color == Qt.black:
                    BlackPixelCount += 1
        
        #get percent                    
        Precentage = int(100 - BlackPixelCount / 100) #by 1 %               

        #del temp file
        rt.execute ("deleteFile " + "\"" + UVFileName + "\"") 
        
    except:        
        Precentage = 0
        Pixmap.fill(ColorRed)   
        #convert to poly
        rt.execute ("macros.run \"Modifier Stack\" \"Convert_to_Poly\"")

        print ('\n', "EXEPTION in uvUtilStat function. Problem with object or object hasn't name!")

    #return selection
    rt.select(SelectedNodes)

    return Precentage, Pixmap


def prepareMesh(sel_editable_poly_objects):

    prep_mesh_conclusion_data = []

    print ("-----------------------------------------")
    print ("PolygonTools: MESH PREPARE BATCH")
    print ("-----------------------------------------")

    # STEP 1
    try:
        #unhide layers
        for i in range(0, rt.LayerManager.count):
            rt.LayerManager.getLayer(i).on = True

        rt.execute ("max unhide all")
        prep_mesh_conclusion_data.append(True)
    except:
        prep_mesh_conclusion_data.append(False)

    # STEP 2
    try:
        rt.execute ("max unfreeze all")
        prep_mesh_conclusion_data.append(True)
    except:
        prep_mesh_conclusion_data.append(False)

    # STEP 3
    try:
        rt.execute ("macros.run \"Medit Tools\" \"clear_medit_slots\"")
        prep_mesh_conclusion_data.append(True)
    except:
        prep_mesh_conclusion_data.append(False)

        
    # STEP 4
    try:
        for i in range(len(sel_editable_poly_objects)):
            rt.execute ("$" + sel_editable_poly_objects[i] + ".EditablePoly.unhideAll #Face")
        prep_mesh_conclusion_data.append(True)
    except:
        print ("Faces Unhiden not supported for current type of the object! Object Name:", sel_editable_poly_objects[i])
        prep_mesh_conclusion_data.append(False)
    
    # STEP 5
    try:
        for i in range(len(sel_editable_poly_objects)):
            rt.execute ("$" + sel_editable_poly_objects[i] + ".EditablePoly.unhideAll #Vertex")
        prep_mesh_conclusion_data.append(True)
    except:
        print ("Vertices Unhiden not supported for current type of the object! Object Name:", sel_editable_poly_objects[i])
        prep_mesh_conclusion_data.append(False)

    # STEP 6
    try:
        for i in range(len(sel_editable_poly_objects)):
            rt.execute ("resetxform $" + sel_editable_poly_objects[i])
        prep_mesh_conclusion_data.append(True)
    except:
        prep_mesh_conclusion_data.append(False)

    # STEP 7
    try:
        for i in range(len(sel_editable_poly_objects)):
            rt.execute ("convertto $" + sel_editable_poly_objects[i] + " editable_poly")
        prep_mesh_conclusion_data.append(True)
    except:
        prep_mesh_conclusion_data.append(False)

    # STEP 8
    try:
        for i in range(len(sel_editable_poly_objects)):
            rt.execute ("$" + sel_editable_poly_objects[i] + ".backfacecull = true")
        prep_mesh_conclusion_data.append(True)
    except:
        prep_mesh_conclusion_data.append(False)
            
    fixed_material_obj = []
    assigned_material_obj = []

    # STEP 9
    try:
        for i in range(len(sel_editable_poly_objects)):
            
            #GET MAT BY OBJECT
            ObjectName = sel_editable_poly_objects[i]                
            NodeName = rt.getNodeByName(ObjectName)
            CurrentMat = NodeName.material        

            #try to get mat
            try:

                #get mat class
                MaterialClass = str(rt.classOf(CurrentMat))
                
                #get mat name
                MaterialName =  str(NodeName.material.name)

            except:

                #no mat assigned
                MaterialClass = "None"
                MaterialName = "None"

            if MaterialClass == "None" and MaterialName == "None":
                rt.execute ("$" + sel_editable_poly_objects[i] + ".material = Standard()")
                rt.execute ("$" + sel_editable_poly_objects[i] + ".material.name = $" + sel_editable_poly_objects[i] + ".name + \"_mat\"")
                assigned_material_obj.append(sel_editable_poly_objects[i] )
        
            #fix default names
            if ("- Default" in MaterialName) or ("Material #" in MaterialName) or (len(MaterialName) == 0):                     
                rt.execute ("$" + sel_editable_poly_objects[i] + ".material.name = $" + sel_editable_poly_objects[i] + ".name + \"_mat\"")
                fixed_material_obj.append(sel_editable_poly_objects[i] )

            if MaterialClass == "Multimaterial":
                
                MaterialsList = NodeName.material.materialList
                
                for k in range(len(MaterialsList)):
                    
                    #get sub mat
                    SubMaterial = MaterialsList[k]
                    
                    if SubMaterial != None:

                        SubMatClass = rt.classOf(MaterialsList[k])
                        SubMatName = str(SubMaterial.name)

                        if ("- Default" in SubMatName) or ("Material #" in SubMatName) or (len(SubMatName) == 0):

                            NewMatName = sel_editable_poly_objects[i] + "_ID" + str(k+1)
                            SubMaterial.name = NewMatName
                            
                            #add only unique
                            if sel_editable_poly_objects[i] not in fixed_material_obj:
                                fixed_material_obj.append( sel_editable_poly_objects[i] )
                            
        prep_mesh_conclusion_data.append(True)                        
    except:
        prep_mesh_conclusion_data.append(False)


    #for uniqe mat and objects
    unique_materials = []
    unique_material_obj = []

    #get Unique
    try:
        for i in range(len(sel_editable_poly_objects)):
            
            ObjectName = sel_editable_poly_objects[i]  
            NodeName = rt.getNodeByName( ObjectName )
            MaterialName =  NodeName.material.name

            if MaterialName not in unique_materials:                
                unique_materials.append(MaterialName)
                unique_material_obj.append(NodeName)
    except:
        print ("PolygonTools: Can't collect unique Materials. Error 1 in 'prepareMesh' function.")

    #add to Slots
    try:
        for i in range(len(unique_material_obj)):            
            rt.meditMaterials[i] = unique_material_obj[i].material
    except:
        print ("PolygonTools: Can't update Material slots! Error 2 in 'prepareMesh' function.")

    #end

    #STEP 10
    for i in range(len(sel_editable_poly_objects)):
        rt.execute ("$" + sel_editable_poly_objects[i] + ".showVertexColors = off")

    try:
        rt.execute ("redrawViews()")
        prep_mesh_conclusion_data.append(True)
    except:
        prep_mesh_conclusion_data.append(False)
    
    #0
    if prep_mesh_conclusion_data[0] == True:
        print ("1. All objects and Layers are Unhidden............OK")
    #1
    if prep_mesh_conclusion_data[1] == True:
        print ("2. All objects are Unfrozen.......................OK")
    #2
    if prep_mesh_conclusion_data[2] == True:
        print ("3. Material Slot Reseted..........................OK"        )
    #3    
    if prep_mesh_conclusion_data[3] == True:
        print ("4. All Faces are Unhidden.........................OK")
    #4    
    if prep_mesh_conclusion_data[4] == True:
        print ("5. All Vertices are Unhidden......................OK")
    #5    
    if prep_mesh_conclusion_data[5] == True:
        print ("6. Reset XForm applied to all objects.............OK")
    #6    
    if prep_mesh_conclusion_data[6] == True:
        print ("7. All objects are converted to Editable Poly.....OK")
    #7    
    if prep_mesh_conclusion_data[7] == True:
        print ("8. Backface Cull in ON for all objects............OK")
    #8    
    if prep_mesh_conclusion_data[8] == True:
        print ("9. Materials was processed........................OK")
        
        if len(assigned_material_obj) > 0:
            print ('\n', "Material assigned to:")
            for i in range(len(assigned_material_obj)):
                print ((str(i+1) + "."), assigned_material_obj[i])

        if len(fixed_material_obj) > 0:
            print ('\n', "Material Name fixed for:")
            for i in range(len(fixed_material_obj)):
                print ((str(i+1) + "."), fixed_material_obj[i])

    print ('\t', "Unique Materials in Selection:", len(unique_materials))

    #9
    if prep_mesh_conclusion_data[9] == True:
        print ("10. PolygonTools: Viewport Redraw.................OK")

    print ("")

    return prep_mesh_conclusion_data


def prepareScene():

    prep_scene_conclusion_data = []                

    print ("-----------------------------------------")
    print ("PolygonTools: SCENE PREPARE BATCH")
    print ("-----------------------------------------")

    #0
    try:
        #unhide layers
        for i in range(0, rt.LayerManager.count):
            rt.LayerManager.getLayer(i).on = True

        rt.execute ("max unhide all")
        print ("1. All objects and layers are Unhidden............OK")
        prep_scene_conclusion_data.append(True)
    except:
        prep_scene_conclusion_data.append(False)
    
    #1
    try:
        rt.execute ("max unfreeze all")
        print ("2. All objects are Unfrozen.......................OK")
        prep_scene_conclusion_data.append(True)
    except:
        prep_scene_conclusion_data.append(False)
    
    #2
    try:
        rt.execute ("redrawViews()")
        print ("3. Viewport Redraw................................OK")
        prep_scene_conclusion_data.append(True)
    except:
        prep_scene_conclusion_data.append(False)    
    
    #3
    try:
        rt.execute ("macros.run \"Medit Tools\" \"clear_medit_slots\"")
        print ("4. Materials was processed........................OK")
        prep_scene_conclusion_data.append(True)
    except:
        prep_scene_conclusion_data.append(False)

    #Editable_Poly objects in scene
    scene_objects = []

    #get all scene ojects
    SceneObjects = rt.objects

    #get all Editable_Poly
    for i in range(len(SceneObjects)):
        ObjectClass = str(rt.classOf(SceneObjects[i]))
	    
        if ObjectClass == "Editable_Poly":
            scene_objects.append(SceneObjects[i])

    #for uniqe mat and objects
    unique_materials = []
    unique_material_obj = []
    
    try:
        for i in range(len(scene_objects)):
            
            #try to get mat
            try:
                CurrentMaterial = str(scene_objects[i].material)
                MaterialName = scene_objects[i].material.name
            except:
                #no mat assigned
                CurrentMat = "None"
                MaterialName = "None"

            if MaterialName == "None" or CurrentMaterial == "None":            
                scene_objects[i].material = rt.Standard()
                scene_objects[i].material.name = scene_objects[i].name + "_mat"
                print ("Material was Assigned to object:", scene_objects[i].name)

            if scene_objects[i].material.name not in unique_materials:                
                unique_materials.append(scene_objects[i].material.name)
                unique_material_obj.append(scene_objects[i])
    except:
        print ("PolygonTools: Can't collect unique Materials. Error 1 in 'prepareScene' function")

    try:
        for i in range(len(unique_material_obj)):
            MaterialName = str(unique_material_obj[i].material)        
            rt.meditMaterials[i] = unique_material_obj[i].material
    except:
        print ("PolygonTools: Can't update Material slots! Error 2 in 'prepareScene' function")

    
    CustomSysUnits = cfgl.configLoader()[9]
    CurrentWorkUnits = str(rt.units.Systemtype)

    #4
    if CustomSysUnits != CurrentWorkUnits:        
        rt.execute ("units.Systemtype = #" + CustomSysUnits)
        print ("ATTENTION!: System units were changed to - ", CurrentWorkUnits)
        prep_scene_conclusion_data.append(False)
    else:
        prep_scene_conclusion_data.append(True)           
        print ("6. System units - ", CurrentWorkUnits)
        
    return prep_scene_conclusion_data

#check scene name
def sceneName():

    scene_name_conclusion_data = False   

    Message = ""

    #get path and name
    PathToCurrentFile = rt.maxFilePath
    MaxFileName = rt.maxFileName
    #MaxFileName = rt.getFilenameFile(rt.maxFileName)

    #abs path
    AbsolutePathToScene = PathToCurrentFile + MaxFileName

    #path yes or not
    if PathToCurrentFile == "":
        Message = "Please save current scene!"
        LabelColor = "background-color:#916666;"
        scene_name_conclusion_data = False
    else:
        Message = "Current file name is: " + AbsolutePathToScene
        LabelColor = "background-color:#3D523D;"
        scene_name_conclusion_data = True

    return AbsolutePathToScene, Message, LabelColor, scene_name_conclusion_data

#viewport operations
def prepareViewport():

    prep_viewport_conclusion_data = []

    print ("-----------------------------------------")
    print ("PolygonTools: VIEW PREPARE BATCH")
    print ("-----------------------------------------")

    #0
    try:
        rt.clearSelection()
        prep_viewport_conclusion_data.append(True)
    except:
        prep_viewport_conclusion_data.append(False)

    #1
    try:
        rt.execute ("IDisplayGamma.colorCorrectionMode = #none")
        print ("1. Gamma and LUT is off...................OK")
        prep_viewport_conclusion_data.append(True)
    except:
        prep_viewport_conclusion_data.append(False)

    #2
    try:
        rt.execute ("viewport.setLayout #layout_4")
        rt.execute ("viewport.ResetAllViews()")
        print ("2. Standart Layout........................OK")
        prep_viewport_conclusion_data.append(True)
    except:
        prep_viewport_conclusion_data.append(False)

    #3
    try:
        rt.execute ("max vpt persp user")
        print ("3. Set Perspective........................OK")
        prep_viewport_conclusion_data.append(True)
    except:
        prep_viewport_conclusion_data.append(False)

    #4
    try:
        rt.execute("max zoomext sel all")
        print ("4. Zoom to Objects........................OK")
        prep_viewport_conclusion_data.append(True)
    except:
        prep_viewport_conclusion_data.append(False)

    #5        
    try:
        rt.execute ("viewport.setFOV 45.0")
        print ("5. FOV 45 for camera......................OK")
        prep_viewport_conclusion_data.append(True)
    except:
        prep_viewport_conclusion_data.append(False)

    #6
    try:
        rt.execute ("redrawViews()")
        print ("6. Viewport Redraw........................OK")
        prep_viewport_conclusion_data.append(True)
    except:
        prep_viewport_conclusion_data.append(False)
    #7
    try:
        rt.execute ("actionMan.executeAction 0 \"550\"")
        print ("7. Shaded Mode is ON......................OK")
        prep_viewport_conclusion_data.append(True)
    except:
        prep_viewport_conclusion_data.append(False)
    
    #8
    try:
        rt.execute ("viewport.setGridVisibility 4 false")
        print ("8. Grid is OFF............................OK")
        prep_viewport_conclusion_data.append(True)
    except:
        prep_viewport_conclusion_data.append(False)

    return prep_viewport_conclusion_data


def materialFixer(sel_editable_poly_nodes, Action):

    fixed_material_obj = []
    assigned_material_obj = []

    for i in range(len(sel_editable_poly_nodes)):
        
        #GET MAT BY OBJECT
        NodeName = sel_editable_poly_nodes[i]
        CurrentMat = NodeName.material        

        #try to get mat
        try:

            #get mat class
            MaterialClass = str(rt.classOf(CurrentMat))
            
            #get mat name
            MaterialName =  str(NodeName.material.name)

        except:

            #no mat assigned
            MaterialClass = "None"
            MaterialName = "None"

        if MaterialClass == "None" and MaterialName == "None":
            rt.execute ("$" + NodeName.name + ".material = Standard()")
            rt.execute ("$" + NodeName.name  + ".material.name = $" + NodeName.name + ".name + \"_mat\"")
            assigned_material_obj.append( NodeName )

        #fix default names
        if ("- Default" in MaterialName) or ("Material #" in MaterialName) or (len(MaterialName) == 0):                     
            rt.execute ("$" + NodeName.name + ".material.name = $" + NodeName.name + ".name + \"_mat\"")
            fixed_material_obj.append( NodeName )

        if MaterialClass == "Multimaterial" and Action == "Check":
            
            MaterialsList = NodeName.material.materialList
            
            for k in range(len(MaterialsList)):
                
                #get sub mat
                SubMaterial = MaterialsList[k]
                
                if SubMaterial != None:

                    SubMatClass = rt.classOf(MaterialsList[k])
                    SubMatName = str(SubMaterial.name)

                    if ("- Default" in SubMatName) or ("Material #" in SubMatName) or (len(SubMatName) == 0):

                        NewMatName = NodeName.name + "_ID" + str(k+1)
                        SubMaterial.name = NewMatName
                        
                        #add only unique
                        if NodeName not in fixed_material_obj:
                            fixed_material_obj.append( NodeName )
        
        elif MaterialClass == "Multimaterial" and Action == "Fix":
            rt.execute ("$" + NodeName.name + ".material = Standard()")
            rt.execute ("$" + NodeName.name  + ".material.name = $" + NodeName.name + ".name + \"_mat\"")
            assigned_material_obj.append( NodeName )
    
    return  fixed_material_obj, assigned_material_obj


def localTexturePathFix():

    try:
        bitmap_textures = rt.getClassInstances(rt.BitmapTexture)

        for i in bitmap_textures:
            if len(i.fileName) == 0:
                i.fileName = str(i) + " (Zero-map)"
                print ("Zero-length Map Name has been fixed!")
            else:
                FileName = rt.filenameFromPath(i.fileName)
            
            if  len(FileName) == 0:
                FileName = str(i) + " (Zero-map)"
            
            if i.Filename != FileName and len(i.fileName) != 0:
                i.Filename = FileName
        
        print ("Path to Texture was Stripped......................OK"     )

    except:
        
        print ("EXCEPTION in 'localTexturePathFix' function!")


    
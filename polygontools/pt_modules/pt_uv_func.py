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

class PT_UV_Tab (QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)

        #Create Widgets
        self.tabUv_v_layout = QVBoxLayout(self)
        self.tabUv_v_layout.setAlignment(Qt.AlignTop)
        
        #icons
        CurrentDir = os.path.dirname(__file__)
        IconPath = (CurrentDir + "\icons")

        try:
            iconScaleUV2  = QPixmap(IconPath + "/scale_uv2_icon.png")
            iconScaleUV05  = QPixmap(IconPath + "/scale_uv05_icon.png")
            iconMoveVUp  = QPixmap(IconPath + "/move_v_up_icon.png")
            iconMoveVDown  = QPixmap(IconPath +"/move_v_down_icon.png")
            iconMoveURight  = QPixmap(IconPath + "/move_u_right_icon.png")
            iconMoveULeft  = QPixmap(IconPath + "/move_u_left_icon.png")
            iconShowUV  = QPixmap(IconPath +"/show_uv_icon.png")
            iconRemoveChecker  = QPixmap(IconPath + "/remove_checker_icon.png")
        except:
            cmds.warning( "PolygonTools: Can't load icons for UV Tab! Check icon files in pt_modules/icons directory.")

        MaxWidth = 370
                
        #label for info
        self.lblInfo_01 = QLabel()
        self.lblInfo_01.setMargin(2)
        
        #group for Checkers
        self.gboxCheckers = QGroupBox("Checker Textures")
        self.gboxCheckers.setMaximumWidth(MaxWidth)
        self.gboxCheckers_v_layout = QVBoxLayout()
                
        #Red checker
        self.btnCheStd = QPushButton()
        self.btnCheStd.setMaximumWidth(68)
        self.btnCheStd.setMaximumHeight(68)
        
        #Digit checker
        self.btnCheDig = QPushButton()
        self.btnCheDig.setMaximumWidth(68)
        self.btnCheDig.setMaximumHeight(68)
        
        #Diagonal checker
        self.btnCheDiag = QPushButton()
        self.btnCheDiag.setMaximumWidth(68)
        self.btnCheDiag.setMaximumHeight(68)
        
        #Gradient checker
        self.btnCheGrad = QPushButton()
        self.btnCheGrad.setMaximumWidth(68)
        self.btnCheGrad.setMaximumHeight(68)        
        
        currentDir = os.path.dirname(__file__)
        
        #Red checker icon
        self.iconCheRed = QIcon() 
        checker_standard_path = IconPath + "/checker_standard_icon.png"
        checkCheckerTextureFile(checker_standard_path)        
        self.iconCheRed.addPixmap(QPixmap(checker_standard_path), QIcon.Normal, QIcon.Off)
        self.btnCheStd.setIcon(self.iconCheRed)
        self.btnCheStd.setIconSize(QSize(64, 64))
        
        #Digit checker  icon
        self.iconCheDig = QIcon() 
        checker_digital_path = IconPath + "/checker_digital_icon.png"
        checkCheckerTextureFile(checker_digital_path)
        self.iconCheDig.addPixmap(QPixmap(checker_digital_path), QIcon.Normal, QIcon.Off)
        self.btnCheDig.setIcon(self.iconCheDig)
        self.btnCheDig.setIconSize(QSize(64, 64))

        #Diagoanl checker  icon
        self.iconCheDiag = QIcon() 
        checker_diagonal_path = IconPath + "/checker_diagonal_icon.png"
        checkCheckerTextureFile(checker_diagonal_path)
        self.iconCheDiag.addPixmap(QPixmap(checker_diagonal_path), QIcon.Normal, QIcon.Off)
        self.btnCheDiag.setIcon(self.iconCheDiag)
        self.btnCheDiag.setIconSize(QSize(64, 64))

        #Gradient checker  icon
        self.iconCheGrad = QIcon()
        checker_gradient_path = IconPath + "/checker_gradient_icon.png"
        checkCheckerTextureFile(checker_gradient_path)
        self.iconCheGrad.addPixmap(QPixmap(checker_gradient_path), QIcon.Normal, QIcon.Off)
        self.btnCheGrad.setIcon(self.iconCheGrad)
        self.btnCheGrad.setIconSize(QSize(64, 64))
        
        self.gboxCheckRes = QGroupBox("Checker Texture Size Emulation (px)")
        self.gboxCheckRes.setMaximumWidth(MaxWidth)
        self.gboxCheckRes.setMaximumHeight(50)
        self.gboxCheckRes.setEnabled(False)
        self.gboxCheckRes_h_layout = QHBoxLayout()
        
        self.rbtn256 = QRadioButton()
        self.rbtn256.setText("256")
        self.rbtn512 = QRadioButton()
        self.rbtn512.setText("512")
        self.rbtn1024 = QRadioButton()
        self.rbtn1024.setText("1K")
        self.rbtn2048 = QRadioButton()
        self.rbtn2048.setText("2K")
        self.rbtn4096 = QRadioButton()
        self.rbtn4096.setText("4K")
        self.rbtn8192 = QRadioButton()
        self.rbtn8192.setText("8K")
        
        #UV Utils
        self.gboxUVUtils = QGroupBox("UV Utilities")
        self.gboxUVUtils.setMaximumWidth(MaxWidth)
        self.gboxUVUtils.setMaximumHeight(350)
        self.gboxUVUtils.setEnabled(True)
        self.gboxUVUtil_h_layout = QHBoxLayout()
        
        self.gboxUVUtil_v_layout1 = QVBoxLayout()
        self.gboxUVUtil_v_layout1.setAlignment(Qt.AlignTop)
        
        self.gboxUVUtil_v_layout2 = QVBoxLayout()
        self.gboxUVUtil_v_layout2.setAlignment(Qt.AlignTop)
        
        self.gboxUVUtil_v_layout3 = QVBoxLayout()
        self.gboxUVUtil_v_layout3.setAlignment(Qt.AlignTop)
        
        self.btnScale2 = QPushButton("x2")
        self.btnScale2.setIcon(iconScaleUV2)
        self.btnScale2.setToolTip("Increase UV layout by 2 times")
        self.btnScale2.setStyleSheet("color:#000000;background-color:#E1E1E1;")
        
        self.btnScale05 = QPushButton("x0.5")
        self.btnScale05.setToolTip("Decrease UV layout by 2 times")
        self.btnScale05.setIcon(iconScaleUV05)
        self.btnScale05.setStyleSheet("color:#000000;background-color:#E1E1E1;")
        
        self.btnMoveUVLeft = QPushButton("-1U")
        self.btnMoveUVLeft.setToolTip("Move UV layout left")
        self.btnMoveUVLeft.setIcon(iconMoveULeft)
        self.btnMoveUVLeft.setStyleSheet("color:#000000;background-color:#E1E1E1;")
        
        self.btnMoveUVRight = QPushButton("+1U")
        self.btnMoveUVRight.setToolTip("Move UV layout right")
        self.btnMoveUVRight.setIcon(iconMoveURight)
        self.btnMoveUVRight.setStyleSheet("color:#000000;background-color:#E1E1E1;")
        
        self.btnMoveUVUp = QPushButton("+1V")
        self.btnMoveUVUp.setToolTip("Move UV layout up")
        self.btnMoveUVUp.setIcon(iconMoveVUp)
        self.btnMoveUVUp.setStyleSheet("color:#000000;background-color:#E1E1E1;")
        
        self.btnMoveUVDown = QPushButton("-1V")
        self.btnMoveUVDown.setToolTip("Move UV layout down")
        self.btnMoveUVDown.setIcon(iconMoveVDown)
        self.btnMoveUVDown.setStyleSheet("color:#000000;background-color:#E1E1E1;")
        
        self.btnViewUV = QToolButton()
        self.btnViewUV.setText("Show UV")
        self.btnViewUV.setIcon(iconShowUV)
        self.btnViewUV.setToolTip("Show UV layout on object as texture")
        self.btnViewUV.setMaximumWidth(125) 
        self.btnViewUV.setCheckable(True)
        
        self.lblUvScale = QLabel("Scale UV")
        self.lblMoveUV = QLabel("Move UV")
        self.lblShowUV = QLabel("Additional")
        
        #layouting
        self.gboxCheckRes_h_layout.addWidget(self.rbtn256)
        self.gboxCheckRes_h_layout.addWidget(self.rbtn512)
        self.gboxCheckRes_h_layout.addWidget(self.rbtn1024)
        self.gboxCheckRes_h_layout.addWidget(self.rbtn2048)
        self.gboxCheckRes_h_layout.addWidget(self.rbtn4096)
        self.gboxCheckRes_h_layout.addWidget(self.rbtn8192)
        
        
        self.gboxUVUtil_v_layout1.addWidget(self.lblUvScale)
        self.gboxUVUtil_v_layout1.addWidget(self.btnScale2)
        self.gboxUVUtil_v_layout1.addWidget(self.btnScale05)
        
        self.gboxUVUtil_v_layout2.addWidget(self.lblMoveUV)
        self.gboxUVUtil_v_layout2.addWidget(self.btnMoveUVLeft)
        self.gboxUVUtil_v_layout2.addWidget(self.btnMoveUVRight)
        self.gboxUVUtil_v_layout2.addWidget(self.btnMoveUVUp)
        self.gboxUVUtil_v_layout2.addWidget(self.btnMoveUVDown)
        
        self.gboxUVUtil_v_layout3.addWidget(self.lblShowUV)
        self.gboxUVUtil_v_layout3.addWidget(self.btnViewUV)
        
        self.gboxUVUtil_h_layout.addLayout(self.gboxUVUtil_v_layout1)
        self.gboxUVUtil_h_layout.addLayout(self.gboxUVUtil_v_layout2)
        self.gboxUVUtil_h_layout.addLayout(self.gboxUVUtil_v_layout3)
        
        self.gboxCheckRes.setLayout(self.gboxCheckRes_h_layout)
        self.gboxUVUtils.setLayout(self.gboxUVUtil_h_layout)

        self.btnRemCheck = QPushButton("Remove Checker")
        self.btnRemCheck.setStyleSheet("color:#000000;background-color:#E1E1E1;")
        self.btnRemCheck.setMaximumWidth(140)
        self.btnRemCheck.setMinimumWidth(140)
        self.btnRemCheck.setIcon(iconRemoveChecker)
        self.btnRemCheck.setEnabled(False)
        
        self.gboxUVConclusion = QGroupBox("Conclusion")
        self.gboxUVConclusion.setStyleSheet("color:#ffffff; background-color:#2b2b2b;")
        self.gboxUVConclusion.setMaximumWidth(MaxWidth)
        self.gboxUVConclusion.setMinimumHeight(170)
        self.gboxUVConclusion_v_layout = QVBoxLayout()        

        #conclusion text here
        self.txtbrowUVConclusion = QTextBrowser()
        self.txtbrowUVConclusion.setHtml("") 
        
            
        #Add Widgets        
        self.gboxUVConclusion_v_layout.addWidget(self.txtbrowUVConclusion) 
        
        self.tabUv_v_layout.addWidget(self.lblInfo_01)
        
        #add gbox
        self.tabUv_v_layout.addWidget(self.gboxCheckers)
        
        self.gboxCheckers.setLayout(self.gboxCheckers_v_layout)
        
        self.tabUv_h_layout_01 = QHBoxLayout()
        self.tabUv_h_layout_01.setAlignment(Qt.AlignLeft)
        self.gboxCheckers_v_layout.addLayout(self.tabUv_h_layout_01)
        
        #add buttons
        self.tabUv_h_layout_01.addWidget(self.btnCheStd)
        self.tabUv_h_layout_01.addWidget(self.btnCheDig)
        self.tabUv_h_layout_01.addWidget(self.btnCheDiag)
        self.tabUv_h_layout_01.addWidget(self.btnCheGrad)
        
        #remove checker button
        self.gboxCheckers_v_layout.addWidget(self.btnRemCheck)
        
        self.tabUv_v_layout.addWidget(self.gboxCheckRes)
        
        self.tabUv_v_layout.addWidget(self.gboxUVUtils)
        
        #conclusion
        self.gboxUVConclusion.setLayout(self.gboxUVConclusion_v_layout)
        
        #conclusion area
        self.tabUv_v_layout.addWidget(self.gboxUVConclusion)

        #SIGNALS
        self.btnRemCheck.clicked.connect(self.btnRemCheckClicked)
        
        #checker buttons click
        self.btnCheStd.clicked.connect(self.btnCheStdClicked)
        self.btnCheDig.clicked.connect(self.btnCheDigClicked)
        self.btnCheDiag.clicked.connect(self.btnCheDiagClicked)
        self.btnCheGrad.clicked.connect(self.btnCheGradClicked)       
        
        self.rbtn256.toggled.connect(self.setTile256Toggled)         
        self.rbtn512.toggled.connect(self.setTile512Toggled)
        self.rbtn1024.toggled.connect(self.setTile1024Toggled)
        self.rbtn2048.toggled.connect(self.setTile2048Toggled)
        self.rbtn4096.toggled.connect(self.setTile4096Toggled)
        self.rbtn8192.toggled.connect(self.setTile8192Toggled)
        
        self.btnScale2.clicked.connect(self.btnScale2Clicked)
        self.btnScale05.clicked.connect(self.btnScale05Clicked)
        
        self.btnMoveUVLeft.clicked.connect(self.btnMoveUVLeftClicked)
        self.btnMoveUVRight.clicked.connect(self.btnMoveUVRightClicked)
        self.btnMoveUVUp.clicked.connect(self.btnMoveUVUpClicked)
        self.btnMoveUVDown.clicked.connect(self.btnMoveUVDownClicked)
        
        self.btnViewUV.pressed.connect(self.btnViewUVPressed)
        
        self.previous_materials_data = []

        #intro text
        current_languge = cfgl.configLoader()[14]
        self.txtbrowUVConclusion.setHtml( conclusion.uvTabIntroConclusion(current_languge) )      

        check_material_data = []
        check_material_data = checkShaderIntegrity()

        
        #0-scene_materials, PTCheckerInScene, Tiling, checkers_in_scene, GradientOnly, 5- std_checker_data, digital_checker_data, diagonal_checker_data, 8-gradient_checker_data, uvmat
        #print ("start", check_material_data[2])
        if check_material_data[1] == True and check_material_data[4] == False:
            self.toggleTile(check_material_data[2])
            self.btnRemCheck.setEnabled(True)
            self.gboxCheckRes.setEnabled(True)
            self.lblInfo_01.setText("Select an Object and Click on the necessary Checker or Utility.")
            self.lblInfo_01.setStyleSheet("")
        else:
            self.rbtn256.setChecked(True)
            self.btnRemCheck.setEnabled(True)
            self.gboxCheckRes.setEnabled(False)
            self.lblInfo_01.setText("Select an Object and Click on the necessary Checker or Utility.")
            self.lblInfo_01.setStyleSheet("")

        if check_material_data[1] == False:
            self.btnRemCheck.setEnabled(False)

        if check_material_data[9] == True: 
            self.btnViewUV.setText("Show UV")
            self.btnViewUV.setChecked(True)           


    def showInfo(self, info_type, info_text):

        #trim lables
        if len(info_text) > 67:
            short_info_text = info_text[:67] + "..."
        else:
            short_info_text = info_text
        
        if info_type == "info":
            self.lblInfo_01.setText(short_info_text)
            self.lblInfo_01.setStyleSheet("background-color:#3D523D;")
            print ("\nPolygonTools:", info_text, '\n')
        
        if info_type == "warn":
            self.lblInfo_01.setText(short_info_text)
            self.lblInfo_01.setStyleSheet("background-color:#916666;")
            print ("\nPolygonTools:", info_text, '\n')
        
            
    #check depends on tile
    def toggleTile (self, Repeat):

        #if tile was changed to incorrect
        good_tile_aray = [2, 4, 8, 16, 32, 64]

        if Repeat == 2:
            self.rbtn256.setChecked(True)

        if Repeat == 4:
            self.rbtn512.setChecked(True)

        if Repeat == 8:
            self.rbtn1024.setChecked(True)

        if Repeat == 16:
            self.rbtn2048.setChecked(True)

        if Repeat == 32:
            self.rbtn4096.setChecked(True)

        if Repeat == 64:
            self.rbtn8192.setChecked(True)
        
        #set to 256 if problems
        if Repeat not in good_tile_aray:
            self.rbtn256.setChecked(True)
            print ("PolygonTools: Tile was Fixed to 256x256")

    #Aassign std checker    
    def btnCheStdClicked (self):

        current_languge = cfgl.configLoader()[14]
        
        #getselection
        try:
            selection_array = gen_func.checkSelection()

            sel_objects = selection_array[0]
            sel_editable_poly_objects = selection_array[1]
            sel_editable_poly_nodes = selection_array[3]
        except:
            print ("Please select something. Editable Poly object for example...")


        if len(sel_editable_poly_objects) > 0:

            checker_material_data = []
            #0-scene_materials, PTCheckerInScene, Tiling, checkers_in_scene, GradientOnly, 5- std_checker_data, digital_checker_data, diagonal_checker_data, 8-gradient_checker_data
            
            checker_material_data = checkShaderIntegrity()

            #previous mats
            self.previous_materials_data = getMaterials(sel_editable_poly_nodes)

            #if checker in scene
            if (checker_material_data[5][0] != "None"):
                ChangeResult = changeCheckerTexture ("checker_standard", sel_editable_poly_objects, checker_material_data[5])
            else:
                createCheckerMaterial("01")
                checker_material_data = checkShaderIntegrity()
                ChangeResult = changeCheckerTexture ("checker_standard", sel_editable_poly_objects, checker_material_data[5])
                

            if ChangeResult == True:
                self.checkCheckerTextureRepeat()

                conclusion_text = conclusion.uvOperationConclusion (current_languge, "assign_std_checker")
                self.txtbrowUVConclusion.setHtml(conclusion_text)

                self.showInfo("info", "Standard checker was assigned!")
                rt.execute ("actionMan.executeAction 0 \"63545\"")

            else:
                self.showInfo("warn", "Checker texture not found. Check files or try to re-install PolygonTools.")
        else:
            conclusion_text = conclusion.noSelection(current_languge, "assign_std_checker")
            self.txtbrowUVConclusion.setHtml(conclusion_text) 

            self.showInfo("warn", "Cant assign checker. Please select Editable Poly object(s).")

    #Aassign digital checker    
    def btnCheDigClicked (self):

        current_languge = cfgl.configLoader()[14]
        
        #getselection
        try:
            selection_array = gen_func.checkSelection()

            sel_objects = selection_array[0]
            sel_editable_poly_objects = selection_array[1]
            sel_editable_poly_nodes = selection_array[3]
        except:
            print ("Please select something. Editable Poly object for example...")

        if len(sel_editable_poly_objects) > 0:

            checker_material_data = []
            #0-scene_materials, PTCheckerInScene, Tiling, checkers_in_scene, GradientOnly, std_checker_data, digital_checker_data, diagonal_checker_data, 8-gradient_checker_data
            checker_material_data = checkShaderIntegrity()

            #previous mats
            self.previous_materials_data = getMaterials(sel_editable_poly_nodes)

            #if checker in scene
            if (checker_material_data[6][0] != "None"):
                ChangeResult = changeCheckerTexture ("checker_digital", sel_editable_poly_objects, checker_material_data[6])
            else:
                createCheckerMaterial("02")
                checker_material_data = checkShaderIntegrity()
                ChangeResult = changeCheckerTexture ("checker_digital", sel_editable_poly_objects, checker_material_data[6])

            if ChangeResult == True:
                self.checkCheckerTextureRepeat()                

                conclusion_text = conclusion.uvOperationConclusion (current_languge, "assign_dig_checker")
                self.txtbrowUVConclusion.setHtml(conclusion_text)

                self.showInfo("info", "Checker with digits was assigned!")
                rt.execute ("actionMan.executeAction 0 \"63545\"")
                
            else:
                self.showInfo("warn", "Checker texture not found. Check files or try to re-install PolygonTools.")

        else:
            conclusion_text = conclusion.noSelection(current_languge, "assign_dig_checker")
            self.txtbrowUVConclusion.setHtml(conclusion_text) 

            self.showInfo("warn", "Cant assign checker. Please select Editable Poly object(s).")


    #Aassign diagonal checker    
    def btnCheDiagClicked (self):
        
        

        current_languge = cfgl.configLoader()[14]
                
        #getselection
        try:
            selection_array = gen_func.checkSelection()

            sel_objects = selection_array[0]
            sel_editable_poly_objects = selection_array[1]
            sel_editable_poly_nodes = selection_array[3]
        except:
            print ("Please select something. Editable Poly object for example...")

        if len(sel_editable_poly_objects) > 0:

            checker_material_data = []
            #0-scene_materials, PTCheckerInScene, Tiling, checkers_in_scene, GradientOnly, std_checker_data, digital_checker_data, diagonal_checker_data, 8-gradient_checker_data
            checker_material_data = checkShaderIntegrity()

            #previous mats
            self.previous_materials_data = getMaterials(sel_editable_poly_nodes)

            #if checker in scene
            if (checker_material_data[7][0] != "None"):
                ChangeResult = changeCheckerTexture ("checker_diagonal", sel_editable_poly_objects, checker_material_data[7])
            else:
                createCheckerMaterial("03")
                checker_material_data = checkShaderIntegrity()
                ChangeResult = changeCheckerTexture ("checker_diagonal", sel_editable_poly_objects, checker_material_data[7])
            
            if ChangeResult == True:
                self.checkCheckerTextureRepeat()

                conclusion_text = conclusion.uvOperationConclusion (current_languge, "assign_diag_checker")
                self.txtbrowUVConclusion.setHtml(conclusion_text)

                self.showInfo("info", "Diagonal checker was assigned!")
                rt.execute ("actionMan.executeAction 0 \"63545\"")
            else:
                self.showInfo("warn", "Checker texture not found. Check files or try to re-install PolygonTools.")
        else:
            conclusion_text = conclusion.noSelection(current_languge, "assign_diag_checker")
            self.txtbrowUVConclusion.setHtml(conclusion_text) 

            self.showInfo("warn", "Cant assign checker. Please select Editable Poly object(s).")


    #Aassign diagonal checker    
    def btnCheGradClicked (self):

        current_languge = cfgl.configLoader()[14]
                
        #getselection
        try:
            selection_array = gen_func.checkSelection()

            sel_objects = selection_array[0]
            sel_editable_poly_objects = selection_array[1]
            sel_editable_poly_nodes = selection_array[3]
        except:
            print ("Please select something. Editable Poly object for example...")

        if len(sel_editable_poly_objects) > 0:

            checker_material_data = []
            #0-scene_materials, PTCheckerInScene, Tiling, checkers_in_scene, GradientOnly, std_checker_data, digital_checker_data, diagonal_checker_data, 8-gradient_checker_data
            checker_material_data = checkShaderIntegrity()

            #previous mats
            self.previous_materials_data = getMaterials(sel_editable_poly_nodes)

            #if checker in scene
            if (checker_material_data[8][0] != "None"):
                changeCheckerTexture ("checker_gradient", sel_editable_poly_objects, checker_material_data[8])
            else:
                createCheckerMaterial("04")
                checker_material_data = checkShaderIntegrity()
                changeCheckerTexture ("checker_gradient", sel_editable_poly_objects, checker_material_data[8])  

            self.btnRemCheck.setEnabled(True)                

            conclusion_text = conclusion.uvOperationConclusion (current_languge, "assign_grad_checker")
            self.txtbrowUVConclusion.setHtml(conclusion_text)

            self.showInfo("info", "Gradient checker was assigned!")
        
        else:
            conclusion_text = conclusion.noSelection(current_languge, "assign_grad_checker")
            self.txtbrowUVConclusion.setHtml(conclusion_text) 

            self.showInfo("warn", "Cant assign checker. Please select Editable Poly object(s).")

    #256
    def setTile256Toggled (self):     

        

        CreatedCheckers = checkCreatedCheckers()

        if CreatedCheckers == 0:
            self.gboxCheckRes.setEnabled(False)
            print("PolygonTools. Checker Materials not yet created or it's integrity broken!")

        if (self.rbtn256.isChecked() == True) and (CreatedCheckers > 0):
            setCheckerTextureRepeat(2, 2)
            self.showInfo("info", "256x256 texture was emulated.")
            rt.execute ("redrawViews()")

    #512                    
    def setTile512Toggled (self):

        

        CreatedCheckers = checkCreatedCheckers()

        if CreatedCheckers == 0:
            self.gboxCheckRes.setEnabled(False)
            print("PolygonTools. Checker Materials not yet created or it's integrity broken!")

        if self.rbtn512.isChecked() == True and (CreatedCheckers > 0):
            setCheckerTextureRepeat(4, 4)
            self.showInfo("info", "512x512 texture was emulated.")
            rt.execute ("redrawViews()")

    #1K
    def setTile1024Toggled (self):

        

        CreatedCheckers = checkCreatedCheckers()

        if CreatedCheckers == 0:
            self.gboxCheckRes.setEnabled(False)
            print("PolygonTools. Checker Materials not yet created or it's integrity broken!")

        if self.rbtn1024.isChecked() == True and (CreatedCheckers > 0):
            setCheckerTextureRepeat(8, 8)
            self.showInfo("info", "1024x1024 texture was emulated.")
            rt.execute ("redrawViews()")
    
    #2K            
    def setTile2048Toggled (self):

        

        CreatedCheckers = checkCreatedCheckers()

        if CreatedCheckers == 0:
            self.gboxCheckRes.setEnabled(False)
            print("PolygonTools. Checker Materials not yet created or it's integrity broken!")

        if self.rbtn2048.isChecked() == True and (CreatedCheckers > 0):
            setCheckerTextureRepeat(16, 16)
            self.showInfo("info", "2048x2048 texture was emulated.")
            rt.execute ("redrawViews()")
    
    #4K
    def setTile4096Toggled (self):

        

        CreatedCheckers = checkCreatedCheckers()

        if CreatedCheckers == 0:
            self.gboxCheckRes.setEnabled(False)
            print("PolygonTools. Checker Materials not yet created or it's integrity broken!")

        if self.rbtn4096.isChecked() == True and (CreatedCheckers > 0):
            setCheckerTextureRepeat(32, 32)
            self.showInfo("info", "4096x4096 texture was emulated.")
            rt.execute ("redrawViews()")
    
    #8K
    def setTile8192Toggled (self):

        

        CreatedCheckers = checkCreatedCheckers()

        if CreatedCheckers == 0:
            self.gboxCheckRes.setEnabled(False)
            print("PolygonTools. Checker Materials not yet created or it's integrity broken!")

        if self.rbtn8192.isChecked() == True and (CreatedCheckers > 0):
            setCheckerTextureRepeat(64, 64)
            self.showInfo("info", "8192x8192 texture was emulated.")
            rt.execute ("redrawViews()")


    def checkCheckerTextureRepeat(self):

        self.btnRemCheck.setEnabled(True)
        self.gboxCheckRes.setEnabled(True)

        if self.rbtn256.isChecked() == True:
            setCheckerTextureRepeat(2, 2)
        
        if self.rbtn512.isChecked() == True:
            setCheckerTextureRepeat(4, 4)
        
        if self.rbtn1024.isChecked() == True:
            setCheckerTextureRepeat(8, 8)
        
        if self.rbtn2048.isChecked() == True:
            setCheckerTextureRepeat(16, 16)
        
        if self.rbtn4096.isChecked() == True:
            setCheckerTextureRepeat(32, 32)
        
        if self.rbtn8192.isChecked() == True:
            setCheckerTextureRepeat(64, 64)

    #remove checker
    def btnRemCheckClicked (self):

        

        current_languge = cfgl.configLoader()[14]

        checker_material_data = []
        #0-scene_materials, PTCheckerInScene, Tiling, checkers_in_scene, GradientOnly, std_checker_data, digital_checker_data, diagonal_checker_data, 8-gradient_checker_data
        checker_material_data = checkShaderIntegrity()

        for i in range(len(checker_material_data[3])):

            Slot = str(checker_material_data[3][i][4])
            Place = str(checker_material_data[3][i][5])

            if Place == "Scene":
                rt.execute ("scenematerials[" + Slot + "].diffusemap = undefined")
                rt.execute ("scenematerials[" + Slot + "].name = \"0" + Slot  + " - Default\"")                        
                rt.execute ("scenematerials[" + Slot + "] = Standard()")
                
            if Place == "Slot":
                rt.execute ("meditMaterials[" + Slot + "].diffusemap = undefined")              
                rt.execute ("meditMaterials[" + Slot + "].name = \"0" + Slot  + " - Default\"")                                  
                rt.execute ("meditMaterials[" + Slot + "] = Standard()")                                        

        #try restore previous
        restorePreviousMat(self.previous_materials_data)

        rt.execute ("actionMan.executeAction 0 \"63545\"")

        #disable buttons            
        self.btnRemCheck.setEnabled(False)
        self.gboxCheckRes.setEnabled(False)

        conclusion_text = conclusion.uvOperationConclusion (current_languge, "delete_checker")
        self.txtbrowUVConclusion.setHtml(conclusion_text)

        self.showInfo("info", "Remove pt_checker_material's operation complete!")

    # x2 Scale UP
    def btnScale2Clicked(self):

        current_languge = cfgl.configLoader()[14]

        #getselection
        try:
            selection_array = gen_func.checkSelection()

            sel_objects = selection_array[0]
            sel_editable_poly_objects = selection_array[1]
            sel_editable_poly_nodes = selection_array[3]

        except:
            print ("Please select something. Editable Poly object(s) for example...")

        if len(sel_editable_poly_objects) > 0:
            scaleUV (sel_editable_poly_nodes, "Up", 2, 2)
            self.showInfo("info", "UV successfully scaled Up.")
        else:
            conclusion_text = conclusion.noSelection(current_languge, "scale_uv_up")
            self.txtbrowUVConclusion.setHtml(conclusion_text) 
            self.showInfo("warn", "Cant Scale UV Up. Please select Editable Poly object(s).")


    # x0.5 Scale Down    
    def btnScale05Clicked(self):

        current_languge = cfgl.configLoader()[14]

        #getselection
        try:
            selection_array = gen_func.checkSelection()

            sel_objects = selection_array[0]
            sel_editable_poly_objects = selection_array[1]
            sel_editable_poly_nodes = selection_array[3]

        except:
            print ("Please select something. Editable Poly object(s) for example...")

        if len(sel_editable_poly_objects) > 0:
            scaleUV (sel_editable_poly_nodes, "Down", 0.5, 0.5)
            self.showInfo("info", "UV successfully scaled Down.")
        else:
            conclusion_text = conclusion.noSelection(current_languge, "scale_uv_down")
            self.txtbrowUVConclusion.setHtml(conclusion_text) 
            self.showInfo("warn", "Cant Scale UV Down. Please select Editable Poly object(s).")


    def btnMoveUVRightClicked (self):

        current_languge = cfgl.configLoader()[14]

        #getselection
        try:
            selection_array = gen_func.checkSelection()

            sel_objects = selection_array[0]
            sel_editable_poly_objects = selection_array[1]
            sel_editable_poly_nodes = selection_array[3]

        except:
            print ("Please select something. Editable Poly object(s) for example...")

        if len(sel_editable_poly_objects) > 0:
            moveUV (sel_editable_poly_nodes, "Right", 1, 0)
            self.showInfo("info", "UV successfully moved Right.")
        else:
            conclusion_text = conclusion.noSelection(current_languge, "move_uv_right")
            self.txtbrowUVConclusion.setHtml(conclusion_text) 
            self.showInfo("warn", "Cant UV move UV Right. Please select Editable Poly object(s).")


    def btnMoveUVLeftClicked (self):

        current_languge = cfgl.configLoader()[14]

        #getselection
        try:
            selection_array = gen_func.checkSelection()

            sel_objects = selection_array[0]
            sel_editable_poly_objects = selection_array[1]
            sel_editable_poly_nodes = selection_array[3]

        except:
            print ("Please select something. Editable Poly object(s) for example...")

        if len(sel_editable_poly_objects) > 0:
            moveUV (sel_editable_poly_nodes, "Left", -1, 0)
            self.showInfo("info", "UV successfully moved Left.")
        else:
            conclusion_text = conclusion.noSelection(current_languge, "move_uv_left")
            self.txtbrowUVConclusion.setHtml(conclusion_text) 
            self.showInfo("warn", "Cant UV move UV Left. Please select Editable Poly object(s).")


    def btnMoveUVUpClicked (self):

        current_languge = cfgl.configLoader()[14]

        #getselection
        try:
            selection_array = gen_func.checkSelection()

            sel_objects = selection_array[0]
            sel_editable_poly_objects = selection_array[1]
            sel_editable_poly_nodes = selection_array[3]

        except:
            print ("Please select something. Editable Poly object(s) for example...")

        if len(sel_editable_poly_nodes) > 0:
            moveUV (sel_editable_poly_objects, "Up", 0, 1)
            self.showInfo("info", "UV successfully moved Up.")
        else:
            conclusion_text = conclusion.noSelection(current_languge, "move_uv_up")
            self.txtbrowUVConclusion.setHtml(conclusion_text) 
            self.showInfo("warn", "Cant UV move UV Up. Please select Editable Poly object(s).")


    def btnMoveUVDownClicked (self):

        current_languge = cfgl.configLoader()[14]

        #getselection
        try:
            selection_array = gen_func.checkSelection()

            sel_objects = selection_array[0]
            sel_editable_poly_objects = selection_array[1]
            sel_editable_poly_nodes = selection_array[3]

        except:
            print ("Please select something. Editable Poly object(s) for example...")

        if len(sel_editable_poly_objects) > 0:
            moveUV (sel_editable_poly_nodes, "Down", 0, -1)
            self.showInfo("info", "UV successfully moved Down.")
        else:
            conclusion_text = conclusion.noSelection(current_languge, "move_uv_down")
            self.txtbrowUVConclusion.setHtml(conclusion_text)
            self.showInfo("warn", "Cant UV move UV Down. Please select Editable Poly object(s).")             


    def btnViewUVPressed(self):

        current_languge = cfgl.configLoader()[14]

        #getselection
        try:
            selection_array = gen_func.checkSelection()

            sel_objects = selection_array[0]
            sel_editable_poly_objects = selection_array[1]

            sel_editable_poly_nodes = selection_array[3]

        except:
            print ("Please select something. Editable Poly object for example...")

        if len(sel_editable_poly_objects) > 0:

            #if pressed
            if self.btnViewUV.isChecked() == True:

                checker_material_data = []
                checker_material_data = checkShaderIntegrity()

                #try restore previous
                restorePreviousMat(self.previous_materials_data)

                if checker_material_data[9] == True:
                    DelUVShaders()
                    self.btnViewUV.setText("Show UV")      

                self.showInfo("info", "UV Texture was successfully removed.")           

            else:
                try:
                    #previous mats
                    self.previous_materials_data = getMaterials(sel_editable_poly_nodes)

                    renderUV(sel_editable_poly_objects)

                    self.btnViewUV.setText("Hide UV")

                    conclusion_text = conclusion.uvOperationConclusion (current_languge, "assign_uv")
                    self.txtbrowUVConclusion.setHtml(conclusion_text)

                    self.showInfo("info", "UV Texture was successfully assigned to objects.")                    
                except:
                    self.showInfo ("warn", "Can't create UV Texture.")            
        else:
            conclusion_text = conclusion.noSelection(current_languge, "show_uv")
            self.txtbrowUVConclusion.setHtml(conclusion_text)            

            #If nothing selected
            self.btnViewUV.setChecked(True)

            checker_material_data = []
            checker_material_data = checkShaderIntegrity()
            
            #delete shader if not selected
            if checker_material_data[9] == True:
                DelUVShaders()
                self.btnViewUV.setText("Show UV")
                self.showInfo("info", "All UV Texture was successfully removed.")
            else:
                self.showInfo ("warn", "Please select something. Editable Poly object for example...") 


def checkCreatedCheckers():
    
    CreatedCheckers = 0

    checker_material_data = []
    #0-scene_materials, PTCheckerInScene, Tiling, checkers_in_scene, GradientOnly, std_checker_data, digital_checker_data, diagonal_checker_data, 8-gradient_checker_data
    checker_material_data = checkShaderIntegrity()

    if checker_material_data[5] != "None":        
        CreatedCheckers += 1
    
    if checker_material_data[6] != "None":        
        CreatedCheckers += 1

    if checker_material_data[7] != "None":        
        CreatedCheckers += 1

    return CreatedCheckers


#check all need material params
def checkShaderIntegrity():

    name_class_bitmap = []
    scene_materials = []
    checkers_in_scene = []
    UVMatInScene = False
    PTCheckerInScene = False
    PTMatteInScene = False
    PTGlossInScene = False
    PTNMInScene = False

    CorrectMaterialNames = ['pt_checker_material_01__Legacy', 'pt_checker_material_02__Legacy', 'pt_checker_material_03__Legacy', 'pt_checker_material_04__Legacy']
    CorrectDiffuseNames = ['checker_diagonal.tga', 'checker_digital.tga', 'checker_standard.tga', "pt_gradient_ramp"]

    
    SceneMaterialsCount = rt.scenematerials.count

    #scene mats
    for i in range(0, SceneMaterialsCount):

        name_class_bitmap = []

        MultiSubMat = False

        MaterialName = rt.scenematerials[i].name
        MaterialClass = str(rt.scenematerials[i])

        if "pt_uvrender_" in MaterialName:
            UVMatInScene = True

        if "PT_Matte_Material" in MaterialName:
            PTMatteInScene = True

        if "PT_Gloss_Material" in MaterialName:
            PTGlossInScene = True

        if "PT_NM_Material" in MaterialName:
            PTNMInScene = True          

        try:
            DiffuseMapStatus = str(rt.scenematerials[i].diffuseMap)
            DiffuseMapTemp = rt.scenematerials[i].diffuseMap.filename
            DiffuseMap = os.path.basename(DiffuseMapTemp)
            VTiling = int(rt.scenematerials[i].diffuseMap.coords.V_Tiling)
            #DiffuseMapName = rt.meditMaterials[i].diffuseMap.name
        except:
            DiffuseMap = "None"
            VTiling = "None"            

        try:
            DiffuseMapName = rt.scenematerials[i].diffuseMap.name
            if DiffuseMapName == "pt_gradient_ramp":
                DiffuseMap = "pt_gradient_ramp"
                VTiling = 1
        except:
            pass

        name_class_bitmap.append(MaterialName)
        name_class_bitmap.append(MaterialClass)
        name_class_bitmap.append(DiffuseMap)
        name_class_bitmap.append(VTiling)
        name_class_bitmap.append(i+1) #scene mats start from 1
        name_class_bitmap.append("Scene")

        if name_class_bitmap not in scene_materials:
            scene_materials.append(name_class_bitmap)

    #slots mats
    for i in range(0, 24):
        
        name_class_bitmap = []
        
        MultiSubMat = False

        TempMatName = str(rt.meditMaterials[i])

        if "pt_uvrender_" in TempMatName:
            UVMatInScene = True

        if "PT_Matte_Material" in TempMatName:
            PTMatteInScene = True

        if "PT_Gloss_Material" in TempMatName:
            PTGlossInScene = True

        if "PT_NM_Material" in TempMatName:
            PTNMInScene = True          

        if ":Standard" in TempMatName:    
            MaterialName = TempMatName.replace(":Standard", "")
        else:
            MaterialName = TempMatName

        MaterialClass = str(rt.meditMaterials[i])

        try:
            DiffuseMapStatus = str(rt.meditMaterials[i].diffuseMap)
            DiffuseMapTemp = rt.meditMaterials[i].diffuseMap.filename
            DiffuseMap = os.path.basename(DiffuseMapTemp)
            VTiling = int(rt.meditMaterials[i].diffuseMap.coords.V_Tiling)
        except:
            DiffuseMap = "None"
            VTiling = "None"

        try:
            DiffuseMapName = rt.meditMaterials[i].diffuseMap.name
            if DiffuseMapName == "pt_gradient_ramp":
                DiffuseMap = "pt_gradient_ramp"
                VTiling = 1
        except:
            pass

        name_class_bitmap.append(MaterialName)
        name_class_bitmap.append(MaterialClass)
        name_class_bitmap.append(DiffuseMap)
        name_class_bitmap.append(VTiling)
        name_class_bitmap.append(i+1) #scene mats start from 1
        name_class_bitmap.append("Slot")

        if name_class_bitmap not in scene_materials:
            scene_materials.append(name_class_bitmap)

    Tiling = 1

    for i in range(len(scene_materials)):
        if (scene_materials[i][0] in CorrectMaterialNames) and (scene_materials[i][2] in CorrectDiffuseNames):
            PTCheckerInScene = True 

            checkers_in_scene.append(scene_materials[i]) #add checker

    std_checker_data = []
    digital_checker_data = []
    diagonal_checker_data = []
    gradient_checker_data = []

    if len(checkers_in_scene) > 0:

        counter = 0
        ItemForDel = ""
        for i in range(len(checkers_in_scene)):
            if checkers_in_scene[i][0] == CorrectMaterialNames[0]:
                counter += 1
                if counter > 1:
                    ItemForDel = str(i)
        if counter > 1:
            del checkers_in_scene[int(ItemForDel)]

        counter = 0
        ItemForDel = ""
        for i in range(len(checkers_in_scene)):
            if checkers_in_scene[i][0] == CorrectMaterialNames[1]:
                counter += 1
                if counter > 1:
                    ItemForDel = str(i)
        if counter > 1:
            del checkers_in_scene[int(ItemForDel)]


        counter = 0
        ItemForDel = ""
        for i in range(len(checkers_in_scene)):
            if checkers_in_scene[i][0] == CorrectMaterialNames[2]:
                counter += 1
                if counter > 1:
                    ItemForDel = str(i)
        if counter > 1:
            del checkers_in_scene[int(ItemForDel)]

        counter = 0
        ItemForDel = ""
        for i in range(len(checkers_in_scene)):
            if checkers_in_scene[i][0] == CorrectMaterialNames[3]:
                counter += 1
                if counter > 1:
                    ItemForDel = str(i)
        if counter > 1:
            del checkers_in_scene[int(ItemForDel)]

        for i in range(len(checkers_in_scene)):
            if CorrectMaterialNames[0] in checkers_in_scene[i]:
                std_checker_data = checkers_in_scene[i]

        if std_checker_data == []:
            std_checker_data.append("None")

        for i in range(len(checkers_in_scene)):
            if CorrectMaterialNames[1] in checkers_in_scene[i]:
                digital_checker_data = checkers_in_scene[i]

        if digital_checker_data == []:
            digital_checker_data.append("None")

        for i in range(len(checkers_in_scene)):
            if CorrectMaterialNames[2] in checkers_in_scene[i]:
                diagonal_checker_data = checkers_in_scene[i]
            #else:
            # diagonal_checker_data.append("None")

        if diagonal_checker_data == []:
            diagonal_checker_data.append("None")

        for i in range(len(checkers_in_scene)):
            if CorrectMaterialNames[3] in checkers_in_scene[i]:
                gradient_checker_data = checkers_in_scene[i]

        if gradient_checker_data == []:
            gradient_checker_data.append("None")

        GradientOnly = False
        if (len(checkers_in_scene) == 1) and (checkers_in_scene[0][0] == CorrectMaterialNames[3]):
            GradientOnly = True
            Tiling = 2
        else:
            Tiling = checkers_in_scene[0][3]
    else:
        GradientOnly = False
        std_checker_data.append("None")
        digital_checker_data.append("None")
        diagonal_checker_data.append("None")
        gradient_checker_data.append("None")

    return scene_materials, PTCheckerInScene, Tiling, checkers_in_scene, GradientOnly, std_checker_data, digital_checker_data, diagonal_checker_data, gradient_checker_data, UVMatInScene, PTMatteInScene, PTGlossInScene, PTNMInScene


#assign ready texture to object
def changeCheckerTexture (CheckerType, sel_editable_poly_objects, checker_material_data):

    rt.execute ("UserScriptsDir = getDir #userScripts")
    TempGetDirPath = rt.UserScriptsDir

    #change symbols
    GetDirPath = TempGetDirPath.replace ("\\", "/") + "/polygontools/pt_modules/"

    #type selector
    if CheckerType == "checker_standard":
        Type = "01"
        PathToCheckerFile = GetDirPath + "checker_standard.tga"

    if CheckerType == "checker_digital":
        Type = "02"
        PathToCheckerFile = GetDirPath + "checker_digital.tga"

    if CheckerType == "checker_diagonal":
        Type = "03"
        PathToCheckerFile = GetDirPath + "checker_diagonal.tga"

    if CheckerType == "checker_gradient":
        PathToCheckerFile = "pt_gradient_ramp"
        Type = "04"        
             
    #turn on textures in viewport
    rt.execute ("actionMan.executeAction -844228238 \"13\"")
    rt.execute ("actionMan.executeAction 0 \"63566\"")
    
    #slot in materials
    Slot = str(checker_material_data[4])

    #scene or slots
    Place = str(checker_material_data[5])

    #check files
    if checkCheckerTextureFile (PathToCheckerFile) == True and Type != "04":
        #assign to all selected objects
        for i in range(len(sel_editable_poly_objects)):
            if Place == "Scene":
                rt.execute ("$" + sel_editable_poly_objects[i] + ".material = scenematerials[" + Slot + "]")                        
            if Place == "Slot":
                rt.execute ("$" + sel_editable_poly_objects[i] + ".material = meditMaterials[" + Slot + "]")                        

        ChangeCheckerResult = True
    elif Type == "04":
        for i in range(len(sel_editable_poly_objects)):
            if Place == "Scene":
                rt.execute ("$" + sel_editable_poly_objects[i] + ".material = scenematerials[" + Slot + "]")                        
            if Place == "Slot":
                rt.execute ("$" + sel_editable_poly_objects[i] + ".material = meditMaterials[" + Slot + "]")                        
        
        ChangeCheckerResult = True
        
        rt.execute ("redrawViews()")

    else:
        
        ChangeCheckerResult = False
        print ("PolygonTools. Checker texture not found. Check files or try to re-install PolygonTools.")
            
    return ChangeCheckerResult


#exist file or not
def checkCheckerTextureFile (FilePath):        
    try:
        os.path.getsize(FilePath)
        CheckFileResult = True
    except:
        if FilePath != "pt_gradient_ramp":
            print ((FilePath + " not exist. Check files. Try to re-install PolygonTools."))
            CheckFileResult = False
        else:
            CheckFileResult = True
    
    return CheckFileResult


def createCheckerMaterial(CheckerType):

    
    
    #set tupe
    Type = CheckerType
    
    CorrectMaterialName = "pt_checker_material_" + Type

    try:
        rt.execute ("UserScriptsDir = getDir #userScripts")

        TempGetDirPath = rt.UserScriptsDir

        #change symbols
        GetDirPath = TempGetDirPath.replace ("\\", "/") + "/polygontools/pt_modules/"

        for i in range(0, 24):
            SlotName = str(rt.meditMaterials[i])
            if "- Default:" in SlotName:
                Slot = i
                break
            else:
                Slot = 0

        if Type == "01":
            PathToChecker = GetDirPath + "checker_standard.tga"
        elif Type == "02":
            PathToChecker = GetDirPath + "checker_digital.tga"
        elif Type == "03":
            PathToChecker = GetDirPath + "checker_diagonal.tga"

        #mat for checker
        rt.execute ("CheckerMat = Standard()")
        
        rt.CheckerMat.name = CorrectMaterialName
        
        rt.meditMaterials[Slot] = rt.CheckerMat
        
        #std or ramp
        if Type != "04":
            try:
                rt.CheckerMat.diffuseMapEnable = True
            except:
                print ("EXCEPTION in 'createCheckerMaterial' function. diffuseMapEnable Error!")

            try:
                rt.execute ("CheckerMat.diffusemap = Bitmaptexture fileName: \"" + PathToChecker + "\"")
            except:
                print ("EXCEPTION in 'createCheckerMaterial' function. Bitmaptexture fileName Error!")
        else:
            rt.execute ("CheckerMat.diffuseMap = Gradient_Ramp ()")
            rt.execute ("CheckerMat.diffuseMap.gradient_ramp.flag__1.color = color 0 0 255")
            rt.execute ("CheckerMat.diffuseMap.gradient_ramp.flag__2.color = color 255 0 0")
            rt.execute ("CheckerMat.diffuseMap.gradient_ramp.flag__3.color = color 0 255 0")
            rt.execute ("CheckerMat.diffuseMap.name = \"pt_gradient_ramp\"")
            
        print ("PolygonTools. Material for checker type", CheckerType, "was created!")

        CreateCheckerMaterial = True    
    except:
        print ("PolygonTools. Can't create material for checker type", CheckerType)
        CreateCheckerMaterial = False
    
    return CreateCheckerMaterial

#repeat of checker texture
def setCheckerTextureRepeat (u, v):

    
    
    ChangeResult = []

    checker_material_data = []
    checker_material_data = checkShaderIntegrity()

    for i in range(5, 8):
        if checker_material_data[i][0] != "None":
            
            try:
                Place = checker_material_data[i][5]
                Slot = str(checker_material_data[i][4])
                
                if Place == "Scene":
                    rt.execute ("scenematerials[" + Slot + "].diffuseMap.coords.U_Tiling = " + str(u))
                    rt.execute ("scenematerials[" + Slot + "].diffuseMap.coords.V_Tiling = " + str(v))
                if Place == "Slot":
                    rt.execute ("meditMaterials[" + Slot + "].diffuseMap.coords.U_Tiling = " + str(u))
                    rt.execute ("meditMaterials[" + Slot + "].diffuseMap.coords.V_Tiling = " + str(v))

                ChangeResult.append(True)
            except:
                ChangeResult.append(False)
    
    return ChangeResult  

# Scale
def scaleUV ( sel_editable_poly_nodes, Action, sU, sV ):

    
    #get selection
    SelectedNodes = rt.selection

    print ("PolygonTools. UV Scale " + Action + ":")
    
    rt.execute ("max modify mode")
    
    for i in range(len(sel_editable_poly_nodes)):
        
        NodeName = sel_editable_poly_nodes[i]
        
        rt.select(NodeName)
        rt.subobjectLevel = 4
        rt.execute("$.EditablePoly.SetSelection #Face #{}")
        rt.subobjectLevel = 0

    rt.execute ("subobjectLevel = 0")

    try:
        for i in range(len(sel_editable_poly_nodes)):
            
            rt.select(sel_editable_poly_nodes[i])            
            rt.execute ("modPanel.addModToSelection (UVW_Xform ()) ui:on")
            rt.execute ("$.modifiers[#UVW_Xform].U_Tile = " + str(sU))
            rt.execute ("$.modifiers[#UVW_Xform].V_Tile = " + str(sV))
            rt.execute ("$.modifiers[#UVW_Xform].W_Tile = " + str(sV))
            
            rt.execute ("convertto $" + sel_editable_poly_nodes[i].name + " editable_poly")

            print ('\t', (str(i + 1) + "."), sel_editable_poly_nodes[i].name, "... OK")
    except:
        pass

    #return selection
    rt.select(SelectedNodes)

    rt.execute ("redrawViews()")

        
# Move
def moveUV ( sel_editable_poly_nodes, Action, vU, vV ):
    
    
    #get selection
    SelectedNodes = rt.selection

    print ("PolygonTools. UV Move " + Action + ":")

    rt.execute ("max modify mode")

    for i in range(len(sel_editable_poly_nodes)):
        
        NodeName = sel_editable_poly_nodes[i]

        rt.select(NodeName)
        rt.subobjectLevel = 4
        rt.execute("$.EditablePoly.SetSelection #Face #{}")
        rt.subobjectLevel = 0
    
    try:
        for i in range(len(sel_editable_poly_nodes)): 
            
            rt.select(sel_editable_poly_nodes[i]) 

            rt.execute ("modPanel.addModToSelection (UVW_Xform ()) ui:on")
            rt.execute ("$.modifiers[#UVW_Xform].U_Offset = " + str(vU))
            rt.execute ("$.modifiers[#UVW_Xform].V_Offset = " + str(vV))

            rt.execute ("convertto $" + sel_editable_poly_nodes[i].name + " editable_poly")
           
            print ('\t', (str(i + 1) + "."), sel_editable_poly_nodes[i].name, "... OK")
    except:
        pass

    #return selection
    rt.select(SelectedNodes)
    
    rt.execute ("redrawViews()")

#render UV as texture
def renderUV(sel_editable_poly_objects):

    

    #get selection
    SelectedNodes = rt.selection

    rt.execute ("max modify mode")

    TempGetDirPath = rt.execute ("GetDir #temp")
    
    #change symbols
    GetDirPath = TempGetDirPath.replace ("\\", "/")

    #get selection
    SelNodes = rt.selection

    for i in range(len(sel_editable_poly_objects)):  

        rt.execute ("select $" + sel_editable_poly_objects[i])
        rt.execute ("modPanel.addModToSelection (Unwrap_UVW ()) ui:off")
            
        rt.execute ("$.modifiers[#Unwrap_UVW].renderuv_width = 1024")
        rt.execute ("$.modifiers[#Unwrap_UVW].renderuv_height = 1024")
        rt.execute ("$.modifiers[#unwrap_uvw].renderuv_fillmode = 1;")
        rt.execute ("$.modifiers[#Unwrap_UVW].renderuv_seamedges = on")
        rt.execute ("$.modifiers[#unwrap_uvw].renderuv_seamColor = color 0 255 0;")
        rt.execute ("$.modifiers[#unwrap_uvw].renderuv_overlapColor = color 255 128 128;")
        rt.execute ("$.modifiers[#unwrap_uvw].renderuv_fillColor = color 128 128 128;")
        rt.execute ("$.modifiers[#unwrap_uvw].renderuv_showframebuffer = false;")

        #random for name
        RandInd = str(random.randrange(1000))

        UVRFileName = GetDirPath + "/_renderUV_" + sel_editable_poly_objects[i] + "_" + RandInd + "_.jpg"
        #print (UVRFileName)
            
        rt.execute ("$.modifiers[#unwrap_uvw].unwrap5.renderUV \"" + UVRFileName + "\";")

        rt.execute ("UVRender = Standard ()")

        rt.UVRender.name = "pt_uvrender_" + sel_editable_poly_objects[i] + "_" + RandInd

        #find free slot
        for i in range(0, 24):
            SlotName = str(rt.meditMaterials[i])
            if "- Default:" in SlotName:
                Slot = i
                break
            else:
                Slot = 0


        rt.meditMaterials[Slot] = rt.UVRender
        rt.UVRender.diffuseMapEnable = True

        rt.execute ("UVRender.diffusemap = Bitmaptexture fileName: \"" + UVRFileName + "\"")

        rt.execute ("$.material = UVRender")

        rt.execute ("actionMan.executeAction 0 \"63545\"")
        rt.execute ("convertto $ editable_poly")
        rt.execute ("redrawViews()")

    #return selection
    rt.select(SelectedNodes)


def DelUVShaders ():

    
    #get selection
    SelectedNodes = rt.selection

    
    SceneMaterialsCount = rt.scenematerials.count

    #scene mats
    for i in range(0, SceneMaterialsCount):

        Slot = str(i+1)
        
        MaterialName = rt.scenematerials[i].name
        
        if "pt_uvrender_" in MaterialName:
            try:
                DiffuseMapFilenameTemp = rt.scenematerials[i].diffuseMap.filename
                DiffuseMapFilename = DiffuseMapFilenameTemp.replace ("\\", "/")
                rt.execute ("deleteFile " + "\"" + DiffuseMapFilename + "\"") 
            except:
                pass

            rt.execute ("scenematerials[" + Slot + "].diffusemap = undefined")
            rt.execute ("scenematerials[" + Slot + "].name = \"0" + Slot  + " - Default\"")                        
            rt.execute ("scenematerials[" + Slot + "] = Standard()")

    #slots
    for i in range(0, 24):
        
        MaterialName = str(rt.meditMaterials[i])

        Slot = str(i+1)
        
        if "pt_uvrender_" in MaterialName:
            try:
                DiffuseMapFilenameTemp = rt.scenematerials[i].diffuseMap.filename
                DiffuseMapFilename = DiffuseMapFilenameTemp.replace ("\\", "/")
                rt.execute ("deleteFile " + "\"" + DiffuseMapFilename + "\"") 
            except:
                pass

            rt.execute ("meditMaterials[" + Slot + "].diffusemap = undefined")              
            rt.execute ("meditMaterials[" + Slot + "].name = \"0" + Slot  + " - Default\"")                                  
            rt.execute ("meditMaterials[" + Slot + "] = Standard()")      

    rt.execute ("redrawViews()")

    #return selection
    rt.select(SelectedNodes)


def getMaterials(sel_editable_poly_nodes):

    

    materials_in_scene = []

    skip_names = ['pt_checker_material_01', 'pt_checker_material_02', 'pt_checker_material_03', 'pt_checker_material_04']

    for i in range(len(sel_editable_poly_nodes)):

        current_material = []
    
        #get name and node
        NodeName = sel_editable_poly_nodes[i]

        try:
            CurrentMaterial = NodeName.material
            MaterialName = CurrentMaterial.name
        except:
            MaterialName = "undefined"
        
        if MaterialName not in skip_names:
            current_material.append(NodeName.name)
            current_material.append(MaterialName)
            materials_in_scene.append(current_material)
        else:
            pass

    return materials_in_scene

#restore previous mat if Exists
def restorePreviousMat(previous_materials_data):

    

    for i in range(len(previous_materials_data)):
        
        OjectName = previous_materials_data[i][0]
        MaterialName = previous_materials_data[i][1]
        
        #slot
        try:
            rt.execute ("$" + OjectName + ".material = meditMaterials[\"" + MaterialName + "\"]")
        except:
            pass                        
        
        #scene
        try:
            rt.execute ("$" + OjectName + ".material = scenematerials[\"" + MaterialName + "\"]")
        except:
            pass

    print ("\nPolygonTools: Previous materials was restored!")
    rt.execute ("redrawViews()")
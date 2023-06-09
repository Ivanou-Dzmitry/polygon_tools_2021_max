# This Python file uses the following encoding: utf-8
#******************************************************************************************************
# Created: polygon.by        
# Last Updated: 8 may 2020
# Version: 2021.0.0 
#
# Authors:
#"Mango Team"
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

import pt_conclusion as conclusion
importlib.reload(conclusion)

import pt_texel_func as tef
importlib.reload (tef)

import pt_uv_func as uvf
importlib.reload (uvf)

import pt_gen_func as gen_func
importlib.reload(gen_func)

import pt_tools_func as tools
importlib.reload (tools)

RootDir = ".."

if RootDir not in sys.path:
  sys.path.append( RootDir )
  
import pt_config_loader as cfgl
importlib.reload(cfgl)

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import *

#GUI    
class PT_Check_Tab (QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        
        #set layoit
        self.tabCheck_v_layout = QVBoxLayout(self)
        self.tabCheck_v_layout.setAlignment(Qt.AlignTop)

        MaxWidth = 370

        currentDir = os.path.dirname(__file__)
        try:
            iconChecker  = QPixmap(currentDir +"/icons/checker_icon.png")
        except:
            print( "PolygonTools: Can't load icons for Checker Tab! Check icon files in pt_modules/icons directory.")
        
        self.btnCheck = QPushButton("Check")
        self.btnCheck .setStyleSheet("color:#000000;background-color:#E1E1E1;")
        self.btnCheck.setMaximumWidth(75)
        self.btnCheck.setIcon(iconChecker)
        
        self.pbChekProgress = QProgressBar()
        self.pbChekProgress.setRange(0,100)
        self.pbChekProgress.setValue(0)
        self.pbChekProgress.setMaximumWidth(MaxWidth)

                
        self.lblInfo = QLabel("Please select one ore more Mesh objects and press Check button.")
        self.lblInfo.setMinimumHeight(20)
        self.lblInfo.setMargin(5)
        
        self.tabCheck_h_layout_01 = QHBoxLayout()
        self.tabCheck_h_layout_01.setAlignment(Qt.AlignLeft)
        
        self.tabCheck_v_layout.addLayout(self.tabCheck_h_layout_01)
        
        self.tabCheck_h_layout_01.addWidget(self.btnCheck)
        self.tabCheck_h_layout_01.addWidget(self.pbChekProgress)
        
        self.tabCheck_v_layout.addWidget(self.lblInfo)
    
        #colors
        global green
        green = ("<font color='#8dc63f'>" + u'\N{Full Block}' + "</font>")
        
        global red
        red = ("<font color='#ed1c24'>" + u'\N{Full Block}' + "</font>")
        
        global black
        black = ("<font color='#000000'>" + u'\N{Full Block}' + "</font>")
        
        global orange
        orange = ("<font color='#ff5001'>" + u'\N{Full Block}' + "</font>")
        
        global yellow
        yellow = ("<font color='#ffd101'>" + u'\N{Full Block}' + "</font>")
        

        global ckecksText
        ckecksText = []
        
        global checkLabels
        checkLabels = []

        global checkMarks
        checkMarks = []
        
        global fixButtons
        fixButtons = []
        
        checkLayouts = []
        
        #Checks
        ckecksText.append("1. Correct system units")
        ckecksText.append("2. Correct file, object and material name.")
        ckecksText.append("3. Pivot should be in the Center of coordinates [0,0,0]")
        ckecksText.append("4. Pivot inside of Objects Bounding Box")
        ckecksText.append("5. No hidden objects and layers on scene")
        ckecksText.append("6. Backface Culling enabled")
        ckecksText.append("7. The object hasn\'t transformation")
        ckecksText.append("8. Correct Polygons")
        ckecksText.append("9. Correct Material on the scene")
        ckecksText.append("10. UV shells in [0,1] area")
        ckecksText.append("11. Quantity of Map Channels")
        ckecksText.append("12. UV-utilization")
        ckecksText.append("13. Correct Smoothing Groups")
        ckecksText.append("14. Quantity of Material ID's")
        
        #create checks structure
        for i in range(len(ckecksText)):
            
            #create labels names
            label_name = "self.lblItem_" + ckecksText[i]
            
            #label mark
            label_mark = "self.lblItem_Mark_" + ckecksText[i]
            
            #fix button
            fix_but_name = "self.btnFixItem_" + ckecksText[i]
            
            #create layouts names
            layout_name =  "self.tabCheck_h_lay_" + ckecksText[i]
            
            #create label
            label_name = QLabel()

            #add to array
            checkLabels.append(label_name)
            
            #create mark
            label_mark = QLabel()
            label_mark.setText( black )
            #add to array
            checkMarks.append(label_mark)
            
            #create button
            fix_but_name = QPushButton("Fix")
            fix_but_name.setEnabled(False)
            fix_but_name.setMaximumHeight(20)
            fix_but_name.setMaximumWidth(30)
            fixButtons.append(fix_but_name)
            
            #set check text
            label_name.setText(ckecksText[i])
            label_name.setFixedWidth(315)
            
            #create layout
            layout_name = QHBoxLayout()
            layout_name.setAlignment(Qt.AlignLeft)
            
            #add to array
            checkLayouts.append(layout_name)
            
            #add layout
            self.tabCheck_v_layout.addLayout(layout_name)
            
            #add label to layout
            layout_name.addWidget(label_name)
            layout_name.addWidget(label_mark)
            layout_name.addWidget(fix_but_name)
    
        self.btnLog = QPushButton("Open Log")
        self.tabCheck_v_layout.addWidget(self.btnLog )

        self.gboxCheckerConclusion = QGroupBox("Conclusion")
        self.gboxCheckerConclusion.setStyleSheet("color:#ffffff; background-color:#2b2b2b;")
        self.gboxCheckerConclusion.setMaximumWidth(MaxWidth)
        self.gboxCheckerConclusion.setMinimumHeight(170)
        self.gboxCheckerConclusion_v_layout = QVBoxLayout()        

        #conclusion text here
        self.txtbrowCheckerConclusion = QTextBrowser()
        self.txtbrowCheckerConclusion.setHtml("")

        self.gboxCheckerConclusion_v_layout.addWidget(self.txtbrowCheckerConclusion)    

        self.gboxCheckerConclusion.setLayout(self.gboxCheckerConclusion_v_layout)

        self.tabCheck_v_layout.addWidget(self.gboxCheckerConclusion)     

        #SIGNALS
        self.btnCheck.clicked.connect(self.btnCheckClicked)
        self.btnLog.clicked.connect(self.openListner)
        
        fixButtons[0].clicked.connect(self.unitsFix01)
        fixButtons[2].clicked.connect(self.pivotPointFix03)
        fixButtons[3].clicked.connect(self.pivotInsideBBoxFix04)
        fixButtons[4].clicked.connect(self.hiddenfrozenObjectsFix05)
        fixButtons[5].clicked.connect(self.backFaceCullingFix06)
        fixButtons[6].clicked.connect(self.transformationFix07)
        fixButtons[7].clicked.connect(self.correctPolygonsFix08)
        fixButtons[8].clicked.connect(self.materialFix09)
        fixButtons[12].clicked.connect(self.sgFix13)
        
        #no fixable
        #fixButtons[1].setText("     ")
        fixButtons[1].setMaximumWidth(0)
        #fixButtons[9].setText("     ")
        fixButtons[9].setMaximumWidth(0)
        #fixButtons[10].setText("     ")
        fixButtons[10].setMaximumWidth(0)
        #fixButtons[11].setText("     ")
        fixButtons[11].setMaximumWidth(0)
        fixButtons[13].setMaximumWidth(0)

        #arrays
        self.ObjWithPivotError = []
        self.ObjWithBBoxError = []
        self.ObjWithBackCull = []
        self.ObjWithTransform = []
        self.ObjWithPolyErrors = []
        self.ObjWithMatProblems = []
        self.ObjWithManyUVSets = []
        self.AllUVAreas = []
        self.hiddenObjects = []
        self.CheckErrorCount = []

        #intro text
        current_language = cfgl.configLoader()[14]
        self.txtbrowCheckerConclusion.setHtml(conclusion.checkerTabIntroConclusion(current_language))

    def openListner(self):
        
        rt.execute ("actionMan.executeAction 0 \"40472\"")


    #set check result to Zero
    def zeroResult(self):        
        for i in range(len(ckecksText)):
            checkLabels[i].setText(ckecksText[i])
            checkMarks[i].setText( black )
            fixButtons[i].setEnabled(False)
        
        self.pbChekProgress.setValue(0)
        self.lblInfo.setStyleSheet("")


    def btnCheckClicked (self):

        

        current_language = cfgl.configLoader()[14]    

        #getselection
        try:
            selection_array = gen_func.checkSelection()

            sel_objects = selection_array[0]
            sel_editable_poly_objects = selection_array[1]
            sel_editable_poly_nodes = selection_array[3]
        except:
            print ("Please select something. Editable Poly object for example...")

        #get selection
        SelectedNodes = rt.selection
        
        LongLine=''

        for i in range(0,60):
            LongLine = LongLine + "- "

        if len(sel_editable_poly_objects) > 0:

            CheckConclusion = []
            self.CheckErrorCount = []

            print ("Сheck started!", '\n', "Time:", rt.localTime[11:19], '\n')

            if len(sel_editable_poly_objects) == 1:
                self.lblInfo.setText(sel_editable_poly_objects[0] + " will be checked.")
            elif len(sel_editable_poly_objects) > 1:
                self.lblInfo.setText(str(len(sel_editable_poly_objects)) + " objects will be checked.")

            #Units
            CheckConclusion.append(self.unitsCheck01())
            self.pbChekProgress.setValue(7)
            print (checkLabels[0].text())
            
            print (LongLine, "1")

            #names
            CheckConclusion.append(self.namesCheck02(sel_editable_poly_nodes))            
            self.pbChekProgress.setValue(14)
            print ('\n', checkLabels[1].text() )

            print (LongLine, "2")
            
            #pivot
            CheckConclusion.append(self.pivotPointPos03(sel_editable_poly_nodes))
            self.pbChekProgress.setValue(21)
            print ('\n', checkLabels[2].text())

            print (LongLine, "3")

            #inside bbox
            CheckConclusion.append(self.pivotInsideBBox04(sel_editable_poly_nodes))
            self.pbChekProgress.setValue(28)
            print ('\n', checkLabels[3].text())
            
            print (LongLine, "4"    )

            #freeze hide
            CheckConclusion.append(self.hiddenfrozenObjects05())
            self.pbChekProgress.setValue(35)
            print ('\n', checkLabels[4].text())
            
            print (LongLine, "5")

            #backfaces
            CheckConclusion.append(self.backFaceCulling06(sel_editable_poly_nodes))
            self.pbChekProgress.setValue(42)
            print ('\n', checkLabels[5].text())

            print (LongLine, "6")

            #transform
            CheckConclusion.append(self.transformationCheck07(sel_editable_poly_nodes))
            self.pbChekProgress.setValue(49)
            print ('\n', checkLabels[6].text())

            print (LongLine, "7")

            #correct polygons
            CheckConclusion.append(self.correctPolygonsCheck08(sel_editable_poly_nodes))
            self.pbChekProgress.setValue(56)
            print ('\n', checkLabels[7].text())

            print (LongLine, "8")
            
            CheckConclusion.append(self.materialCheck09(sel_editable_poly_nodes))
            self.pbChekProgress.setValue(63)
            print ('\n', checkLabels[8].text())

            print (LongLine, "9")
            
            #uv area
            CheckConclusion.append(self.uvBorderCheck10(sel_editable_poly_nodes))
            self.pbChekProgress.setValue(70)
            print ('\n', checkLabels[9].text())

            print (LongLine, "10")
            
            CheckConclusion.append(self.uvSetsCountCheck11(sel_editable_poly_nodes))
            self.pbChekProgress.setValue(77)
            print ('\n', checkLabels[10].text())

            print (LongLine, "11")
            
            CheckConclusion.append(self.uvUtilCheck12(sel_editable_poly_nodes))
            self.pbChekProgress.setValue(84)
            print ('\n', checkLabels[11].text())

            print (LongLine, "12")
            
            CheckConclusion.append(self.sgCheck13(sel_editable_poly_nodes))
            self.pbChekProgress.setValue(100)
            print ('\n', checkLabels[12].text())

            print (LongLine, "13")

            #self.pbChekProgress.setValue(100)

            try:
                FoundErrors = int(sum(self.CheckErrorCount)/len((self.CheckErrorCount)))
            except:
                FoundErrors = 0

            #print ((CheckConclusion))

            conclusion_text = conclusion.checkResult(current_language, CheckConclusion)
            self.txtbrowCheckerConclusion.setHtml(conclusion_text) 
            
            if len(sel_editable_poly_objects) == 1:
                
                OjectName = str(sel_editable_poly_objects[0])
                
                if len(OjectName) > 24:
                    ShortObjectName = OjectName[:24] + "..."
                else:
                    ShortObjectName = OjectName

            if len(sel_editable_poly_objects) > 1:
                self.lblInfo.setText("Check complete for " + str(len(sel_editable_poly_objects)) + " objects. " + str(FoundErrors) + " check errors. See log for details.")
                print ('\n', "Check complete for " + str(len(sel_editable_poly_objects)) + " objects. " + str(FoundErrors) + " check errors. See log for details.", '\n')
            else:
                self.lblInfo.setText("Check complete for " + ShortObjectName + " mesh. " + str(FoundErrors) + " check errors.")
                print ('\n', "PolygonTools.", ("Check complete for " + OjectName + " mesh. " + str(FoundErrors) + " check errors."), '\n')

            self.lblInfo.setStyleSheet("background-color:#598527;")
            
            print ("Time:", rt.localTime[11:19])
            print (LongLine)
            
        else:
            conclusion_text = conclusion.noSelection(current_language, "checker")
            self.txtbrowCheckerConclusion.setHtml(conclusion_text) 
            self.lblInfo.setText("To start checking please select one or more Editable Poly objects!")     
            print (self.lblInfo.text())
            self.zeroResult()

        #return selection
        rt.select(SelectedNodes)


    #1 Units checker
    def unitsCheck01 (self):

        

        #get Units custom and current
        try:
            CustomSystemUnits = cfgl.configLoader()[9]
            CurrentWorkUnits = str(rt.units.Systemtype)

            if CustomSystemUnits == CurrentWorkUnits:
                checkMarks[0].setText( green )
                fixButtons[0].setEnabled(False)
                checkLabels[0].setText('1. System units is correct. It\'s \"' + CurrentWorkUnits + "\"")            
                return True
            else:
                checkMarks[0].setText( red )
                fixButtons[0].setEnabled(True)
                checkLabels[0].setText('1. System units is not correct. It\'s \"' + CurrentWorkUnits + "\"")    
                return False

        except:
            print ("PolygonTools. Problem with units checking.")
            self.CheckErrorCount.append(1)
        
        
    #1 Units fixer
    def unitsFix01(self):

        

        current_language = cfgl.configLoader()[14]

        try:
            #get custom units
            CustomSysUnits = cfgl.configLoader()[9]
            
            #set custom units
            if CustomSysUnits == 'meters':
                rt.execute ("units.Systemtype = #meters")
    
            if CustomSysUnits == 'centimeters':
                rt.execute ("units.Systemtype = #centimeters")
            
            if CustomSysUnits == 'millimeters':
                rt.execute ("units.Systemtype = #millimeters")
                            
            checkMarks[0].setText( green )
            fixButtons[0].setEnabled(False)
            checkLabels[0].setText('1. System units is fixed. Now It\'s \"' + CustomSysUnits + "\"")
            
            self.lblInfo.setText ('System units is fixed. Now It\'s \"' + CustomSysUnits + "\"")
            print ( "PolygonTools.", self.lblInfo.text())

            conclusion_text = conclusion.fixConclusion(current_language, "1", True)
            self.txtbrowCheckerConclusion.setHtml(conclusion_text) 
        except:
            print ("PolygonTools. Can\'t fix system units.")
            conclusion_text = conclusion.fixConclusion(current_language, "1", False)
            self.txtbrowCheckerConclusion.setHtml(conclusion_text)

    #2 Names
    def namesCheck02 (self, sel_editable_poly_nodes):
        
        try:
            NameErrors = namesChecker(sel_editable_poly_nodes)

            if len(NameErrors) == 0:
                checkMarks[1].setText( green )
                checkLabels[1].setText('2. Names is normal or correct')
                return True
            
            #show errors
            if len(NameErrors) == 1:
                checkMarks[1].setText( yellow )
                checkLabels[1].setText('2. Check: ' + NameErrors[0])
                return False
            elif len(NameErrors) > 1:
                checkMarks[1].setText( orange )
                all_errors = ""
                all_errors = (', '.join(NameErrors))
                checkLabels[1].setText('2. Check: ' + all_errors)
                return False            
        except:
            checkMarks[1].setText( red )
            checkLabels[1].setText("2. Can't check names")
            print ("PolygonTools. Can\'t check names.")
            self.CheckErrorCount.append(1)
            return False 


    #3 Pivot Point
    def pivotPointPos03 (self, sel_editable_poly_nodes):

        

        Errors = []
        
        self.ObjWithPivotError = []
        
        #get world space pivot point
        for i in range(len(sel_editable_poly_nodes)):

            try:
                #get pivot point pos
                pivot_point_pos = sel_editable_poly_nodes[i].pivot

                if sum(pivot_point_pos) != 0:
                    self.ObjWithPivotError.append(sel_editable_poly_nodes[i])
            except:
                Errors.append(sel_editable_poly_nodes[i])

        self.CheckErrorCount.append(len(Errors))
        
        if len(Errors) > 0:
            print ('\n', "ATTENTION! These objects have not been checked because they do not exist, has wrong name or contain serious errors (", len(Errors), "):", '\n')
            for i in range(len(Errors)):
                print ('\t', (str(i+1) + "."), Errors[i])

        if len(self.ObjWithPivotError) == 0:
            checkMarks[2].setText( green )
            checkLabels[2].setText('3. Pivot in the center of coordinates [0,0,0]')
            fixButtons[2].setEnabled(False)
            return True
        else:
            checkMarks[2].setText( yellow )
            checkLabels[2].setText('3. Check the Pivot Point position | (' +str(len(self.ObjWithPivotError)) + ")")
            fixButtons[2].setEnabled(True)

            print ("List of Objects with Pivot Point Not in [0,0,0]:")
            for i in range(len( self.ObjWithPivotError )):
                if len(self.ObjWithPivotError[i].name) == 0:
                    print ('\t', (str(i+1) + "."), "noname object #" + str(i))
                else: 
                    print ('\t', (str(i+1) + "."), self.ObjWithPivotError[i].name)

            print ('\n', len(self.ObjWithPivotError), "object(s) Needs to Check the Position of the Pivot Point.")
            return False


    #3 FIX
    def pivotPointFix03 (self):

        current_language = cfgl.configLoader()[14]        

        FixResult = []

        if len(self.ObjWithPivotError) > 0:
            
            print ("List of Objects with Fixed Pivot Position:")
                        
            for i in range(len(self.ObjWithPivotError)):

                NodeName = self.ObjWithPivotError[i]

                unicodeChecker(NodeName)

                if str(NodeName) != "<Deleted scene node>":
                    try:
                        #get pivot
                        ObjPivotPos = NodeName.pivot
                        
                        #set pivot
                        ObjPivotPos[0] = 0
                        ObjPivotPos[1] = 0
                        ObjPivotPos[2] = 0

                        NodeName.pivot = ObjPivotPos      

                        print ('\t', (str(i+1) + "."), NodeName.name)
                    except: #error
                        print ('\t', "ERROR: Pivot Position Not fixed for Object#" + str(i) + "! Object possibly Deleted or Renamed or has Other Problems.")
                        FixResult.append(self.ObjWithPivotError[i])
                else: #error
                    print ("PolygonTools. Object #" + str(i) + " Deleted, Renamed or Not Exists!")
                    FixResult.append(self.ObjWithPivotError[i])
            
            #one or many objects
            if len(self.ObjWithPivotError) == 1 and len(FixResult) == 0:
                self.lblInfo.setText("Pivot point position fixed for " + str(self.ObjWithPivotError[0].name) + " object.")                
            elif len(self.ObjWithPivotError) > 1 and len(FixResult) == 0:
                self.lblInfo.setText("Pivot point position fixed for " + str(len(self.ObjWithPivotError)) + " objects.")

            print ("")

            #problem with fix
            if len(FixResult) == 0:
                checkMarks[2].setText( green )
                checkLabels[2].setText('3. Pivot point position fixed. Now it\'s [0,0,0]')
                fixButtons[2].setEnabled(False)
                print (self.lblInfo.text(), "Now it\'s [0,0,0]")
                conclusion_text = conclusion.fixConclusion(current_language, "3", True)
                self.txtbrowCheckerConclusion.setHtml(conclusion_text) 
                print ("---")
                self.pivotInsideBBox04(self.ObjWithPivotError) #run 4
            else:
                checkMarks[2].setText( red )
                checkLabels[2].setText("3. Can't Fix Pivot point position for " + str(len(FixResult)) + "objects")
                fixButtons[2].setEnabled(False)

                self.lblInfo.setText("Fix Error. Object(s) possibly deleted or renamed. See log.")
                self.lblInfo.setStyleSheet("background-color:#ed1c24;")
                
                print ("PolygonTools:", self.lblInfo.text(), '\n')
            
                conclusion_text = conclusion.fixConclusion(current_language, "3", False)
                self.txtbrowCheckerConclusion.setHtml(conclusion_text)            

    #4 
    def pivotInsideBBox04 (self, sel_editable_poly_nodes):

        

        self.ObjWithBBoxError = []

        Errors = []
        
        for i in range(len(sel_editable_poly_nodes)):  
            
            rt.select(sel_editable_poly_nodes[i])

            try:                
                rt.execute ("BBoxLocal = nodeGetBoundingBox $" + sel_editable_poly_nodes[i].name + " $" + sel_editable_poly_nodes[i].name +".transform")
                
                rt.execute ("_bboxMin = BBoxLocal[1]")
                rt.execute ("_bboxMax = BBoxLocal[2]")
                
                rt.execute ("_bboxWidth = abs(_bboxMax.x - _bboxMin.x)")
                rt.execute ("_bboxHeight = abs(_bboxMax.y - _bboxMin.y)")
                rt.execute ("_bboxLength = abs(_bboxMax.z - _bboxMin.z)")

                if abs(rt._bboxMin.x <= rt._bboxWidth) and abs(rt._bboxMax.x <= rt._bboxWidth) and \
                    abs(rt._bboxMin.y <= rt._bboxHeight) and abs(rt._bboxMax.y <= rt._bboxHeight) and \
                        abs(rt._bboxMin.z <= rt._bboxLength) and abs(rt._bboxMax.z <= rt._bboxLength):
                    pass
                else: #outside
                    self.ObjWithBBoxError.append(sel_editable_poly_nodes[i])

            except: #no object

                Errors.append(sel_editable_poly_nodes[i])
                print ("EXCEPTION in 'pivotInsideBBox04' function!")

        self.CheckErrorCount.append(len(Errors))        

        if len(Errors) > 0:
            print ('\n', "ATTENTION! These objects have not been checked because they do not exist, has wrong name or contain serious errors (", len(Errors), "):", '\n')
            for i in range(len(Errors)):
                print ('\t', (str(i+1) + "."), Errors[i])


        if len(self.ObjWithBBoxError) == 0:
            checkMarks[3].setText( green )
            checkLabels[3].setText('4. Pivot inside of objects Bounding Box')
            fixButtons[3].setEnabled(False)
            return True
        else:
            checkMarks[3].setText( yellow )
            checkLabels[3].setText('4. Check Pivot. It\'s outside of objects Bounding Box | (' + str(len(self.ObjWithBBoxError))+")")
            fixButtons[3].setEnabled(True)    

            print ("List of Objects with Pivot Point outside of BoundigBox:")
            for i in range(len( self.ObjWithBBoxError )):
                if len(self.ObjWithBBoxError[i].name) == 0:
                    print ('\t', (str(i+1) + "."), "noname object #" + str(i))
                else: 
                    print ('\t', (str(i+1) + "."), self.ObjWithBBoxError[i].name)
            
            print ('\n', len(self.ObjWithBBoxError), "object(s) Needs to Check the Position of the Pivot Point.")
            return False

    #4 FIX
    def pivotInsideBBoxFix04 (self):

        current_language = cfgl.configLoader()[14] 

        FixResult = []
        
        if len(self.ObjWithBBoxError) > 0:

            print ("List of Objects with Fixed Pivot Point position relative to BBox:")
            
            for i in range(len(self.ObjWithBBoxError)):    

                NodeName = self.ObjWithBBoxError[i]

                unicodeChecker(NodeName)
                
                if str(NodeName) != "<Deleted scene node>":        
                    
                    try:
                        NodeName.pivot = NodeName.center   

                        print ('\t', (str(i+1) + "."), NodeName.name)
                    except:
                        print ("ERROR: Pivot Pointnot Not fixed! Object#" + str(i) + " possibly Deleted, Renamed, Not Exists or has other problems.")
                        FixResult.append(self.ObjWithBBoxError[i])
                else:
                    print("PolygonTools. Object#" + str(i) + " Deleted, Renamed or Not Exists or has other problems!")
                    FixResult.append(self.ObjWithBBoxError[i])

            print ("")

            if len(self.ObjWithBBoxError) == 1 and len(FixResult) == 0:
                self.lblInfo.setText("Pivot inside of " + str(self.ObjWithBBoxError[0].name) + " object BBox.")
            elif len(self.ObjWithBBoxError) > 1 and len(FixResult) == 0:
                self.lblInfo.setText("Pivot inside of " + str(len(self.ObjWithBBoxError)) + " objects BBoxes.")

            if len(FixResult) == 0:
                checkMarks[3].setText( green )
                checkLabels[3].setText('4. Fixed. Pivot inside of objects bounding box')
                fixButtons[3].setEnabled(False)
                conclusion_text = conclusion.fixConclusion(current_language, "4", True)
                self.txtbrowCheckerConclusion.setHtml(conclusion_text) 
                
                print (self.lblInfo.text(), '\n')
                self.pivotPointPos03(self.ObjWithBBoxError) #run 3
            else:
                checkMarks[3].setText( red )
                checkLabels[3].setText("4. Can't Fix pivot for " + str(len(self.ObjWithBBoxError)) + " objects")
                fixButtons[3].setEnabled(False)

                self.lblInfo.setText("Fix Error. Object(s) possibly deleted or renamed. See log.")
                self.lblInfo.setStyleSheet("background-color:#ed1c24;")
                
                print ("PolygonTools:", self.lblInfo.text(), '\n'            )
                conclusion_text = conclusion.fixConclusion(current_language, "4", False)
                self.txtbrowCheckerConclusion.setHtml(conclusion_text) 

            print ("---")

    #5    
    def hiddenfrozenObjects05(self):

        

        Errors = []

        self.hiddenObjects = []

        #try:
        for i in range(len(rt.objects)): 
            try:

                ObjNode = rt.objects[i]
                ObjectClass = str(rt.classOf(ObjNode))

                #ObjName = rt.objects[i].name
                if ObjectClass == "Editable_Poly":

                    if rt.objects[i].isHidden == True:
                        self.hiddenObjects.append(ObjNode)
                        
                    if rt.objects[i].isFrozen == True:
                        self.hiddenObjects.append(ObjNode)
                    
                    #get node by name
                    #ObjNode = rt.getNodeByName ( ObjName )   

                    hidden_vertices = []
                    hidden_faces = []
                    
                    #get BitArrays of verts and Faces
                    VertsBitArray = rt.polyop.getHiddenVerts(ObjNode)
                    FacesBitArray = rt.polyop.getHiddenFaces(ObjNode)

                    for i in range(len(VertsBitArray)):
                        if VertsBitArray[i] == True:
                            hidden_vertices.append(i+1) 

                    for i in range(len(FacesBitArray)):
                        if FacesBitArray[i] == True:
                            hidden_faces.append(i+1)
                    
                    if len(hidden_vertices) > 0:    
                        self.hiddenObjects.append(ObjNode)
                    if len(hidden_faces) > 0:
                        self.hiddenObjects.append(ObjNode)
                else:
                    pass

            except:
                Errors.append(rt.objects[i].name)

        self.CheckErrorCount.append(len(Errors))

        #remove doubles
        self.hiddenObjects = list(dict.fromkeys(self.hiddenObjects))
    

        if len(Errors) > 0:
            print ('\n', "ATTENTION! These objects have not been checked because they do not exist, has wrong name or contain serious errors (", len(Errors), "):", '\n')
            for i in range(len(Errors)):
                print ('\t', (str(i+1) + "."), Errors[i])

        #we check hidden objects, hidden layers 
        if (len(self.hiddenObjects) == 0) and len(Errors) == 0:
            checkMarks[4].setText( green )
            checkLabels[4].setText('5. No hidden objects, faces or vertices on scene')
            fixButtons[4].setEnabled(False)
            return True
        else:
            checkMarks[4].setText( red )
            checkLabels[4].setText('5. Check hidden objects, faces or vertices on scene')
            fixButtons[4].setEnabled(True)

            print ("List of Hidden/Frozen Objects or Objects With Hidden Elements (faces or vertices):")
            
            for i in range(len( self.hiddenObjects )):
                if len(self.hiddenObjects[i].name) == 0:
                    print ('\t', (str(i+1) + "."), "noname object #" + str(i))
                else: 
                    print ('\t', (str(i+1) + "."), self.hiddenObjects[i].name)

            print ('\n', len(self.hiddenObjects), "object(s) Needs to Check Visibility.")
            return False
     
    #5 FIX
    def hiddenfrozenObjectsFix05(self):

        

        current_language = cfgl.configLoader()[14] 

        print ('\n', "Fix result:")
        
        FixResult = []

        #unhide
        for i in range(len(self.hiddenObjects)):

            NodeName = self.hiddenObjects[i]

            #unhide elements
            try:
                rt.execute ("$" + NodeName.name + ".EditablePoly.unhideAll #Face")    
                rt.execute ("$" + NodeName.name + ".EditablePoly.unhideAll #Vertex")
            except:
                FixResult.append(self.hiddenObjects[i])

        #unhide layers
        for i in range(0, rt.LayerManager.count):
            rt.LayerManager.getLayer(i).on = True

        #unhide all
        rt.execute ("max unhide all")        
        rt.execute ("max unfreeze all")        
       
        if len(FixResult) == 0:
            checkMarks[4].setText( green )
            checkLabels[4].setText('5. Fixed. All objects and layers unhidden')
            fixButtons[4].setEnabled(False)
            self.lblInfo.setText("Fixed. All objects and layers unhidden.")
            
            conclusion_text = conclusion.fixConclusion(current_language, "5", True)
            self.txtbrowCheckerConclusion.setHtml(conclusion_text) 

            print (self.lblInfo.text(), '\n')
        else:
            checkMarks[4].setText( red )
            checkLabels[4].setText("5. Can't Fix all hidden objects and layers")
            fixButtons[4].setEnabled(False)
            self.lblInfo.setText("Can't Fix all hidden objects and layers")
            self.lblInfo.setStyleSheet("background-color:#ed1c24;")

            conclusion_text = conclusion.fixConclusion(current_language, "5", False)
            self.txtbrowCheckerConclusion.setHtml(conclusion_text) 

            print (self.lblInfo.text(), '\n')


    #6
    def backFaceCulling06(self, sel_editable_poly_nodes):

        

        #local errors
        Errors = []

        #global backf array
        self.ObjWithBackCull = []
        
        #get backface
        for i in range(len(sel_editable_poly_nodes)):
                                
            #get name and backface
            try:
                BackFace = sel_editable_poly_nodes[i].backfacecull
            except:
                Errors.append(sel_editable_poly_nodes[i])
                print ("EXCEPTION in backFaceCulling06 function!")
            
            #backface false - add to array
            if BackFace == False:
                self.ObjWithBackCull.append(sel_editable_poly_nodes[i])
        
        #add errors to array
        self.CheckErrorCount.append(len(Errors))

        #remove doubles
        self.ObjWithBackCull = list(dict.fromkeys(self.ObjWithBackCull))
        
        #list error
        if len(Errors) > 0:
            print ('\n', "ATTENTION! These objects have not been checked because they do not exist, has wrong name or contain serious errors (", len(Errors), "):\n")
            for i in range(len(Errors)):
                print ('\t', (str(i+1) + "."), Errors[i])

        #one or many objects
        if len(self.ObjWithBackCull) == 0 and len(Errors) == 0:
            checkMarks[5].setText( green )
            checkLabels[5].setText("6. Backface Culling enabled")
            fixButtons[5].setEnabled(False)
            return True
        else:
            checkMarks[5].setText( yellow )
            checkLabels[5].setText("6. Backface Culling disabled | (" + str(len(self.ObjWithBackCull)) + ")")
            fixButtons[5].setEnabled(True)

            print ("List of Objects with the option 'Backface Culling' disabled:")
            
            for i in range(len( self.ObjWithBackCull )):
                if len(self.ObjWithBackCull[i].name) == 0:
                    print ('\t', (str(i+1) + "."), "noname object #" + str(i))
                else: 
                    print ('\t', (str(i+1) + "."), self.ObjWithBackCull[i].name)

            print ('\n', len(self.ObjWithBackCull), "object(s) Needs to Check 'Backface Culling' option.")
            return False
            
    #6 FIX
    def backFaceCullingFix06(self):

        

        current_language = cfgl.configLoader()[14] 

        FixResult = []

        print ("Backface Culling Fix Result:")
        
        for i in range(len(self.ObjWithBackCull)):

                NodeName = self.ObjWithBackCull[i]

                unicodeChecker(NodeName)

                if str(NodeName) != "<Deleted scene node>": 
                    
                    try:
                        NodeName.backfacecull = True
                        
                        if self.ObjWithBackCull[i].name == 0:
                            print ('\t', (str(i+1) + ". noname object #" + str(i)), "- enabled." )
                        else:
                            print ('\t', (str(i+1) + "."), NodeName.name, "- enabled." )

                    except:
                        print ('\t', (str(i+1) + "."), "Object#" + str(i) + " possibly Deleted, Renamed or has other problems!" )
                        FixResult.append(self.ObjWithBackCull[i])
                else:
                    FixResult.append(self.ObjWithBackCull[i])
                    print ('\t', (str(i+1) + "."), "Object#" + str(i) + " possibly Deleted, Renamed or has other problems!" )

        print ("")

        rt.execute ("redrawViews()")
        
        #one or many objects
        if len(self.ObjWithBackCull) == 1 and len(FixResult) == 0:
            self.lblInfo.setText("Backface Culling enabled for " + str(self.ObjWithBackCull[0].name))
        if len(self.ObjWithBackCull) > 1 and len(FixResult) == 0:
            self.lblInfo.setText("Backface Culling enabled for " + str(len(self.ObjWithBackCull)) + " object(s).")

        if len(FixResult) == 0:            
            checkMarks[5].setText( green )
            checkLabels[5].setText("6. Fixed. Backface Culling enabled")
            fixButtons[5].setEnabled(False)

            conclusion_text = conclusion.fixConclusion(current_language, "6", True)
            self.txtbrowCheckerConclusion.setHtml(conclusion_text) 

            print ("PolygonTools:", self.lblInfo.text())
        else:
            checkMarks[5].setText( red )
            checkLabels[5].setText("6. Can't fix Backface Culling for " + str(len(FixResult)) + " object(s)")
            fixButtons[5].setEnabled(False)

            self.lblInfo.setText("Fix Error. " + str(len(FixResult)) + " object(s) possibly not Exists, Deleted or Renamed. See log.")
            self.lblInfo.setStyleSheet("background-color:#ed1c24;")

            conclusion_text = conclusion.fixConclusion(current_language, "6", False)
            self.txtbrowCheckerConclusion.setHtml(conclusion_text) 

            print ("PolygonTools:", self.lblInfo.text(), '\n')

    #7
    def transformationCheck07(self, sel_editable_poly_nodes):

        
        
        Errors = []

        self.ObjWithTransform = []

        SelectedNodes = rt.selection
        
        for i in range(len(sel_editable_poly_nodes)):   

            try:                
                #get transform
                ScaleXYZ = sel_editable_poly_nodes[i].scale

                #select
                rt.select(sel_editable_poly_nodes[i])
                
                #get rotation
                Rotation = rt.execute("quattoeuler $.rotation.controller.value")
                
                #sum of rotation
                RotationXYZSum = Rotation.x + Rotation.y + Rotation.z
                
                if sum(ScaleXYZ) != 3.0 or (RotationXYZSum != 0):
                    self.ObjWithTransform.append( sel_editable_poly_nodes[i] )
                
            except: #no object
                Errors.append( sel_editable_poly_nodes[i] )
                print ("Exception in transformationCheck07 function!")
                
        self.CheckErrorCount.append(len(Errors))

        #remove doubles
        self.ObjWithTransform = list(dict.fromkeys(self.ObjWithTransform))

        #list error
        if len(Errors) > 0:
            print ('\n', "ATTENTION!\nThese objects have not been checked because they do not exist, has wrong name or contain serious errors (", len(Errors), "):\n")
            for i in range(len(Errors)):
                print ('\t', (str(i+1) + "."), Errors[i])

        rt.select(SelectedNodes)
        
        #if 4 - then no transform
        if len(self.ObjWithTransform) == 0:
            checkMarks[6].setText( green )
            checkLabels[6].setText("7. The object(s) hasn\'t transformation")
            fixButtons[6].setEnabled(False)
            return True
        else:
            checkMarks[6].setText( red )
            checkLabels[6].setText("7. The object(s) has transformation (" + str(len(self.ObjWithTransform)) + ")")
            fixButtons[6].setEnabled(True)

            print ("List of Objects With Transformations:")
            
            for i in range(len( self.ObjWithTransform )):
                if len(self.ObjWithTransform[i].name) == 0:
                    print ('\t', (str(i+1) + "."), "noname object #" + str(i))
                else: 
                    print ('\t', (str(i+1) + "."), self.ObjWithTransform[i].name)
            
            print ('\n', len(self.ObjWithTransform), "object(s) Needs to Check Transformation.")
            return False
            

    #7 FIX       
    def transformationFix07(self):

        

        current_language = cfgl.configLoader()[14] 

        FixResult = []
        print ("Transformation Fix result:")
        
        if len(self.ObjWithTransform) > 0:

            for i in range(len(self.ObjWithTransform)):

                    NodeName = self.ObjWithTransform[i]

                    unicodeChecker(NodeName)

                    if str(NodeName) != "<Deleted scene node>":
                        try:                
                            rt.resetxform(NodeName)
                            ObjClass = rt.classOf(NodeName)
                            rt.convertto(NodeName, ObjClass)
                            print ('\t', (str(i+1) + "."), NodeName.name, "- reseted." )
                        except:
                            print ('\t', (str(i+1) + "."), "Object#" + str(i) + " possibly Deleted, Renamed or has other problems!" )
                            FixResult.append(self.ObjWithTransform[i])
                    else:
                        FixResult.append(self.ObjWithTransform[i])
                        print ('\t', (str(i+1) + "."), "Object#" + str(i) + " possibly Deleted, Renamed or has other problems!" )
                                    
            print ("")

            if len(self.ObjWithTransform) == 1:  
                self.lblInfo.setText("Transformation Reseted for " + str(self.ObjWithTransform[0]))
            elif len(self.ObjWithTransform) > 1:
                self.lblInfo.setText("Transformation Reseted for " + str(len(self.ObjWithTransform)) + " objects.")


            if len(FixResult) == 0:
                rt.select(self.ObjWithTransform)

                checkMarks[6].setText( green )
                checkLabels[6].setText("7. Fixed. Transformation Reseted")
                fixButtons[6].setEnabled(False)

                conclusion_text = conclusion.fixConclusion(current_language, "7", True)
                self.txtbrowCheckerConclusion.setHtml(conclusion_text) 

                print ("PolygonTools:", self.lblInfo.text(), '\n')
            else:
                checkMarks[6].setText( red )
                checkLabels[6].setText("7. Cant Fix Transformation for " + str(len(FixResult)) + " object(s)")
                fixButtons[6].setEnabled(False)

                self.lblInfo.setText("Fix Error. " + str(len(FixResult)) + " Object possibly Deleted or Renamed. See log.")
                self.lblInfo.setStyleSheet("background-color:#ed1c24;")

                conclusion_text = conclusion.fixConclusion(current_language, "7", False)
                self.txtbrowCheckerConclusion.setHtml(conclusion_text) 

                print ("PolygonTools:", self.lblInfo.text(), '\n')

    #8
    def correctPolygonsCheck08(self, sel_editable_poly_nodes):

        

        self.ObjWithPolyErrors = []
        
        Errors = []
    
        #list of errors
        errors_list = []

        #get selection
        SelectedNodes = rt.selection
        
        for i in range(len(sel_editable_poly_nodes)):   

            try:
                Concave = False
                NGone = False
                CoPlanar = True
                PolygonProblems = ""
                InputPolygonsValue = 0
                OutpputPolygonsValue = 0

                #select node by name
                rt.select(sel_editable_poly_nodes[i])

                #copy of objects for test
                ConcaveDummy = rt.execute("copy $")
                ConcaveDummy.name = "ConcaveDummy"
                
                NGoneDummy = rt.execute("copy $")
                NGoneDummy.name = "NGoneDummy"
                
                CoPlanarDummy = rt.execute("copy $")
                CoPlanarDummy.name = "CoPlanarDummy"

                #get concave
                InputPolygonsValue = rt.polyop.getNumFaces(ConcaveDummy) 
                rt.execute("addModifier $ConcaveDummy (Turn_to_Poly keepConvex:true removeMidEdgeVertices:false)")
                rt.execute("convertto $ConcaveDummy editable_poly")
                OutpputPolygonsValue = rt.polyop.getNumFaces(ConcaveDummy) 
                rt.delete(ConcaveDummy)

                if InputPolygonsValue != OutpputPolygonsValue:
                    errors_list.append("Concave")
                    self.ObjWithPolyErrors.append( sel_editable_poly_nodes[i] )

                #get nGons
                InputPolygonsValue = rt.polyop.getNumFaces(NGoneDummy) 
                rt.execute("addModifier $NGoneDummy (Turn_to_Poly limitPolySize:true maxPolySize:4 removeMidEdgeVertices:false)")
                rt.execute("convertto $NGoneDummy editable_poly")
                OutpputPolygonsValue = rt.polyop.getNumFaces(NGoneDummy) 
                rt.delete(NGoneDummy)

                if InputPolygonsValue != OutpputPolygonsValue:
                    errors_list.append("nGons")
                    self.ObjWithPolyErrors.append( sel_editable_poly_nodes[i] )
                
                #get Planar
                InputPolygonsValue = rt.polyop.getNumFaces(CoPlanarDummy) 
                rt.execute("addModifier $CoPlanarDummy (Turn_to_Poly requirePlanar:true planarThresh:15.0 removeMidEdgeVertices:false)")
                rt.execute("convertto $CoPlanarDummy editable_poly")
                OutpputPolygonsValue = rt.polyop.getNumFaces(CoPlanarDummy) 
                rt.delete(CoPlanarDummy)

                if InputPolygonsValue != OutpputPolygonsValue:
                    errors_list.append("NoPlanar")
                    self.ObjWithPolyErrors.append( sel_editable_poly_nodes[i] )

            except:
                Errors.append( sel_editable_poly_nodes[i] )
                print ("Exception in correctPolygonsCheck08 function!")

        self.CheckErrorCount.append(len(Errors))        

        #remove repeats
        self.ObjWithPolyErrors = list(dict.fromkeys(self.ObjWithPolyErrors))
        errors_list = list(dict.fromkeys(errors_list))
        
        if len(Errors) > 0:
            print ('\n', "ATTENTION! These objects have not been checked because they do not exist or contain serious errors (", len(Errors), "):", '\n')
            for i in range(len(Errors)):
                print ('\t', (str(i+1) + "."), Errors[i])
            
        #return selection
        rt.select(SelectedNodes)
        
        if len(self.ObjWithPolyErrors) == 0:
            checkMarks[7].setText( green )
            checkLabels[7].setText("8. All polygons are correct")
            fixButtons[7].setEnabled(False)
            return True
        else:
            checkMarks[7].setText( red )
            checkLabels[7].setText("8. Check for errors: " + (', '.join(errors_list)) + " | (" + str(len(self.ObjWithPolyErrors)) + ")")
            fixButtons[7].setEnabled(True)

            print ( "List of Objects With Topology Problems:" )
            for i in range(len( self.ObjWithPolyErrors )):
                if len(self.ObjWithPolyErrors[i].name) == 0:
                    print ('\t', (str(i+1) + "."), "noname object #" + str(i))
                else: 
                    print ('\t', (str(i+1) + "."), self.ObjWithPolyErrors[i].name)
            
            print ('\n', len(self.ObjWithPolyErrors), "object(s) Needs to Check Topology.")
            return False

    #8 Fix    
    def correctPolygonsFix08(self):

        

        current_language = cfgl.configLoader()[14] 

        FixResult = []
        print ("Fix Objects Topology Result:")
                
        if len(self.ObjWithPolyErrors) > 0:
            
            for i in range(len(self.ObjWithPolyErrors)):

                NodeName = self.ObjWithPolyErrors[i]

                unicodeChecker(NodeName)

                if str(NodeName) != "<Deleted scene node>":
                    try:
                        rt.execute("addModifier $" + NodeName.name + " (Turn_to_Poly keepConvex:true limitPolySize:true maxPolySize:4 requirePlanar:true planarThresh:15.0 removeMidEdgeVertices:false)")
                        rt.execute("convertto $" + NodeName.name + " editable_poly")                

                        print ('\t', (str(i+1) + "."), NodeName.name, "- complete." )
                    except:
                            print ('\t', (str(i+1) + "."), "Object#" + str(i) + " possibly Deleted, Renamed or has other problems!" )
                            FixResult.append(self.ObjWithPolyErrors[i])
                else:
                    FixResult.append(self.ObjWithPolyErrors[i])
                    print ('\t', (str(i+1) + "."), "Object#" + str(i) + " possibly Deleted, Renamed or has other problems!" )


        if len(self.ObjWithPolyErrors) == 1 and len(FixResult) == 0:  
            self.lblInfo.setText("Topology Fix complete for " + str(self.ObjWithPolyErrors[0].name))
        elif len(self.ObjWithPolyErrors) > 1 and len(FixResult) == 0:
            self.lblInfo.setText("Topology Fix complete for " + str(len(self.ObjWithPolyErrors)) + " objects.")

        print (""    )

        rt.execute ("redrawViews()")
        
        if len(FixResult) == 0:
            #return select
            rt.select(self.ObjWithPolyErrors)

            checkMarks[7].setText( green )
            checkLabels[7].setText("8. Fixed. All polygons are correct")
            fixButtons[7].setEnabled(False)

            conclusion_text = conclusion.fixConclusion(current_language, "8", True)
            self.txtbrowCheckerConclusion.setHtml(conclusion_text) 

            print (self.lblInfo.text(), '\n')
        else:
            checkMarks[7].setText( red )
            checkLabels[7].setText("8. Can't fix " + str(len(FixResult)) + " objects")
            fixButtons[7].setEnabled(False)

            self.lblInfo.setText("Fix Error. " + str(len(FixResult)) + " Object possibly deleted or renamed. See log.")
            self.lblInfo.setStyleSheet("background-color:#ed1c24;")

            conclusion_text = conclusion.fixConclusion(current_language, "8", False)
            self.txtbrowCheckerConclusion.setHtml(conclusion_text) 

            print ("PolygonTools:", self.lblInfo.text(), '\n')

    #9
    def materialCheck09(self, sel_editable_poly_nodes):

        

        self.ObjWithMatProblems = []       
        
        Errors = []

        print ("List of Materials Assigned to Objects:" )
        
        problems_data = []

        for i in range(len(sel_editable_poly_nodes)):

            try:
                Material = str(sel_editable_poly_nodes[i].material)
                MaterialClass = str(rt.classOf(sel_editable_poly_nodes[i].material))
                ObjectName = sel_editable_poly_nodes[i].name

                if len(ObjectName) == 0:
                    ObjectName = "noname object #" + str(i)

                try:
                    MaterialName = str(sel_editable_poly_nodes[i].material.name)
                except:
                    MaterialName = "None"


                if Material == "None":
                    print ('\t', (str(i+1) + "."), ObjectName, "-> ATTENTION! Object without material.")
                    self.ObjWithMatProblems.append(sel_editable_poly_nodes[i])  
                    problems_data.append("Undefined")
                elif MaterialClass != "Standardmaterial":
                    print ('\t', (str(i+1) + "."), ObjectName, "-> ATTENTION! Object uses Non Standard material.")
                    self.ObjWithMatProblems.append(sel_editable_poly_nodes[i])
                    problems_data.append("Non Standard")
                elif "- Default" in MaterialName and (MaterialClass == "Standardmaterial"):
                    print ('\t', (str(i+1) + "."), ObjectName, "-> ATTENTION! Default material assigned to the object.")
                    self.ObjWithMatProblems.append(sel_editable_poly_nodes[i])
                    problems_data.append("Default")
                else:
                    print ('\t', (str(i+1) + "."), ObjectName, "->", MaterialName)


                #diffuse maps check 
                if sel_editable_poly_nodes[i].material != None:
                    DiffuseMapEnabled = sel_editable_poly_nodes[i].material.diffuseMapEnable                
                    DiffuseMap = sel_editable_poly_nodes[i].material.diffuseMap
                else:
                    DiffuseMapEnabled = False
                    DiffuseMap = None

                try:    
                    if DiffuseMap != None:
                        DiffuseMapFilename = sel_editable_poly_nodes[i].material.diffuseMap.filename
                except:
                    print ('\t\t', "Diffuse Map Enabled but Unsupported Map Used!")
                    self.ObjWithMatProblems.append(sel_editable_poly_nodes[i])
                    problems_data.append("Unsup")
                    DiffuseMapFilename = "Unsupported"
                                    
                if DiffuseMapEnabled == True and DiffuseMap == None:
                    print ('\t\t', "Diffuse Map Enabled but Empty!")
                    self.ObjWithMatProblems.append(sel_editable_poly_nodes[i])
                    problems_data.append("DiffMap")
                
                if DiffuseMapEnabled != True and DiffuseMap != None:
                    print ('\t\t', "Diffuse Map Not Empty but Disabled!")
                    self.ObjWithMatProblems.append(sel_editable_poly_nodes[i])
                    problems_data.append("DiffMap")

                if DiffuseMap != None and len(DiffuseMapFilename) == 0:
                    print ('\t\t', "Diffuse Map Enabled but has Empty Bitmap!")
                    self.ObjWithMatProblems.append(sel_editable_poly_nodes[i])
                    problems_data.append("ZeroBitmap")

            except:
                Errors.append(sel_editable_poly_nodes[i])
                print ("Exception in materialCheck09 function!")
                 
        self.CheckErrorCount.append(len(Errors))

        #remove repeats
        problems_data = list(dict.fromkeys(problems_data))
        
        if len(Errors) > 0:
            print ('\n', "ATTENTION! These objects have not been checked because they do not exist or contain serious errors (", len(Errors), "):", '\n')
            for i in range(len(Errors)):
                print ('\t', (str(i+1) + "."), Errors[i])

        if len(self.ObjWithMatProblems) == 0:
            checkMarks[8].setText( green )
            checkLabels[8].setText("9. No problem with materials")
            fixButtons[8].setEnabled(False)
            return True
        else:      #no material or default or non standard
            checkMarks[8].setText( red )
            checkLabels[8].setText("9. Material problems: " + (', '.join(problems_data)) + " | (" + str(len(self.ObjWithMatProblems)) + ")")
            fixButtons[8].setEnabled(True)
            
            print ('\n', len(self.ObjWithMatProblems), "object(s) Needs to Check Materials."              )
            return False
    
    #9 FIX
    def materialFix09(self):

        

        current_language = cfgl.configLoader()[14] 

        FixResult = []
        print ("Fix Materials result:")

        if len(self.ObjWithMatProblems) > 0:

            for i in range(len(self.ObjWithMatProblems)):

                NodeName = self.ObjWithMatProblems[i]

                unicodeChecker(NodeName)

                one_node = []

                if str(NodeName) != "<Deleted scene node>":

                    one_node.append(NodeName)

                    try:
                        #fixed_material_obj, assigned_material_obj
                        fix_material_data = gen_func.materialFixer(one_node, "Fix")

                        fixed_material_obj = fix_material_data[0]
                        assigned_material_obj = fix_material_data[1]

                        if len(fixed_material_obj) != 0:
                            for i in range(len(fixed_material_obj)):
                                print ('\t', (str(i+1) + "."), fixed_material_obj[i].name, "- name fixed.")

                        if len(assigned_material_obj) != 0:
                            for i in range(len(assigned_material_obj)):
                                print ('\t', (str(i+1) + "."), assigned_material_obj[i].name, "- material assigned.")
                    except:
                            print ('\t', (str(i+1) + "."), "Object#" + str(i) + " possibly Deleted, Renamed or has other problems!" )
                            FixResult.append(self.ObjWithMatProblems[i])
                else:
                    FixResult.append(self.ObjWithMatProblems[i])
                    print ('\t', (str(i+1) + "."), "Object#" + str(i) + " possibly Deleted, Renamed or has other problems!" )
            
            rt.execute ("macros.run \"Medit Tools\" \"clear_medit_slots\"")

            #add to Slots
            Slot = 0
            
            for Material in rt.scenematerials:
                if rt.scenematerials.count < 24:
                    rt.meditMaterials[Slot] = Material
                    Slot += 1
                else:
                    pass

            rt.execute ("redrawViews()")         
            print (""           )

            if len(self.ObjWithMatProblems) == 1:
                self.lblInfo.setText("Material has been fixed to " + str(self.ObjWithMatProblems[0].name))
            elif len(self.ObjWithMatProblems) > 1:
                self.lblInfo.setText("Materials has been fixed to " + str(len(self.ObjWithMatProblems)) + " objects.")

            if len(FixResult) == 0:
                checkMarks[8].setText( green )
                checkLabels[8].setText("9. Temporary material has been assigned")
                fixButtons[8].setEnabled(False)

                conclusion_text = conclusion.fixConclusion(current_language, "9", True)
                self.txtbrowCheckerConclusion.setHtml(conclusion_text) 

                print (self.lblInfo.text())
            else:
                checkMarks[8].setText( red )
                checkLabels[8].setText("9. Can't fix " + str(len(FixResult)) + " objects")
                fixButtons[8].setEnabled(False)
                self.lblInfo.setText("Fix Error. Object possibly deleted or renamed. See log.")
                self.lblInfo.setStyleSheet("background-color:#ed1c24;")

                conclusion_text = conclusion.fixConclusion(current_language, "9", False)
                self.txtbrowCheckerConclusion.setHtml(conclusion_text) 

                print ("PolygonTools:", self.lblInfo.text(), '\n')

    #10
    def uvBorderCheck10(self, sel_editable_poly_nodes):
        
        try:
            uvrange_stat_data =  gen_func.uvRangeStat(sel_editable_poly_nodes)
        except:
             self.CheckErrorCount.append("gen_func.uvRangeStat")
             print ("Exception in 'uvBorderCheck10' or 'gen_func.uvRangeStat' function!")
        
        if  len(uvrange_stat_data[0]) > 0:
            checkMarks[9].setText( yellow )
            checkLabels[9].setText("10. Some UV shells outside [0,1] area | (" + str(len(uvrange_stat_data[0])) + ")")

            print ('\n', len(uvrange_stat_data[0]), "object(s) Needs to Check UV Shells Position."   )

            return False
        else:
            checkMarks[9].setText( green )
            checkLabels[9].setText("10. All UV shells inside [0,1] area")
            return True

    #11   
    def uvSetsCountCheck11(self, sel_editable_poly_nodes):

        self.ObjWithManyUVSets = []
        
        Errors = []

        try:
            uvset_stat_data = gen_func.uvSetStat(sel_editable_poly_nodes)
            self.ObjWithManyUVSets = uvset_stat_data[1]
        except:
             Errors.append("1")
             print ("Exception in uvSetsCountCheck11 function!")
        
        self.CheckErrorCount.append(len(Errors))
        
        if len(self.ObjWithManyUVSets) == 0:
            checkMarks[10].setText( green )
            checkLabels[10].setText("11. Quantity of Map Channels: 1")
            fixButtons[10].setEnabled(False)
            return True
        else:
            checkMarks[10].setText( yellow )
            checkLabels[10].setText("11. Check qty. of Map Channels. Some objects has > 1 | (" + str(len(self.ObjWithManyUVSets)) + ")")
            fixButtons[10].setEnabled(False)

            print ("List of Objects with many Map Channels:")
            for i in range(len( self.ObjWithManyUVSets )):
                if len(self.ObjWithManyUVSets[i].name) == 0:
                    print ('\t', (str(i+1) + "."), "noname object #" + str(i))
                else: 
                    print ('\t', (str(i+1) + "."), self.ObjWithManyUVSets[i].name)

            return False

    #12
    def uvUtilCheck12(self, sel_editable_poly_nodes):

        
    
        self.AllUVAreas = []

        print ("Objects UV utilization list:")
        
        ObjectsWithUV = []
        
        #UVarea - check LOW UV-utilization
        for i in range(len(sel_editable_poly_nodes)):
            
            one_obj_arr = []
            one_obj_arr.append(sel_editable_poly_nodes[i])

            #one obj util
            UVAreaSum = gen_func.uvUtilStat(one_obj_arr)

            if len(sel_editable_poly_nodes[i].name) == 0:
                print ('\t', str(i+1) + ".", "noname object #" + str(i), "-", UVAreaSum[0], "%"                )
            else:
                print ('\t', str(i+1) + ".", sel_editable_poly_nodes[i].name, "-", UVAreaSum[0], "%"                )

            if UVAreaSum[0] > 0:                    
                self.AllUVAreas.append(UVAreaSum[0])
                ObjectsWithUV.append(sel_editable_poly_nodes[i])

        try:
            UVAareaAvg = sum(self.AllUVAreas)/len(self.AllUVAreas) 
            print ('\n', "Average UV-Utilization (%):", UVAareaAvg            )
        except:
            print ("UV Area Array values:", sum(self.AllUVAreas), "/", len(self.AllUVAreas) )
            print ("Cant calculate average UV-Utilization. Maybe problems with UV layout.")
            self.CheckErrorCount.append("uvUtilCheck12")
        
        print ("")

        rt.select(sel_editable_poly_nodes)
        uv_data = gen_func.uvUtilStat(sel_editable_poly_nodes)

        FinalUV = uv_data[0]
                
        #UV ranges
        dangerous_uv_range = range(95,101)
        ideal_uv_range = range(67,96)
        medium_uv_range = range(50,68)
        low_uv_range = range(1,51)
        
        checkLabels[11].setStyleSheet("")

        #ideal_uv_range 
        if FinalUV in ideal_uv_range:
            checkMarks[11].setText( green )
            checkLabels[11].setText("12. Current UV utilization: " + str(FinalUV) + "% | Good")
            return True

        #medium_uv_range                
        if FinalUV in medium_uv_range:
            checkMarks[11].setText( yellow )
            checkLabels[11].setText("12. Current UV utilization: " + str(FinalUV) + "% | Normal")
            print ("Try to do UV layout more efficiently!")
            return False

        #low_uv_range 
        if FinalUV in low_uv_range:
            checkMarks[11].setText( red )
            checkLabels[11].setText("12. Current UV utilization: " + str(FinalUV) + "% | Low")
            print ("UV Utilization is Low!")
            return False

        #dangerous_uv_range                            
        if FinalUV in dangerous_uv_range:
            checkMarks[11].setText( red )
            checkLabels[11].setText("12. Current UV utilization: " + str(FinalUV) + "% | Suspicious")
            print ("Check padding, overlap and range on UV layout!")
            return False
                    
        if  FinalUV == 0:
            checkMarks[11].setText( red )
            checkLabels[11].setStyleSheet("color:#ed1c24;")
            checkLabels[11].setText("12. Check UV mapping! UV utilization: 0% | No UV-layout")
            return False

    #13 SG
    def sgCheck13(self, sel_editable_poly_nodes):

        

        self.SGProblems = []

        smooth_group_data = []
        
        # 0-obj_without_problems, obj_with_merged_sg, obj_without_sg, obj_with_many_sg, sg_count, 5 - sg_check_result, many_id, 7-normal_id, 8 - objects_poly_problems
        try:
            smooth_group_data = gen_func.smoothingGroupsCheck(sel_editable_poly_nodes)
            SmoothCheckResult = (', '.join(smooth_group_data[5]))
        except:
            self.CheckErrorCount.append("sgCheck13")            

        
        
        if len(smooth_group_data[1]) != 0:
            for i in range(len(smooth_group_data[1])):
                self.SGProblems.append(smooth_group_data[1][i][0][0])

        if len(smooth_group_data[2]) != 0:
            for i in range(len(smooth_group_data[2])):
                self.SGProblems.append(smooth_group_data[2][i][0][0])

        if len(smooth_group_data[3]) != 0:
            for i in range(len(smooth_group_data[3])):
                self.SGProblems.append(smooth_group_data[3][i][0][0])

        #remove doubles
        self.SGProblems = list(dict.fromkeys(self.SGProblems))

        #Mat ID
        if len(smooth_group_data[6]) == 0:
            checkMarks[13].setText( green )
            checkLabels[13].setText("14. Quantity of Material ID's: 1")            
        else:
            checkMarks[13].setText( yellow )
            checkLabels[13].setText("14. Some Objects has many Material ID's")

        #SG
        if len(smooth_group_data[0]) > 0 and len(smooth_group_data[1]) == 0 and len(smooth_group_data[2]) == 0 and len(smooth_group_data[3]) == 0:
            checkMarks[12].setText( green )
            checkLabels[12].setText("13. No Problem with Smoothing Groups")
            fixButtons[12].setEnabled(False)
            return True
        else:
            checkMarks[12].setText( yellow )
            checkLabels[12].setText("13. Smoothing Groups Problems: " + SmoothCheckResult + " SG")
            fixButtons[12].setEnabled(True)
            return False
    
    #13 FIX
    def sgFix13(self):

        

        current_language = cfgl.configLoader()[14] 

        FixResult = []

        print ("Fix Smoothing Groups result:")

        if len(self.SGProblems) > 0:

            rt.execute("max modify mode")

            for i in range(len(self.SGProblems)):

                NodeName = self.SGProblems[i]

                unicodeChecker(NodeName)

                one_node = []

                if str(NodeName) != "<Deleted scene node>":

                    try:
                        #ObjClass = rt.classOf(NodeName)
                        rt.execute("modPanel.addModToSelection (smooth ()) ui:on")
                        NodeName.modifiers[0].autosmooth = True
                        NodeName.modifiers[0].threshold = 45
                        #rt.convertto(NodeName, ObjClass)

                        if len(self.SGProblems[i].name) == 0:
                            print ('\t', str(i+1) + ".", "noname object #" + str(i), "- fixed."               )
                        else:
                            print ('\t', str(i+1) + ".", self.SGProblems[i].name, "- fixed."            )
                        
                    except:
                            print ('\t', (str(i+1) + "."), "Object#" + str(i) + " possibly Deleted, Renamed or has other problems!" )
                            FixResult.append(self.SGProblems[i])
                else:
                    FixResult.append(self.SGProblems[i])
                    print ('\t', (str(i+1) + "."), "Object#" + str(i) + " possibly Deleted, Renamed or has other problems!" )

            rt.select(self.SGProblems)
            rt.execute ("macros.run \"Modifier Stack\" \"Convert_to_Poly\"")            
            rt.execute ("redrawViews()")         
            print (""           )

        if len(self.SGProblems) == 1:
            self.lblInfo.setText("Smothing Groups has been fixed to " + str(self.SGProblems[0].name))
        elif len(self.SGProblems) > 1:
            self.lblInfo.setText("Smothing Groups has been fixed to " + str(len(self.SGProblems)) + " objects.")

        if len(FixResult) == 0:
            checkMarks[12].setText( green )
            checkLabels[12].setText("13. Smoothing Groups were assigned automatically.")
            fixButtons[12].setEnabled(False)

            conclusion_text = conclusion.fixConclusion(current_language, "10", True)
            self.txtbrowCheckerConclusion.setHtml(conclusion_text) 

            print (self.lblInfo.text(), '\n')
        else:
            checkMarks[12].setText( red )
            checkLabels[12].setText("13. Can't fix " + str(len(FixResult)) + " object(s)")
            fixButtons[12].setEnabled(False)
            self.lblInfo.setText("Fix Error. Object possibly deleted or renamed. See log.")
            self.lblInfo.setStyleSheet("background-color:#ed1c24;")

            conclusion_text = conclusion.fixConclusion(current_language, "10", False)
            self.txtbrowCheckerConclusion.setHtml(conclusion_text) 

            print ("PolygonTools:", self.lblInfo.text(), '\n')


def namesChecker (sel_editable_poly_nodes):

    
    
    #array for errors
    name_errors = []
    
    #names in scene for matching
    used_names = []
    
    naming_problems = []

    material_data = []
    
    #get scene name
    FileDirectory = rt.maxFilePath
    CurrentSceneFileName = rt.execute ("getFilenameFile maxFileName")

    FullPathToFBXfile = FileDirectory + CurrentSceneFileName
    PathToSave = FileDirectory
    
    #SCENE NAME
    if len(FullPathToFBXfile) == 0:
        name_errors.append("scene name")
        print ("ATTENTION! Scene Not Saved. Please Save the Scene!")
    else:
        print ("Current scene name is:", CurrentSceneFileName)
        used_names.append(CurrentSceneFileName)  

    #get layers names
    LayersCount = rt.LayerManager.count

    if LayersCount > 1:
        for i in range(0, LayersCount):
            Layer = rt.LayerManager.getLayer(i)
            LayerName = Layer.name
            used_names.append(LayerName)
    
    for i in range(len(sel_editable_poly_nodes)):

        print ("")

        if len(sel_editable_poly_nodes[i].name) == 0:
            print (str(i+1) + ". Noname Object #" + str(i))
            print ('\t', "Object without name. Please Name the Object!")
            used_names.append("Noname object")
            name_errors.append("obj. name")
        elif len(sel_editable_poly_nodes[i].name) > 32:
            print (str(i+1) + "."), str("'" + sel_editable_poly_nodes[i].name + "'")
            print ('\t', "Object has too Long Name. More than 32 characters. Please Shorten the Name!")
            used_names.append("Longname object")
            name_errors.append("longname")
        else:
            try:
                print ((str(i+1) + "."), str("'" + sel_editable_poly_nodes[i].name + "'"))
            except:
                sel_editable_poly_nodes[i].name = "pt_renamed_object_" + str(i)
                print (str("'" + sel_editable_poly_nodes[i].name + "'"))

        #get object name
        used_names.append(sel_editable_poly_nodes[i].name)
        
        #get material
        try:
            MaterialName = sel_editable_poly_nodes[i].material.name
        except:
            MaterialName = ""

        #check name
        if len(MaterialName) == 0:
            #ErrorName = "mat. availability"
            name_errors.append("mat. name")
            print ('\t', "The assigned material does not have a name or material not assigned. Name or Assign the material!")
        else:
            print ('\t', "Assigned material name:", MaterialName  )
            used_names.append(MaterialName)     

            if "- Default" in MaterialName:
                print ('\t', "Object uses default material name. Better rename it!")


        #unstripped path to file
        try:
            DiffuseMap = sel_editable_poly_nodes[i].material.diffuseMap
            DiffuseMapEnabled = sel_editable_poly_nodes[i].material.diffuseMapEnable
            DiffuseMapFilename = sel_editable_poly_nodes[i].material.diffuseMap.filename
            if ":\\" or "\\" in DiffuseMapFilename:
                name_errors.append("unstrip")
                print ('\t\t', "Please check Path to Bitmap File and Maybe Strip It!")
        except:
            pass

    #remove repeats
    name_errors = list(dict.fromkeys(name_errors))

    #standard names is not good 'Shape'
    bad_names = ['Sphere', 'Tube', 'Cylinder', 'Cone', 'Torus', 'Plane', 'Teapot', 'Box', 'GeoSphere', 'Pyramid', ':', 'untitled', 'Layer0', '- Default', 'Noname object', 'Longname object']

    naming_problems = [s for s in used_names if any(xs in s for xs in bad_names)]

    #remove repeats
    naming_problems = list(dict.fromkeys(naming_problems))

    print (""            )
    
    if len(naming_problems) > 0:
        print ("List of Naming problems on Scene:")
        
        for i in range(len( naming_problems )):
            print ('\t', (str(i+1) + "."), naming_problems[i])

        name_errors.append("naming rules | (" + str(len(naming_problems)) + ")")
        print ('\n', len(naming_problems), "naming problems found.")
        
    return name_errors


def unicodeChecker(NodeName):
    try:
        NameCheck = str(NodeName)        
    except:
        print ('\t', "ATTENTION! Write the name of this object in English using latin letters:", NodeName.name)
        NodeName.name = "pt_renamed_object_" + str(random.randrange(1, 1000)) #random rename
        print ('\t', "Object has been automatically renamed! New name:", NodeName.name)

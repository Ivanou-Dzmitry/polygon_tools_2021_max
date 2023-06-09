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

from PySide2 import QtWidgets, QtCore, QtGui
import os
import sys
import shiboken2
from pymxs import runtime as rt


#add Paths
TempCurrentDir = os.path.dirname(__file__)
CurrentDir = TempCurrentDir.replace ("\\", "/")

#path to config file
TempPtModPath = (CurrentDir + "\\pt_modules")
PtModPath = TempPtModPath.replace ("\\", "/")

if CurrentDir not in sys.path:
  sys.path.append( CurrentDir )

if PtModPath not in sys.path:
  sys.path.append( PtModPath )
  
import importlib

import pt_gui as gui
importlib.reload(gui)

def main():    
    #get main window
    main_window_qwdgt = QtWidgets.QWidget.find(rt.windows.getMAXHWND())

    main_window = shiboken2.wrapInstance(shiboken2.getCppPointer(main_window_qwdgt)[0], QtWidgets.QMainWindow)
    
    #create ptgui
    ptdlg = gui.PTGUI(parent = main_window)

    #set and show
    ptdlg.setFloating(True)
    ptdlg.show()    

if __name__ == '__main__':
	main()    

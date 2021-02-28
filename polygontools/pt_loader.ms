--******************************************************************************************************
-- Created: polygon.by		
-- Last Updated: 5 may 2020
-- Version: 2.0.0
--
-- Authors:  
-- Dzmitry Ivanou
-- Dzmitry Dzrynou
--
--******************************************************************************************************
-- MODIFY THIS AT YOUR OWN RISK


macroScript PolygonTools2
 category:"POLYGON"
 tooltip:"PolygonTools 2"
 buttonText:"PolygonTools 2"
 Icon: #("polygontools", 1)

(

scriptsDir = getDir #scripts
UserScriptsDir = getDir #userScripts 
userIconsDir = getDir #userIcons

-- Main Module File Name
PT_MainModule = UserScriptsDir+"\polygontools\polygon_tools.py"

--Execute Main Module
python.ExecuteFile PT_MainModule

)
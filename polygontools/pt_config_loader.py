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
import weakref

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import * 

from polygon_tools import *
from pt_modules.pt_gen_func import *
from pt_modules.pt_set_func import *

global LoadingCounter
LoadingCounter = 0

#sys info
def MySysInfo():
    import platform;
    print ("SYS INFO: " + (platform.sys.version))

#write to config func
def ConfigWriter(Section, Variable, Value, Path, Config):
    
    #set path
    PTConfigFilePath = Path
    
    #set config
    PTConfig = Config
     
    try:
        PTConfig.set(Section, Variable, Value + '\n\r')
    except:
        print ("EXCEPTION With function 'PTConfig.set'")
        MySysInfo()
            
    try:
        with open(PTConfigFilePath, 'w') as CFG:
            PTConfig.write(CFG)
            print ("PolygonTools. " + "[" + Section + "] " + Variable +" = "+ Value + " write to config file.")
    except:
        print("EXCEPTION With function 'ConfigWriter.Open'\n")
        MySysInfo()

#reader form config file
def readValuesFromConfig(PTConfig, PTConfigFilePath):

    #call function count    
    global LoadingCounter
    LoadingCounter = LoadingCounter + 1

    #global read_cfg_error_count
    ReadCfgErrorCount = 0
    config_values = []

    #0    
    try:
        MapResolution = PTConfig.get('Texel', 'map_resolution')
        config_values.append(MapResolution)
    except:
        print ("ERROR: Can't read 'Map resolution' value from config file.")
        ReadCfgErrorCount = ReadCfgErrorCount + 1
        PTConfig.set('Texel', 'map_resolution', '3')    
        config_values.append(3)

    #1
    try:
        TexelValue = PTConfig.get('In-Range', 'Texel')
        config_values.append(TexelValue)
    except:
        print ("PolygonTools. ERROR: Can't read 'Texel value' from config file.")
        ReadCfgErrorCount = ReadCfgErrorCount + 1
        PTConfig.set('In-Range', 'Texel', '256')
        config_values.append(256)
    
    #2    
    try:
        DiffValue = PTConfig.get('In-Range', 'Difference')
        config_values.append(DiffValue)
    except:
        print ("PolygonTools. ERROR: Can't read Difference value from config file.")
        ReadCfgErrorCount = ReadCfgErrorCount + 1
        PTConfig.set('In-Range', 'Difference', '20')
        config_values.append(20)
    
    #3    
    try:
        TinyItValue = PTConfig.get('In-Range', 'Tiny_it')
        config_values.append(TinyItValue)
    except:
        print ("PolygonTools. ERROR: Can't read Tiny_it value from config file.")
        ReadCfgErrorCount = ReadCfgErrorCount + 1
        PTConfig.set('In-Range', 'Tiny_it', '0.0001')
        config_values.append(0.0001)
    
    #4    
    try:
        TinyUvValue = PTConfig.get('In-Range', 'Tiny UV')
        config_values.append(TinyUvValue)
    except:
        print ("PolygonTools. ERROR: Can't read Tiny UV value from config file.")
        ReadCfgErrorCount = ReadCfgErrorCount + 1
        PTConfig.set('In-Range', 'Tiny UV', '1')
        config_values.append(1)
    
    #5    
    try:
        lod1value = PTConfig.get('LOD_distance', 'lod1') 
        config_values.append(lod1value)
    except:
        print ("PolygonTools. ERROR: Can't read lod1 value from config file.")
        ReadCfgErrorCount = ReadCfgErrorCount + 1
        PTConfig.set('LOD_distance', 'lod1', '10')
        config_values.append(10)
    
    #6    
    try:
        lod2value = PTConfig.get('LOD_distance', 'lod2')
        config_values.append(lod2value)
    except:
        print ("PolygonTools. ERROR: Can't read lod2 value from config file.")
        ReadCfgErrorCount = ReadCfgErrorCount + 1
        PTConfig.set('LOD_distance', 'lod2', '20')
        config_values.append(20)
    
    #7    
    try:
        lod3value = PTConfig.get('LOD_distance', 'lod3')
        config_values.append(lod3value)
    except:
        print ("PolygonTools. ERROR: Can't read lod3 value from config file.")
        ReadCfgErrorCount = ReadCfgErrorCount + 1
        PTConfig.set('LOD_distance', 'lod3', '40')
        config_values.append(40)
        
    #8
    try:
        lod4value = PTConfig.get('LOD_distance', 'lod4')
        config_values.append(lod4value)
    except:
        print ("PolygonTools. ERROR: Can't read lod4 value from config file.")
        ReadCfgErrorCount = ReadCfgErrorCount + 1
        PTConfig.set('LOD_distance', 'lod4', '60')
        config_values.append(60)
    
    #9
    try:
        CustomSysUnits = PTConfig.get('Units', 'Custom_System_type_units')
        config_values.append(CustomSysUnits)
    except:
        print ("PolygonTools. ERROR: Can't read Custom_System_type_units value from config file.")
        ReadCfgErrorCount = ReadCfgErrorCount + 1
        PTConfig.set('Units', 'Custom_System_type_units', 'meters')
        config_values.append("meters")

    #10
    try:
        CustomDispUnits = PTConfig.get('Units', 'Custom_Display_units')
        config_values.append(CustomDispUnits)
    except:
        print ("PolygonTools. ERROR: Can't read Custom_Display_units value from config file.")
        ReadCfgErrorCount = ReadCfgErrorCount + 1
        PTConfig.set('Units', 'Custom_Display_units', 'Generic')
        config_values.append("Generic")
    
    #11    
    try:
        desired_texel = PTConfig.get('Texel', 'desired_texel')
        config_values.append(desired_texel)
    except:
        print ("PolygonTools. ERROR: Can't read desired texel value from config file.")
        ReadCfgErrorCount = ReadCfgErrorCount + 1
        PTConfig.set('Texel', 'desired_texel', '400')
        config_values.append(400)
    
    #12    
    try:
        intersection_depth = PTConfig.get('Tools', 'intersection_depth')
        config_values.append(intersection_depth)
    except:
        print ("PolygonTools. ERROR: Can't read intersection depth value from config file.")
        ReadCfgErrorCount = ReadCfgErrorCount + 1
        PTConfig.set('Tools', 'intersection_depth', '10')
        config_values.append(10)

    #13    
    try:
        target_face_count = PTConfig.get('Tools', 'target_face_count')
        config_values.append(target_face_count)
    except:
        print ("PolygonTools. ERROR: Can't read target face count value from config file.")
        ReadCfgErrorCount = ReadCfgErrorCount + 1
        PTConfig.set('Tools', 'target_face_count', '100')
        config_values.append(100)

    #14    
    try:
        current_languge = PTConfig.get('Languge', 'current_languge')
        config_values.append(current_languge)
    except:
        print ("PolygonTools. ERROR: Can't read current languge value from config file.")
        ReadCfgErrorCount = ReadCfgErrorCount + 1
        PTConfig.set('Languge', 'current_languge', 'eng')
        config_values.append("eng")

    #add empty for future
    for i in range(0, 83):
        config_values.append("Empty")
    
    #98    
    config_values.append(ReadCfgErrorCount ) 
        
    #Fix wrong values
    if ReadCfgErrorCount  > 0:
        try:
            with open(PTConfigFilePath, 'w') as cfg:
                PTConfig.write(cfg)
                PTConfig.close()
                print ("PolygonTools. Some values not read (see log above). Default values was write to file.")
        except:
            print ("EXCEPTION in function 'ReadValuesFromConfig.Open'")
            MySysInfo()
    else:
        if LoadingCounter == 1:
            print ("PolygonTools:\n\tData from config file was loaded.")

    return config_values

#get cfg file path
def getConfigFilePath():

    #get current dir
    CurrentDir = os.path.dirname(__file__)

    #config file
    PTConfigFile = 'polygontoolspack_settings.ini'
    
    #path to config file
    TempPTConfigFilePath = CurrentDir + "\\" + PTConfigFile
    PTConfigFilePath = TempPTConfigFilePath.replace ("\\", "/")

    return PTConfigFilePath

def getPTConfig():

    try:
        from configparser import ConfigParser
    except ImportError:
        from ConfigParser import ConfigParser  # ver. < 3.0
    
    #config data
    PTConfig = ConfigParser()
    
    return PTConfig

#Data loader
def configLoader():
    
    global LoadingCounter
    
    #get path
    PTConfigFilePath = getConfigFilePath() 

    #config data
    PTConfig = getPTConfig()

    read_data = []
                
    try:
        if os.path.getsize(PTConfigFilePath) > 0:
            
            #read config
            try:            
                PTConfig.read(PTConfigFilePath)
            except:
                print ("PolygonTools: ATTENTION! Problems with config file was detected!")
                createDefaultConfig(PTConfig, PTConfigFilePath)

            #read data from config
            read_data = readValuesFromConfig(PTConfig, PTConfigFilePath)

            #add new data - path and config
            read_data.append(PTConfigFilePath)
            read_data.append(PTConfig)
            
            #13 - number of read problems            
            if (read_data[98] == 0):
                if LoadingCounter == 1:                
                    print ("\tConfig file was successfully read!", "\n\tPath to config", read_data[99], '\n')
            else:
                print ("\tATTENTION!\n\tPolygonTools Config file was read with " + str(read_data[98]) + " errors! Default values was loaded.")
                        
        else:
            #create default config
            createDefaultConfig(PTConfig, PTConfigFilePath)
    
    except OSError as e:
        try: 
            print ("PolygonTools: PT_CONFIG_LOADER.\n\tATTENTION! Config File does not Exists or is non Accessible!")
            MySysInfo()
            PTConfig = open(PTConfigFilePath,'w')
            print ("PolygonTools: PT_CONFIG_LOADER.\n\tEmpty Config file was successfully created - " + PTConfigFilePath)
            PTConfig.close()
        except:
            print("ConfigLoader.OSError") 
        finally:            
            PTConfig = getPTConfig()
            createDefaultConfig(PTConfig, PTConfigFilePath)

            #read data from config
            read_data = readValuesFromConfig(PTConfig, PTConfigFilePath)

            #add new data - path and config
            read_data.append(PTConfigFilePath)
            read_data.append(PTConfig)

    return read_data

#write config file with default values
def createDefaultConfig (ptconfig, pt_configfile_path):        
    
    print ('\n', "Restore sections and values:", '\n')
    
    try:
        import configparser as cfgp
    except:
        import ConfigParser as cfgp

    #Add all default values to file
    try:
        ptconfig.add_section("Texel")
        print ("Texel section restored!")
        ptconfig.set('Texel', 'Map_resolution', '3')
        ptconfig.set('Texel', 'desired_texel', '400')
    except cfgp.DuplicateSectionError:
        ptconfig.set('Texel', 'Map_resolution', '3')
        ptconfig.set('Texel', 'desired_texel', '400')
    finally:
        print ('\t', "Texel values restored!")
    
    try:    
        ptconfig.add_section("In-Range")
        print ("In-Range section restored!")
        ptconfig.set('In-Range', 'Texel', '256')
        ptconfig.set('In-Range', 'Difference', '10')
        ptconfig.set('In-Range', 'Tiny_it', '0.0001')
        ptconfig.set('In-Range', 'Tiny UV', '1')
    except cfgp.DuplicateSectionError:
        ptconfig.set('In-Range', 'Texel', '256')
        ptconfig.set('In-Range', 'Difference', '10')
        ptconfig.set('In-Range', 'Tiny_it', '0.0001')
        ptconfig.set('In-Range', 'Tiny UV', '1')
    finally:
        print ('\t', "In-Range values restored!")
    
    try:    
        ptconfig.add_section("LOD_distance")
        print ("LOD_distance section restored!")
        ptconfig.set('LOD_distance', 'lod1', '10')
        ptconfig.set('LOD_distance', 'lod2', '20')
        ptconfig.set('LOD_distance', 'lod3', '40')
        ptconfig.set('LOD_distance', 'lod4', '60')
    except cfgp.DuplicateSectionError:
        ptconfig.set('LOD_distance', 'lod1', '10')
        ptconfig.set('LOD_distance', 'lod2', '20')
        ptconfig.set('LOD_distance', 'lod3', '40')
        ptconfig.set('LOD_distance', 'lod4', '60')
    finally:
        print ('\t', "LOD_distance values restored!")
        
    try:        
        ptconfig.add_section("Units")
        print ("Units section restored!")
        ptconfig.set('Units', 'Custom_System_type_units', 'meters')
        ptconfig.set('Units', 'Custom_Display_units', 'Generic')
    except cfgp.DuplicateSectionError:
        ptconfig.set('Units', 'Custom_System_type_units', 'meters')
        ptconfig.set('Units', 'Custom_Display_units', 'Generic')
    finally:
        print ('\t', "Units value restored!")
    
    try:    
        ptconfig.add_section("Tools")
        print ("Tools section restored!")
        ptconfig.set('Tools', 'intersection_depth', '10')
        ptconfig.set('Tools', 'target_face_count', '100')
    except cfgp.DuplicateSectionError:
        ptconfig.set('Tools', 'intersection_depth', '10')
        ptconfig.set('Tools', 'target_face_count', '100')
    finally:
        print ('\t', "Tools values restored!")

    try:
        ptconfig.add_section("Languge")
        print ("Languge section restored!")
        ptconfig.set('Languge', 'current_languge', 'eng')
    except cfgp.DuplicateSectionError:
        ptconfig.set('Languge', 'current_languge', 'eng')
    finally:
        print ('\t', "Languge values restored!")
        
    print ("")
        
    #Try to save data to the config file
    try:
        with open(pt_configfile_path, 'w') as cfg:
            ptconfig.write(cfg)
            print ("PolygonTools. Config file with default values was successfully created! Please reload PolygonTools.\n")
    except:
        print ("EXCEPTION in function 'createDefaultConfig.Open'\n") 
        MySysInfo()
# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              CeshiAttachment
# Author:            Hygnic
# Created on:        2022/9/4 17:21
# Version:           
# Reference:         
"""
Description:         
Usage:               
"""
# -------------------------------------------
import arcpy


#>>>>>>>>>> Path
arcpy.env.workspace = r"C:\Users\Administrator\Documents\ArcGIS\test.gdb"

workspace = arcpy.env.workspace

walk = arcpy.da.Walk(workspace)
for dirpath, dirnames, filenames in walk:
    for filename in filenames:
        print filename

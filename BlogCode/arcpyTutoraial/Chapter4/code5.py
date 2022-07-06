# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              code5
# Author:            Hygnic
# Created on:        2021/5/21 16:31
# Version:           ArcGIS10.3 Python 2.7.8
# Reference:         
"""
Description:         
Usage:               
"""
# -------------------------------------------
import arcpy
import os
arcpy.env.overwriteOutput = True

# ▶注释1◀
arcpy.env.scratchWorkspace = os.getcwd()
arcpy.env.workspace = "../"

lyr_p = "../SHP/Boroughs.shp"
# ▶注释2◀
arcpy.CopyFeatures_management(lyr_p, "out5")
# ▶注释3◀
arcpy.CopyFeatures_management(
    lyr_p, os.path.join(arcpy.env.scratchFolder, "out5"))
arcpy.CopyFeatures_management(lyr_p, "%scratchFolder%/out5_1")
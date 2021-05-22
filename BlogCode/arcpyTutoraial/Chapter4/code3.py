# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              code3
# Author:            Hygnic
# Created on:        2021/5/21 13:10
# Version:           ArcGIS10.3 Python 2.7.8
# Reference:         
"""
Description:         
Usage:               
"""
# -------------------------------------------
from __future__ import unicode_literals
import arcpy
import os
arcpy.env.overwriteOutput = True

arcpy.env.scratchWorkspace = os.getcwd()

lyr_p = "../SHP/Boroughs.shp"
arcpy.CopyFeatures_management(lyr_p, "%scratchGDB%/out1")
arcpy.CopyFeatures_management(lyr_p, "%scratchFolder%/out2.shp")

print(arcpy.env.scratchFolder)
print(arcpy.env.scratchGDB)
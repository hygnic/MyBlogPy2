# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              code6
# Author:            Hygnic
# Created on:        2021/5/21 17:33
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

arcpy.env.workspace = os.getcwd()

lyr_p = "../SHP/Boroughs.shp"

# ▶注释1◀
inmemory = "in_memory/line1"
arcpy.FeatureToLine_management(lyr_p, inmemory)
arcpy.CopyFeatures_management(inmemory, "out6")
# ▶注释2◀
del inmemory
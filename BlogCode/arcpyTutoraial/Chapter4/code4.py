# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              code4
# Author:            Hygnic
# Created on:        2021/5/21 15:17
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
name1 = arcpy.CreateScratchName(workspace=arcpy.env.scratchFolder)
name2 = arcpy.CreateScratchName(workspace=arcpy.env.scratchGDB)
print "name1: {}".format(name1)
print "name2: {}".format(name2)

arcpy.CopyFeatures_management(lyr_p, name1)
arcpy.CopyFeatures_management(lyr_p, name2)
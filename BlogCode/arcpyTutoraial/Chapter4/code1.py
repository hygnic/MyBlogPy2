# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              code3
# Author:            Hygnic
# Created on:        2021/5/21 11:26
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

lyr_p = "../SHP/Boroughs.shp"
gdb = "YC.gdb"
if not arcpy.Exists(gdb): # ▶注释1◀
    arcpy.CreateFileGDB_management(os.getcwd(), gdb)
arcpy.env.workspace = "YC.gdb"

arcpy.CopyFeatures_management(lyr_p, "Water2")
arcpy.Delete_management("Water2")
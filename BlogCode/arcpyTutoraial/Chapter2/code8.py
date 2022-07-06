# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              code8
# Author:            Hygnic
# Created on:        2021/5/13 16:23
# Version:           ArcGIS10.3 Python 2.7.8
# Reference:         
"""
Description:         
Usage:               
"""
# -------------------------------------------
import arcpy


# ▶注释1◀
arcpy.env.workspace = "../SHP"
fcs = arcpy.ListFeatureClasses()
for fc in fcs:
    print fc
    
    
# ▶注释2◀
arcpy.env.workspace = "../NYC.gdb"
fcs = arcpy.ListFeatureClasses("*Water*")
for fc in fcs:
    print fc